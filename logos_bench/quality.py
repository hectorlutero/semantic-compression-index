"""Quality bench — evaluate extract renders at L1 / L2 / L3.

Uses one extract per item, then scores each level against gold.
Does not replace logos-bench (latency/ratio) or logos-eval (pass/fail gates).
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Optional

from logos_core.index import symbol_macro
from logos_core.interface import CoreInterface, InProcessCore

DEFAULT_CORPUS = Path(__file__).parent / "corpus" / "quality_v1.json"
DEFAULT_BASELINE = Path(__file__).parent / "baselines" / "quality_v1.json"
REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ACERVO = REPO_ROOT / "acervo"


@dataclass
class LevelScore:
    level: int
    recall: float
    precision: float
    f1: float
    needles_ok: bool
    non_empty: bool
    found: list[str] = field(default_factory=list)
    render: str = ""


@dataclass
class ItemQuality:
    id: str
    domain: str
    nodes: int
    matched_ratio: float
    l1: LevelScore
    l2: LevelScore
    l3: LevelScore
    consistency_l1_l3: bool
    consistency_l2_l3: bool
    floors_ok: bool
    detail: str = ""


@dataclass
class QualityReport:
    items: list[ItemQuality]
    f1_l1_avg: float
    f1_l2_avg: float
    f1_l3_avg: float
    needles_l1_pct: float
    needles_l2_pct: float
    needles_l3_pct: float
    floors_pass_pct: float
    consistency_pct: float
    by_domain: dict[str, dict[str, float]] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    failed_thresholds: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failed_thresholds


def _safe_div(n: float, d: float) -> float:
    return n / d if d else 0.0


def _f1(recall: float, precision: float) -> float:
    if recall + precision == 0:
        return 0.0
    return 2 * recall * precision / (recall + precision)


def _score_set(found: set[str], gold: set[str]) -> tuple[float, float, float]:
    if not gold:
        # No gold for this axis — N/A; treat as neutral 1.0 (excluded from averages)
        return 1.0, 1.0, 1.0
    inter = found & gold
    recall = _safe_div(len(inter), len(gold))
    precision = _safe_div(len(inter), len(found)) if found else 0.0
    return recall, precision, _f1(recall, precision)


def _needles_ok(render: str, needles: list[str]) -> bool:
    return all(n in render for n in needles)


def score_item(core: CoreInterface, item: dict[str, Any]) -> ItemQuality:
    text = item["text"]
    gold = item.get("gold") or {}
    floors = item.get("floors") or {}
    min_nodes = int(floors.get("min_nodes", 0))
    min_ratio = float(floors.get("min_matched_ratio", 0.0))

    canonical = core.extract(text)
    r1 = core.render(canonical, 1)
    r2 = core.render(canonical, 2)
    r3 = core.render(canonical, 3)

    macros = {n.macro for n in canonical.nodes if n.macro}
    categories = {n.category for n in canonical.nodes if n.category}
    symbols = {n.symbol for n in canonical.nodes}

    g1 = set((gold.get("l1") or {}).get("macros") or [])
    g2 = set((gold.get("l2") or {}).get("categories") or [])
    g3 = set((gold.get("l3") or {}).get("symbols") or [])
    n1 = list((gold.get("l1") or {}).get("contains") or [])
    n2 = list((gold.get("l2") or {}).get("contains") or [])
    n3 = list((gold.get("l3") or {}).get("contains") or [])

    rec1, prec1, f1_1 = _score_set(macros, g1)
    rec2, prec2, f1_2 = _score_set(categories, g2)
    rec3, prec3, f1_3 = _score_set(symbols, g3)

    # Consistency: L3 symbols' macros ⊆ L1 macros; L2 render cats ⊆ node cats
    l3_macros = {m for sym in symbols if (m := symbol_macro(sym))}
    cons_l1_l3 = l3_macros <= macros if symbols else True
    cons_l2_l3 = True
    if r2:
        for chunk in r2.split(" ∧ "):
            if ":" in chunk:
                cat = chunk.split(":", 1)[0].strip()
                if cat and cat not in categories and cat != "unknown":
                    cons_l2_l3 = False

    floors_ok = len(canonical.nodes) >= min_nodes and float(
        canonical.coverage.matched_ratio
    ) >= min_ratio

    detail_parts = []
    if not floors_ok:
        detail_parts.append(
            f"floors nodes={len(canonical.nodes)}<{min_nodes} or "
            f"ratio={canonical.coverage.matched_ratio:.3f}<{min_ratio}"
        )
    if not cons_l1_l3:
        detail_parts.append(f"l1/l3 macros mismatch want⊇{sorted(l3_macros)}")

    return ItemQuality(
        id=item["id"],
        domain=item.get("domain", ""),
        nodes=len(canonical.nodes),
        matched_ratio=float(canonical.coverage.matched_ratio),
        l1=LevelScore(1, rec1, prec1, f1_1, _needles_ok(r1, n1), bool(r1.strip()), sorted(macros), r1),
        l2=LevelScore(2, rec2, prec2, f1_2, _needles_ok(r2, n2), bool(r2.strip()), sorted(categories), r2),
        l3=LevelScore(3, rec3, prec3, f1_3, _needles_ok(r3, n3), bool(r3.strip()), sorted(symbols), r3),
        consistency_l1_l3=cons_l1_l3,
        consistency_l2_l3=cons_l2_l3,
        floors_ok=floors_ok,
        detail="; ".join(detail_parts),
    )


def _avg(vals: list[float]) -> float:
    return sum(vals) / len(vals) if vals else 0.0


def _pct(flags: list[bool]) -> float:
    return 100.0 * _safe_div(sum(1 for f in flags if f), len(flags))


def run_quality(
    core: CoreInterface,
    corpus: str | Path | list[dict[str, Any]],
    baseline: Optional[str | Path] = None,
) -> QualityReport:
    if isinstance(corpus, (str, Path)):
        items = json.loads(Path(corpus).read_text(encoding="utf-8"))
    else:
        items = corpus

    results = [score_item(core, it) for it in items]

    # Only average F1 when gold axis was non-empty for that item
    def f1s(level: str) -> list[float]:
        out = []
        for it, raw in zip(results, items):
            g = (raw.get("gold") or {}).get(level) or {}
            key = "macros" if level == "l1" else "categories" if level == "l2" else "symbols"
            if g.get(key):
                out.append(getattr(it, level).f1)
        return out

    by_domain: dict[str, dict[str, float]] = {}
    domains = sorted({r.domain for r in results if r.domain})
    for d in domains:
        subset = [r for r in results if r.domain == d]
        by_domain[d] = {
            "count": float(len(subset)),
            "f1_l3_avg": _avg([r.l3.f1 for r in subset]),
            "f1_l1_avg": _avg([r.l1.f1 for r in subset]),
            "floors_pass_pct": _pct([r.floors_ok for r in subset]),
        }

    report = QualityReport(
        items=results,
        f1_l1_avg=_avg(f1s("l1")),
        f1_l2_avg=_avg(f1s("l2")),
        f1_l3_avg=_avg(f1s("l3")),
        needles_l1_pct=_pct([r.l1.needles_ok for r in results]),
        needles_l2_pct=_pct([r.l2.needles_ok for r in results]),
        needles_l3_pct=_pct([r.l3.needles_ok for r in results]),
        floors_pass_pct=_pct([r.floors_ok for r in results]),
        consistency_pct=_pct([r.consistency_l1_l3 and r.consistency_l2_l3 for r in results]),
        by_domain=by_domain,
    )

    if baseline is None:
        baseline = DEFAULT_BASELINE
    bpath = Path(baseline)
    if bpath.is_file():
        cfg = json.loads(bpath.read_text(encoding="utf-8"))
        for key, label in [
            ("min_f1_l1", "f1_l1_avg"),
            ("min_f1_l2", "f1_l2_avg"),
            ("min_f1_l3", "f1_l3_avg"),
            ("min_floors_pass_pct", "floors_pass_pct"),
        ]:
            if key in cfg:
                got = getattr(report, label)
                want = float(cfg[key])
                if got + 1e-9 < want:
                    msg = f"{label}={got:.3f} < baseline {key}={want}"
                    if cfg.get("strict"):
                        report.failed_thresholds.append(msg)
                    else:
                        report.warnings.append(msg)

    return report


def corpus_from_acervo(acervo_root: Path) -> list[dict[str, Any]]:
    """Project curated expects into quality corpus items (L1/L3 from sidecars)."""
    curated = acervo_root / "curated"
    items: list[dict[str, Any]] = []
    if not curated.is_dir():
        return items
    for side in sorted(curated.glob("*.expect.json")):
        stem = side.name.replace(".expect.json", "")
        # find txt
        matches = list(acervo_root.rglob(f"{stem}.txt"))
        matches = [p for p in matches if "curated" not in p.parts]
        if not matches:
            continue
        path = matches[0]
        meta = json.loads(side.read_text(encoding="utf-8"))
        expect = meta.get("expect") or {}
        domain = meta.get("domain") or path.relative_to(acervo_root).parts[0]
        gold: dict[str, Any] = {"l1": {}, "l2": {}, "l3": {}}
        if expect.get("macros"):
            gold["l1"]["macros"] = list(expect["macros"])
            gold["l1"]["contains"] = [f"{m}(" for m in expect["macros"]]
        if expect.get("macros_any"):
            # soft: any-of not expressible as full set — skip hard L1 set
            pass
        if expect.get("symbols"):
            gold["l3"]["symbols"] = list(expect["symbols"])
        floors = {}
        if "min_nodes" in expect:
            floors["min_nodes"] = expect["min_nodes"]
        if "min_matched_ratio" in expect:
            floors["min_matched_ratio"] = expect["min_matched_ratio"]
        items.append(
            {
                "id": f"acervo-{stem}",
                "domain": domain,
                "text": path.read_text(encoding="utf-8").strip(),
                "gold": gold,
                "floors": floors,
                "source": str(path.relative_to(acervo_root)).replace("\\", "/"),
            }
        )
    return items


def report_to_dict(report: QualityReport) -> dict[str, Any]:
    return {
        "f1_l1_avg": report.f1_l1_avg,
        "f1_l2_avg": report.f1_l2_avg,
        "f1_l3_avg": report.f1_l3_avg,
        "needles_l1_pct": report.needles_l1_pct,
        "needles_l2_pct": report.needles_l2_pct,
        "needles_l3_pct": report.needles_l3_pct,
        "floors_pass_pct": report.floors_pass_pct,
        "consistency_pct": report.consistency_pct,
        "by_domain": report.by_domain,
        "warnings": report.warnings,
        "failed_thresholds": report.failed_thresholds,
        "items": [asdict(i) for i in report.items],
    }


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="logos-bench-quality")
    parser.add_argument("--corpus", default=str(DEFAULT_CORPUS))
    parser.add_argument("--baseline", default=str(DEFAULT_BASELINE))
    parser.add_argument("--from-acervo", action="store_true", help="Usar curated/ do acervo")
    parser.add_argument("--acervo", default=str(DEFAULT_ACERVO))
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write", metavar="PATH", help="Gravar relatório JSON")
    args = parser.parse_args(argv)

    if args.from_acervo:
        corpus: str | Path | list = corpus_from_acervo(Path(args.acervo))
        if not corpus:
            print("acervo curated vazio", file=sys.stderr)
            return 1
    else:
        corpus = args.corpus

    report = run_quality(InProcessCore(), corpus, baseline=args.baseline)
    payload = report_to_dict(report)

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(
            f"F1 L1={report.f1_l1_avg:.3f}  L2={report.f1_l2_avg:.3f}  "
            f"L3={report.f1_l3_avg:.3f}"
        )
        print(
            f"needles% L1={report.needles_l1_pct:.0f} L2={report.needles_l2_pct:.0f} "
            f"L3={report.needles_l3_pct:.0f}  floors_pass%={report.floors_pass_pct:.0f}  "
            f"consistency%={report.consistency_pct:.0f}"
        )
        for d, agg in report.by_domain.items():
            print(
                f"  [{d}] n={int(agg['count'])} f1_l1={agg['f1_l1_avg']:.3f} "
                f"f1_l3={agg['f1_l3_avg']:.3f} floors%={agg['floors_pass_pct']:.0f}"
            )
        for w in report.warnings:
            print(f"WARN {w}", file=sys.stderr)
        for f in report.failed_thresholds:
            print(f"FAIL {f}", file=sys.stderr)
        weak = [i for i in report.items if i.l3.f1 < 0.5 or not i.floors_ok]
        if weak:
            print(f"\nweak items ({len(weak)}):", file=sys.stderr)
            for i in weak[:12]:
                print(
                    f"  {i.id}: L3_f1={i.l3.f1:.2f} nodes={i.nodes} {i.detail}",
                    file=sys.stderr,
                )

    if args.write:
        out = Path(args.write)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {out}", file=sys.stderr)

    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
