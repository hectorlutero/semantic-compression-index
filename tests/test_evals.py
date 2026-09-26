"""Eval suite tests (#6)."""

from __future__ import annotations

from logos_core import InProcessCore
from logos_eval import run_evals
from logos_eval.runner import DEFAULT_SUITE


def test_gold_suite_passes():
    report = run_evals(InProcessCore(), DEFAULT_SUITE)
    failed = [r for r in report.results if not r.passed]
    assert report.ok, f"failed cases: {[(r.id, r.detail) for r in failed]}"


def test_runner_exits_nonzero_on_deliberate_fail(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(
        """[{
          "id": "deliberate-fail",
          "domain": "test",
          "input": "hello world",
          "match_mode": "structural",
          "expect": {"macros": ["BE"], "symbols": ["Γ"]}
        }]""",
        encoding="utf-8",
    )
    report = run_evals(InProcessCore(), bad)
    assert not report.ok
    assert report.failed == 1
