"""Fase 1 #12 — open-prose densification via Core seam (BE / RELATE / DYN)."""

from __future__ import annotations

from logos_core import extract, render

# Unmarked narrative — must not rely on João/secular seed fixtures
OPEN_PROSE = (
    "Maria transformou-se após a crise. Ela estava com João no começo. "
    "A luz da esperança enfrentou as trevas do medo. "
    "Todos os cidadãos, para sempre, devem buscar o bem."
)


def test_open_prose_extracts_multiple_nodes():
    c = extract(OPEN_PROSE)
    assert len(c.nodes) >= 3
    assert c.coverage.matched_ratio > 0.0


def test_open_prose_covers_be_relate_dyn_macros():
    c = extract(OPEN_PROSE)
    macros = {n.macro for n in c.nodes if n.macro}
    # At least two of the three densification targets
    hit = macros & {"BE", "RELATE", "DYN"}
    assert len(hit) >= 2, f"expected ≥2 of BE/RELATE/DYN, got {macros}"


def test_open_prose_symbols_include_relation_or_dyn():
    c = extract(OPEN_PROSE)
    syms = {n.symbol for n in c.nodes}
    # Presence-with → Ρ; light/dark → Λ/Δ; transform → Τ; origin → Γ
    assert syms & {"Ρ", "Λ", "Δ", "Τ", "Γ"}, f"sparse symbols: {syms}"


def test_open_prose_render_l1_nonempty():
    c = extract(OPEN_PROSE)
    r1 = render(c, 1)
    assert r1.strip()
    assert any(m in r1 for m in ("BE(", "RELATE(", "DYN("))


def test_existence_and_agency_on_generic_prose():
    text = (
        "Existe uma força que age por meio da comunidade. "
        "No início havia esperança; a causa provocou mudança."
    )
    c = extract(text)
    syms = {n.symbol for n in c.nodes}
    assert len(c.nodes) >= 2
    assert syms & {"∃", "Γ", "Κ", "Caus", "Τ"}
