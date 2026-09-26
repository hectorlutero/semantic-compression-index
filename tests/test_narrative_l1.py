"""Narrative L1 tests (#4) — Core seam only."""

from __future__ import annotations

from logos_core import extract, render

JOAO = """No princípio era o Verbo, e o Verbo estava com Deus, e o Verbo era Deus.
Ele estava no princípio com Deus.
Todas as coisas foram feitas por ele, e sem ele nada do que foi feito se fez.
Nele estava a vida, e a vida era a luz dos homens.
A luz resplandece nas trevas, e as trevas não prevaleceram contra ela."""


def test_joao_extract_has_l1_macros():
    c = extract(JOAO)
    macros = {n.macro for n in c.nodes if n.macro}
    assert "BE" in macros
    assert "RELATE" in macros
    assert "DYN" in macros
    assert c.coverage.matched_ratio > 0.0


def test_joao_render_l1_derived_from_canonical():
    c = extract(JOAO)
    r1 = render(c, 1)
    assert "BE(" in r1
    assert "RELATE(" in r1
    assert "DYN(Λ vs Δ" in r1
    # Cached renders stay consistent with live render
    assert c.renders.get("1") == r1


def test_coverage_not_silent_total_miss():
    c = extract(JOAO)
    assert c.nodes
    assert c.coverage.matched_chars > 0
