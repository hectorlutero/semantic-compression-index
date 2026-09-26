"""Fase 1 #13 — COMM / SCOPE / VAL via Core seam."""

from __future__ import annotations

from logos_core import extract, render

DIALOGIC = (
    "O professor disse aos alunos que a verdade importa. "
    "Eles perguntaram por quê. Ele respondeu com um argumento sólido. "
    "Afirmou que o princípio é justo. Em todas as épocas, para sempre, "
    "esse valor permanece."
)


def test_comm_macros_on_dialogue():
    c = extract(DIALOGIC)
    macros = {n.macro for n in c.nodes if n.macro}
    assert "COMM" in macros, f"missing COMM in {macros}"
    syms = {n.symbol for n in c.nodes}
    assert syms & {"Quest", "Resp", "Arg", "Ω"}, f"sparse COMM: {syms}"


def test_scope_and_val_on_dialogue():
    c = extract(DIALOGIC)
    macros = {n.macro for n in c.nodes if n.macro}
    assert "SCOPE" in macros or "VAL" in macros, f"macros={macros}"
    syms = {n.symbol for n in c.nodes}
    assert syms & {"∀", "Temp", "Θ", "Val+"}, f"sparse SCOPE/VAL: {syms}"


def test_dialogic_render_includes_comm_or_val():
    c = extract(DIALOGIC)
    r1 = render(c, 1)
    assert any(m in r1 for m in ("COMM(", "SCOPE(", "VAL(")), r1


def test_temporal_scope_markers():
    c = extract("Durante a crise e após a guerra, sempre houve esperança.")
    syms = {n.symbol for n in c.nodes}
    assert "Temp" in syms or "∃" in syms
    macros = {n.macro for n in c.nodes if n.macro}
    assert "SCOPE" in macros or "BE" in macros
