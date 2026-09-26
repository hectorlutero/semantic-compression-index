"""Fase 1 #14 — density gate on Core seam via eval runner."""

from __future__ import annotations

import json

from logos_core import InProcessCore
from logos_eval import run_evals
from logos_eval.runner import DEFAULT_SUITE


def test_density_match_mode_passes_on_open_prose(tmp_path):
    suite = tmp_path / "density.json"
    suite.write_text(
        json.dumps(
            [
                {
                    "id": "density-open",
                    "domain": "narrativa",
                    "input": (
                        "Maria transformou-se após a crise. Ela estava com João no começo. "
                        "A luz da esperança enfrentou as trevas do medo."
                    ),
                    "match_mode": "density",
                    "expect": {
                        "min_nodes": 3,
                        "min_matched_ratio": 0.08,
                        "macros_any": ["BE", "RELATE", "DYN"],
                    },
                }
            ]
        ),
        encoding="utf-8",
    )
    report = run_evals(InProcessCore(), suite)
    assert report.ok, [(r.id, r.detail) for r in report.results if not r.passed]


def test_density_match_mode_fails_when_sparse(tmp_path):
    suite = tmp_path / "sparse.json"
    suite.write_text(
        json.dumps(
            [
                {
                    "id": "deliberate-sparse",
                    "domain": "test",
                    "input": "xyzzy plugh foobar sem padrao conhecido qq",
                    "match_mode": "density",
                    "expect": {"min_nodes": 2, "min_matched_ratio": 0.1},
                }
            ]
        ),
        encoding="utf-8",
    )
    report = run_evals(InProcessCore(), suite)
    assert not report.ok
    assert report.failed == 1


def test_full_gold_includes_density_cases():
    report = run_evals(InProcessCore(), DEFAULT_SUITE)
    assert report.ok, [(r.id, r.detail) for r in report.results if not r.passed]
    modes = {r.match_mode for r in report.results}
    assert "density" in modes
