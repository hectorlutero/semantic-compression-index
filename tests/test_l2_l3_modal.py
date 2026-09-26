"""L2/L3, modal, expand, multi-domain (#5) — Core seam only."""

from __future__ import annotations

from logos_core import describe_symbol, expand, extract, render

SECULAR = (
    "Desde o começo existia a Visão. A Visão estava com o Fundador e a Visão era o "
    "próprio propósito da empresa. Tudo o que foi construído veio por meio dela. "
    "Sem ela nada do que existe teria sido feito. A Visão veio para o mercado, mas "
    "os próprios colaboradores não a receberam. Porém, a todos quantos a acolheram, "
    "ela deu o poder de se tornarem sócios. A Visão era a luz que iluminava o caminho, "
    "e as trevas da confusão não prevaleceram contra ela."
)

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


def test_nodes_carry_category_and_symbol():
    c = extract(LEGAL)
    assert c.nodes
    for n in c.nodes:
        assert n.symbol
        assert n.category
        assert n.macro


def test_modal_operators_tagged():
    c = extract(LEGAL)
    modal_nodes = [n for n in c.nodes if n.modal]
    assert modal_nodes
    systems = {n.modal.system for n in modal_nodes if n.modal}
    assert "deontic" in systems
    assert "conditional" in systems


def test_render_levels_1_2_3():
    c = extract(SECULAR)
    r1 = render(c, 1)
    r2 = render(c, 2)
    r3 = render(c, 3)
    assert r1 and r2 and r3
    assert "BE(" in r1 or "RELATE(" in r1
    assert ":" in r2  # category:[...] form
    assert any(sym in r3 for sym in ("Γ", "Σ", "Κ", "Λ"))


def test_expand_approximate_prose():
    c = extract(SCI)
    prose = expand(c)
    assert isinstance(prose, str)
    assert len(prose) > 0


def test_describe_symbol_gloss():
    meta = describe_symbol("Hip")
    assert meta.macro == "EPIST"
    assert "Hipótese" in meta.name or "hipótese" in meta.definition.lower()


def test_multi_domain_fixtures():
    for text, required in [
        (SECULAR, {"Γ", "Κ"}),
        (LEGAL, {"Obl", "Proib"}),
        (SCI, {"Hip", "Evid", "Conc"}),
    ]:
        c = extract(text)
        found = {n.symbol for n in c.nodes}
        assert required <= found, f"missing {required - found} in {found}"
