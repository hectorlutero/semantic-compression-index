"""Benchmark suite tests (#7)."""

from __future__ import annotations

from logos_bench import run_benchmarks
from logos_bench.runner import DEFAULT_BASELINE, DEFAULT_CORPUS
from logos_core import InProcessCore


def test_benchmarks_report_shape():
    report = run_benchmarks(InProcessCore(), DEFAULT_CORPUS, baseline=DEFAULT_BASELINE, repeats=2)
    assert report.latency_p50_ms >= 0
    assert report.latency_p95_ms >= report.latency_p50_ms
    assert 0 <= report.compression_ratio_avg
    assert 0 <= report.symbol_coverage_avg <= 1
    assert report.domain_breakdown
    domains = {d.domain for d in report.domain_breakdown}
    assert "narrativa" in domains
    assert "jurídico" in domains
    assert "científico" in domains
