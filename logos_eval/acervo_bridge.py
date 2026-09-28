"""Bridge: acervo em txt → preview Core → draft gold para logos-eval.

Invoca apenas o seam Core (extract / render / expand). Não alarga regras.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable, Optional

from logos_core.interface import CoreInterface, InProcessCore
from logos_eval.runner import run_evals

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ACERVO = REPO_ROOT / "acervo"
DEFAULT_SUITE = Path(__file__).parent / "suite" / "gold_acervo.json"
CURATED_DIRNAME = "curated"
STUBS_DIRNAME = "stubs"


def _stem_id(path: Path) -> str:
    return path.stem


def _slug_domain(path: Path, acervo_root: Path) -> str:
    try:
        rel = path.relative_to(acervo_root)
    except ValueError:
        return "acervo"
    parts = rel.parts
    if len(parts) >= 2 and parts[0] not in {STUBS_DIRNAME, CURATED_DIRNAME}:
        return parts[0]
    return "acervo"


def iter_txt(acervo_root: Path, *, include_stubs: bool = False) -> list[Path]:
    root = acervo_root.resolve()
    if not root.is_dir():
        return []
    files: list[Path] = []
    for path in sorted(root.rglob("*.txt")):
        if CURATED_DIRNAME in path.parts:
            continue
        if not include_stubs and STUBS_DIRNAME in path.parts:
            continue
        files.append(path)
    return files


def curated_expect_path(acervo_root: Path, txt_path: Path) -> Path:
    return acervo_root / CURATED_DIRNAME / f"{txt_path.stem}.expect.json"


def load_curated(acervo_root: Path, txt_path: Path) -> Optional[dict[str, Any]]:
    side = curated_expect_path(acervo_root, txt_path)
    if not side.is_file():
        return None
    return json.loads(side.read_text(encoding="utf-8"))


def _span_json(span: Any) -> Any:
    if span is None:
        return None
    if isinstance(span, (str, int, float, bool, list, dict)):
        return span
    # Core Span dataclass / namedtuple — keep JSON-safe fields only
    start = getattr(span, "start", None)
    end = getattr(span, "end", None)
    if start is not None or end is not None:
        return {"start": start, "end": end}
    return str(span)


def preview_one(core: CoreInterface, text: str) -> dict[str, Any]:
    canonical = core.extract(text)
    nodes = [
        {
            "macro": n.macro,
            "symbol": n.symbol,
            "span": _span_json(getattr(n, "span", None)),
        }
        for n in canonical.nodes
    ]
    return {
        "node_count": len(canonical.nodes),
        "matched_ratio": float(canonical.coverage.matched_ratio),
        "macros": sorted({n.macro for n in canonical.nodes if n.macro}),
        "symbols": sorted({n.symbol for n in canonical.nodes}),
        "nodes": nodes,
        "render_l1": core.render(canonical, 1),
        "expand": core.expand(canonical),
    }


def draft_case(
    txt_path: Path,
    acervo_root: Path,
    curated: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    text = txt_path.read_text(encoding="utf-8").strip()
    curated = curated if curated is not None else load_curated(acervo_root, txt_path)
    case_id = _stem_id(txt_path)
    domain = (curated or {}).get("domain") or _slug_domain(txt_path, acervo_root)
    match_mode = (curated or {}).get("match_mode") or "density"
    expect = (curated or {}).get("expect")
    if expect is None:
        # Draft floor until human curates — not a claim of gold truth.
        expect = {"min_nodes": 1, "min_matched_ratio": 0.0}
    return {
        "id": f"acervo-{case_id}",
        "domain": domain,
        "source": str(txt_path.relative_to(acervo_root)).replace("\\", "/"),
        "input": text,
        "match_mode": match_mode,
        "expect": expect,
    }


def build_suite(
    acervo_root: Path,
    paths: Iterable[Path],
    *,
    curated_only: bool = True,
) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for path in paths:
        curated = load_curated(acervo_root, path)
        if curated_only and curated is None:
            continue
        cases.append(draft_case(path, acervo_root, curated))
    return cases


def write_suite(suite_path: Path, cases: list[dict[str, Any]]) -> None:
    suite_path.parent.mkdir(parents=True, exist_ok=True)
    suite_path.write_text(
        json.dumps(cases, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def cmd_list(args: argparse.Namespace) -> int:
    files = iter_txt(Path(args.acervo), include_stubs=args.include_stubs)
    for path in files:
        side = curated_expect_path(Path(args.acervo), path)
        mark = "curated" if side.is_file() else "raw"
        print(f"[{mark}] {path}")
    print(f"\n{len(files)} ficheiro(s) .txt", file=sys.stderr)
    return 0


def cmd_preview(args: argparse.Namespace) -> int:
    acervo = Path(args.acervo)
    core = InProcessCore()
    targets = [Path(p) for p in args.paths] if args.paths else iter_txt(
        acervo, include_stubs=args.include_stubs
    )
    if not targets:
        print("nenhum .txt no acervo", file=sys.stderr)
        return 1
    out: list[dict[str, Any]] = []
    for path in targets:
        text = path.read_text(encoding="utf-8")
        item = {
            "path": str(path),
            "id": _stem_id(path),
            "chars": len(text),
            "preview": preview_one(core, text),
            "curated": load_curated(acervo, path) is not None,
        }
        out.append(item)
        if not args.json:
            p = item["preview"]
            print(f"== {path.name} ==")
            print(f"nodes={p['node_count']} matched_ratio={p['matched_ratio']:.3f}")
            print(f"macros={p['macros']} symbols={p['symbols']}")
            print(f"render_l1: {p['render_l1']}")
            print(f"expand: {p['expand'][:200]}{'…' if len(p['expand']) > 200 else ''}")
            print()
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


def cmd_draft(args: argparse.Namespace) -> int:
    acervo = Path(args.acervo)
    suite_path = Path(args.suite)
    files = iter_txt(acervo, include_stubs=args.include_stubs)
    cases = build_suite(acervo, files, curated_only=not args.include_uncurated)
    if args.write:
        write_suite(suite_path, cases)
        print(f"wrote {len(cases)} case(s) → {suite_path}", file=sys.stderr)
    else:
        print(json.dumps(cases, ensure_ascii=False, indent=2))
    return 0


def cmd_eval(args: argparse.Namespace) -> int:
    suite_path = Path(args.suite)
    if not suite_path.is_file():
        print(f"suite em falta: {suite_path}", file=sys.stderr)
        return 1
    cases = json.loads(suite_path.read_text(encoding="utf-8"))
    if not cases:
        print("gold_acervo vazio — nada a avaliar (ok até haver curated)", file=sys.stderr)
        return 0
    report = run_evals(InProcessCore(), suite_path)
    for r in report.results:
        mark = "PASS" if r.passed else "FAIL"
        print(f"[{mark}] {r.id} ({r.match_mode}) {r.detail}")
    print(f"\n{report.passed}/{report.total} passed")
    return 0 if report.ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="logos-acervo",
        description="Acervo em txt → preview Core → draft gold (seam extract/render/expand)",
    )
    parser.add_argument(
        "--acervo",
        default=str(DEFAULT_ACERVO),
        help="Raiz do acervo (default: ./acervo)",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="Listar .txt do acervo")
    p_list.add_argument("--include-stubs", action="store_true")
    p_list.set_defaults(func=cmd_list)

    p_prev = sub.add_parser("preview", help="extract/render/expand sobre o acervo")
    p_prev.add_argument("paths", nargs="*", help="Ficheiros .txt (default: todos no acervo)")
    p_prev.add_argument("--include-stubs", action="store_true")
    p_prev.add_argument("--json", action="store_true")
    p_prev.set_defaults(func=cmd_preview)

    p_draft = sub.add_parser("draft", help="Gerar casos gold a partir de txt + curated")
    p_draft.add_argument("--suite", default=str(DEFAULT_SUITE))
    p_draft.add_argument("--write", action="store_true", help="Escrever suite em disco")
    p_draft.add_argument(
        "--include-uncurated",
        action="store_true",
        help="Incluir txt sem sidecar (expect density mínimo)",
    )
    p_draft.add_argument("--include-stubs", action="store_true")
    p_draft.set_defaults(func=cmd_draft)

    p_eval = sub.add_parser("eval", help="Correr logos-eval sobre gold_acervo.json")
    p_eval.add_argument("--suite", default=str(DEFAULT_SUITE))
    p_eval.set_defaults(func=cmd_eval)

    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
