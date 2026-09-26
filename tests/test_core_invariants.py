"""Core seam invariants (#3–#5) — extract / render / expand / describe_symbol only.

Spec: empty/malformed rejected; source_text preserved; modals tagged;
partial miss never silent success; edges/spans observable on canonical form.
"""

from __future__ import annotations

import pytest

from logos_core import CoreError, describe_symbol, expand, extract, render

JOAO = """No princípio era o Verbo, e o Verbo estava com Deus, e o Verbo era Deus.
Ele estava no princípio com Deus.
Todas as coisas foram feitas por ele, e sem ele nada do que foi feito se fez.
Nele estava a vida, e a vida era a luz dos homens.
A luz resplandece nas trevas, e as trevas não prevaleceram contra ela."""

LEGAL = (
    "O contratante é obrigado a cumprir o prazo. É proibido ceder o contrato sem "
    "autorização. É permitido solicitar prorrogação salvo se houver justa causa. "
    "Se houver atraso, então aplica-se multa sob pena de rescisão."
)

SCI = (
    "A hipótese inicial foi testada pelo método experimental. A evidência empírica "
    "observada sustenta a tese; portanto, conclui-se que o modelo é adequado. "
    "Sabe-se que o resultado é replicável."
)


def test_source_text_preserved_exactly():
    text = "é necessário que o sistema funcione"
    c = extract(text)
    assert c.source_text == text


def test_malformed_options_rejected():
    with pytest.raises(CoreError):
        extract("texto válido", options="not-a-dict")  # type: ignore[arg-type]


def test_invalid_render_level_rejected():
    c = extract("é obrigado a cumprir o prazo")
    with pytest.raises(CoreError):
        render(c, 4)  # type: ignore[arg-type]


def test_matched_nodes_carry_spans():
    c = extract("é necessário que o sistema funcione")
    assert c.nodes
    for n in c.nodes:
        assert n.span is not None
        assert 0 <= n.span.start < n.span.end <= len(c.source_text)


def test_alethic_modal_tagged():
    c = extract("é necessário que o sistema funcione")
    nec = [n for n in c.nodes if n.symbol == "Nec"]
    assert nec
    assert nec[0].modal is not None
    assert nec[0].modal.system == "alethic"
    assert nec[0].macro == "MODAL"


def test_epistemic_modal_tagged():
    c = extract(SCI)
    k_nodes = [n for n in c.nodes if n.symbol == "K"]
    assert k_nodes
    assert k_nodes[0].modal is not None
    assert k_nodes[0].modal.system == "epistemic"


def test_deontic_and_conditional_modals_tagged():
    c = extract(LEGAL)
    systems = {n.modal.system for n in c.nodes if n.modal}
    assert "deontic" in systems
    assert "conditional" in systems
    assert {n.symbol for n in c.nodes} >= {"Obl", "Cond"}


def test_joao_canonical_has_edges():
    c = extract(JOAO)
    assert c.edges, "narrative seed must expose composition edges on the canonical form"
    ops = {e.op for e in c.edges}
    assert "∧" in ops
    assert "vs" in ops
    # Edge indices must point at real nodes
    for e in c.edges:
        assert 0 <= e.left < len(c.nodes)
        assert 0 <= e.right < len(c.nodes)


def test_expand_reuses_same_canonical():
    c = extract(JOAO)
    prose = expand(c)
    assert isinstance(prose, str) and prose.strip()
    # Approximate expand should reflect known seed operators, not echo raw João alone
    assert prose != c.source_text
    assert "e" in prose.lower() or "oposição" in prose.lower()


def test_partial_extraction_keeps_coverage_honest():
    c = extract("xyz nonsense e é obrigado a cumprir o prazo mais lixo qq")
    assert any(n.symbol == "Obl" for n in c.nodes)
    assert 0.0 < c.coverage.matched_ratio < 1.0
    assert c.coverage.unmatched_spans


def test_describe_symbol_unknown_raises():
    with pytest.raises(KeyError):
        describe_symbol("NOT_A_SYMBOL_XYZ")


def test_same_extract_feeds_all_render_levels():
    c = extract(JOAO)
    r1, r2, r3 = render(c, 1), render(c, 2), render(c, 3)
    assert "BE(" in r1 and "RELATE(" in r1 and "DYN(" in r1
    assert ":" in r2
    assert "Γ" in r3 or "Σ" in r3
    assert c.renders["1"] == r1
    assert c.renders["2"] == r2
    assert c.renders["3"] == r3
