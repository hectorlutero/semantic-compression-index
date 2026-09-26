"""Smoke tests for Logos Core public interface (#3)."""

from __future__ import annotations

import pytest

from logos_core import CanonicalRepresentation, describe_symbol, expand, extract, render
from logos_core.engine import CoreError


def test_extract_rejects_empty():
    with pytest.raises(CoreError):
        extract("")
    with pytest.raises(CoreError):
        extract("   ")


def test_extract_returns_canonical_shape():
    result = extract("é necessário que o sistema funcione")
    assert isinstance(result, CanonicalRepresentation)
    assert result.version == "v3"
    assert result.source_text
    assert hasattr(result, "nodes")
    assert hasattr(result, "coverage")
    assert result.coverage.matched_ratio >= 0.0


def test_no_silent_empty_success_on_total_miss():
    result = extract("xyzzy plugh foobar sem padrao conhecido qq")
    # May have zero nodes, but coverage must reflect miss (not pretend success)
    if not result.nodes:
        assert result.coverage.matched_ratio == 0.0
        assert result.coverage.unmatched_spans


def test_describe_symbol_from_v3_index():
    meta = describe_symbol("Obl")
    assert meta.symbol_id == "Obl"
    assert meta.macro == "MODAL"
    assert meta.category == "modalidade"
    assert meta.definition


def test_render_and_expand_from_same_canonical():
    c = extract("é obrigado a cumprir o contrato")
    assert c.nodes
    r1 = render(c, 1)
    r3 = render(c, 3)
    assert "MODAL" in r1 or "Obl" in r3
    prose = expand(c)
    assert isinstance(prose, str) and prose.strip()


def test_public_surface_exports():
    import logos_core as core

    assert callable(core.extract)
    assert callable(core.render)
    assert callable(core.expand)
    assert callable(core.describe_symbol)
    # No public parser/index seam
    assert not hasattr(core, "parse")
    assert not hasattr(core, "load_index")
