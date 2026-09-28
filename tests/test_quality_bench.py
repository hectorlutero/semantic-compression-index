"""Quality bench L1/L2/L3."""

from __future__ import annotations

from logos_bench.quality import DEFAULT_CORPUS, run_quality
from logos_core import InProcessCore


def test_quality_corpus_runs():
    report = run_quality(InProcessCore(), DEFAULT_CORPUS)
    assert report.items
    assert report.f1_l3_avg >= 0.7
    assert report.f1_l1_avg >= 0.7
    assert report.consistency_pct >= 99.0


def test_joao_levels_strong():
    report = run_quality(InProcessCore(), DEFAULT_CORPUS)
    joao = next(i for i in report.items if i.id == "joao-1-1-5")
    assert joao.l1.f1 >= 0.9
    assert joao.l3.f1 >= 0.9
    assert joao.l1.needles_ok and joao.l3.needles_ok
    assert joao.floors_ok
