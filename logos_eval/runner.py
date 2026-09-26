"""Eval runner — invokes only Core extract / render / expand."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Optional

from logos_core.interface import CoreInterface, InProcessCore

DEFAULT_SUITE = Path(__file__).parent / "suite" / "gold_v1.json"


@dataclass
class CaseResult:
    id: str
    domain: str
    match_mode: str
    passed: bool
    detail: str = ""


@dataclass
class EvalReport:
    total: int
    passed: int
    failed: int
    results: list[CaseResult] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.failed == 0


def run_evals(core: CoreInterface, suite_path: str | Path) -> EvalReport:
    path = Path(suite_path)
    cases = json.loads(path.read_text(encoding="utf-8"))
    results: list[CaseResult] = []

    for case in cases:
        case_id = case["id"]
        domain = case.get("domain", "")
        mode = case["match_mode"]
        expect = case.get("expect", {})
        text = case["input"]

        try:
            canonical = core.extract(text)
            if mode == "structural":
                ok, detail = _match_structural(canonical, expect)
            elif mode == "render_l1":
                rendered = core.render(canonical, 1)
                ok, detail = _match_render_l1(rendered, expect)
            elif mode == "symbols_subset":
                ok, detail = _match_symbols_subset(canonical, expect)
            elif mode == "density":
                ok, detail = _match_density(canonical, expect)
            else:
                ok, detail = False, f"unknown match_mode: {mode}"
        except Exception as exc:  # noqa: BLE001 — report as failed case
            ok, detail = False, f"exception: {exc}"

        results.append(
            CaseResult(
                id=case_id,
                domain=domain,
                match_mode=mode,
                passed=ok,
                detail=detail,
            )
        )

    passed = sum(1 for r in results if r.passed)
    failed = len(results) - passed
    return EvalReport(total=len(results), passed=passed, failed=failed, results=results)


def _macros(canonical: Any) -> set[str]:
    return {n.macro for n in canonical.nodes if n.macro}


def _symbols(canonical: Any) -> set[str]:
    return {n.symbol for n in canonical.nodes}


def _match_structural(canonical: Any, expect: dict) -> tuple[bool, str]:
    want_macros = set(expect.get("macros", []))
    want_syms = set(expect.get("symbols", []))
    have_macros = _macros(canonical)
    have_syms = _symbols(canonical)
    missing_m = want_macros - have_macros
    missing_s = want_syms - have_syms
    if missing_m or missing_s:
        return False, f"missing macros={sorted(missing_m)} symbols={sorted(missing_s)}"
    if not canonical.nodes:
        return False, "no nodes extracted"
    return True, "ok"


def _match_render_l1(rendered: str, expect: dict) -> tuple[bool, str]:
    needles = expect.get("contains", [])
    missing = [n for n in needles if n not in rendered]
    if missing:
        return False, f"render missing {missing}; got={rendered!r}"
    if not rendered.strip():
        return False, "empty render"
    return True, "ok"


def _match_symbols_subset(canonical: Any, expect: dict) -> tuple[bool, str]:
    want = set(expect.get("symbols", []))
    have = _symbols(canonical)
    missing = want - have
    if missing:
        return False, f"missing symbols={sorted(missing)}; have={sorted(have)}"
    return True, "ok"


def _match_density(canonical: Any, expect: dict) -> tuple[bool, str]:
    """Open-prose density floor — min nodes / coverage / optional macro any-of."""
    min_nodes = int(expect.get("min_nodes", 1))
    min_ratio = float(expect.get("min_matched_ratio", 0.0))
    macros_any = set(expect.get("macros_any", []))
    n = len(canonical.nodes)
    ratio = float(canonical.coverage.matched_ratio)
    if n < min_nodes:
        return False, f"nodes={n} < min_nodes={min_nodes}"
    if ratio < min_ratio:
        return False, f"matched_ratio={ratio:.3f} < min={min_ratio}"
    if macros_any:
        have = _macros(canonical)
        if not (have & macros_any):
            return False, f"none of macros_any={sorted(macros_any)}; have={sorted(have)}"
    return True, "ok"


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="logos-eval")
    parser.add_argument(
        "--suite",
        default=str(DEFAULT_SUITE),
        help="Path to gold suite JSON",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    report = run_evals(InProcessCore(), args.suite)
    if args.json:
        print(json.dumps(asdict(report), ensure_ascii=False, indent=2))
    else:
        for r in report.results:
            mark = "PASS" if r.passed else "FAIL"
            print(f"[{mark}] {r.id} ({r.match_mode}) {r.detail}")
        print(f"\n{report.passed}/{report.total} passed")
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
