"""Fase 2 #15 — LogosCompress seam (consumes Core only)."""

from __future__ import annotations

from logos_core import extract
from logos_compress import compress, compress_canonical, CompressResult

SAMPLE = (
    "Maria transformou-se após a crise. Ela estava com João no começo. "
    "A luz da esperança enfrentou as trevas do medo."
)


def test_compress_returns_level1_and_metrics():
    result = compress(SAMPLE)
    assert isinstance(result, CompressResult)
    assert result.level1.strip()
    assert any(m in result.level1 for m in ("BE(", "RELATE(", "DYN("))
    assert result.metrics.source_chars == len(SAMPLE)
    assert result.metrics.compressed_chars == len(result.level1)
    assert result.metrics.source_tokens_est > 0
    assert result.metrics.compressed_tokens_est > 0
    assert result.metrics.reduction_ratio < 1.0
    assert result.expand_preview.strip()
    assert result.canonical.nodes


def test_compress_canonical_reuses_extract_once():
    canonical = extract(SAMPLE)
    result = compress_canonical(canonical)
    assert result.canonical is canonical or result.canonical.source_text == SAMPLE
    assert result.level1 == compress(SAMPLE).level1


def test_compress_does_not_expose_core_internals():
    import logos_compress as lc

    assert callable(lc.compress)
    assert callable(lc.compress_canonical)
    assert not hasattr(lc, "LogosEngine")
    assert not hasattr(lc, "_ATOMIC_RULES")
