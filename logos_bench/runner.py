"""Benchmark runner — in-process Core only (no HTTP noise)."""

from __future__ import annotations

import argparse
import json
import statistics
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Optional

from logos_core.interface import CoreInterface, InProcessCore

DEFAULT_CORPUS = Path(__file__).parent / "corpus" / "v1.json"
DEFAULT_BASELINE = Path(__file__).parent / "baselines" / "v1.json"


@dataclass
class ItemMetrics:
    id: str
    domain: str
    latency_ms: float
    compression_ratio: float
    symbol_coverage: float
    matched_ratio: float


@dataclass
class DomainBreakdown:
    domain: str
    count: int
    latency_p50_ms: float
    compression_ratio_avg: float
    symbol_coverage_avg: float


@dataclass
class BenchReport:
    latency_p50_ms: float
    latency_p95_ms: float
    compression_ratio_avg: float
    symbol_coverage_avg: float
    domain_breakdown: list[DomainBreakdown]
    items: list[ItemMetrics] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    failed_thresholds: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failed_thresholds


def _percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    if len(values) == 1:
        return values[0]
    ordered = sorted(values)
    k = (len(ordered) - 1) * (p / 100.0)
    f = int(k)
    c = min(f + 1, len(ordered) - 1)
    if f == c:
        return ordered[f]
    return ordered[f] + (ordered[c] - ordered[f]) * (k - f)


def run_benchmarks(
    core: CoreInterface,
    corpus: str | Path | list[dict[str, Any]],
    baseline: Optional[str | Path] = None,
    repeats: int = 5,
) -> BenchReport:
    if isinstance(corpus, (str, Path)):
        items = json.loads(Path(corpus).read_text(encoding="utf-8"))
    else:
        items = corpus

    baseline_cfg: dict[str, Any] = {}
    if baseline is None:
        baseline = DEFAULT_BASELINE
    if Path(baseline).exists():
        baseline_cfg = json.loads(Path(baseline).read_text(encoding="utf-8"))

    metrics: list[ItemMetrics] = []
    for item in items:
        text = item["text"]
        gold = set(item.get("gold_symbols", []))
        times: list[float] = []
        last_canonical = None
        last_render = ""
        for _ in range(max(1, repeats)):
            t0 = time.perf_counter()
            canonical = core.extract(text)
            rendered = core.render(canonical, 1)
            t1 = time.perf_counter()
            times.append((t1 - t0) * 1000.0)
            last_canonical = canonical
            last_render = rendered

        assert last_canonical is not None
        found = {n.symbol for n in last_canonical.nodes}
        coverage = (len(found & gold) / len(gold)) if gold else 0.0
        src_len = max(len(text), 1)
        ratio = len(last_render) / src_len
        metrics.append(
            ItemMetrics(
                id=item["id"],
                domain=item.get("domain", ""),
                latency_ms=statistics.median(times),
                compression_ratio=ratio,
                symbol_coverage=coverage,
                matched_ratio=last_canonical.coverage.matched_ratio,
            )
        )

    latencies = [m.latency_ms for m in metrics]
    report = BenchReport(
        latency_p50_ms=_percentile(latencies, 50),
        latency_p95_ms=_percentile(latencies, 95),
        compression_ratio_avg=(
            statistics.mean([m.compression_ratio for m in metrics]) if metrics else 0.0
        ),
        symbol_coverage_avg=(
            statistics.mean([m.symbol_coverage for m in metrics]) if metrics else 0.0
        ),
        domain_breakdown=_domain_breakdown(metrics),
        items=metrics,
    )

    _apply_thresholds(report, baseline_cfg)
    return report


def _domain_breakdown(metrics: list[ItemMetrics]) -> list[DomainBreakdown]:
    by_domain: dict[str, list[ItemMetrics]] = {}
    for m in metrics:
        by_domain.setdefault(m.domain or "unknown", []).append(m)
    out: list[DomainBreakdown] = []
    for domain, rows in by_domain.items():
        out.append(
            DomainBreakdown(
                domain=domain,
                count=len(rows),
                latency_p50_ms=_percentile([r.latency_ms for r in rows], 50),
                compression_ratio_avg=statistics.mean([r.compression_ratio for r in rows]),
                symbol_coverage_avg=statistics.mean([r.symbol_coverage for r in rows]),
            )
        )
    return out


def _apply_thresholds(report: BenchReport, cfg: dict[str, Any]) -> None:
    if not cfg:
        return
    fail = bool(cfg.get("fail_on_regression", False))
    warn = bool(cfg.get("warn_on_regression", True))

    checks = [
        ("latency_p95_ms_max", report.latency_p95_ms, "gt"),
        ("compression_ratio_min", report.compression_ratio_avg, "lt"),
        ("symbol_coverage_min", report.symbol_coverage_avg, "lt"),
    ]
    for key, actual, mode in checks:
        if key not in cfg:
            continue
        threshold = float(cfg[key])
        bad = (actual > threshold) if mode == "gt" else (actual < threshold)
        if not bad:
            continue
        msg = f"{key}: actual={actual:.4f} threshold={threshold:.4f}"
        if fail:
            report.failed_thresholds.append(msg)
        elif warn:
            report.warnings.append(msg)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="logos-bench")
    parser.add_argument("--corpus", default=str(DEFAULT_CORPUS))
    parser.add_argument("--baseline", default=str(DEFAULT_BASELINE))
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    report = run_benchmarks(
        InProcessCore(),
        args.corpus,
        baseline=args.baseline,
        repeats=args.repeats,
    )
    payload = asdict(report)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(
            f"latency p50={report.latency_p50_ms:.2f}ms p95={report.latency_p95_ms:.2f}ms"
        )
        print(f"compression_ratio_avg={report.compression_ratio_avg:.3f}")
        print(f"symbol_coverage_avg={report.symbol_coverage_avg:.3f}")
        for d in report.domain_breakdown:
            print(
                f"  [{d.domain}] n={d.count} p50={d.latency_p50_ms:.2f}ms "
                f"ratio={d.compression_ratio_avg:.3f} cov={d.symbol_coverage_avg:.3f}"
            )
        for w in report.warnings:
            print(f"WARN: {w}")
        for f in report.failed_thresholds:
            print(f"FAIL: {f}")
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
