"""Acervo bridge — txt → draft gold (sem inventar acervo)."""

from __future__ import annotations

import json

from logos_eval.acervo_bridge import (
    DEFAULT_ACERVO,
    DEFAULT_SUITE,
    build_suite,
    draft_case,
    iter_txt,
    main,
    preview_one,
)
from logos_core import InProcessCore


def test_stub_txt_exists_and_is_tiny():
    stubs = list((DEFAULT_ACERVO / "stubs").glob("*.txt"))
    assert stubs, "esperado um stub mínimo em acervo/stubs/"
    text = stubs[0].read_text(encoding="utf-8")
    assert 0 < len(text) < 200


def test_iter_txt_skips_stubs_by_default():
    files = iter_txt(DEFAULT_ACERVO, include_stubs=False)
    assert len(files) >= 15, "esperado acervo real puxado sob acervo/<domínio>/"
    assert all("stubs" not in p.parts for p in files)
    with_stubs = iter_txt(DEFAULT_ACERVO, include_stubs=True)
    assert any(p.name == "principio-minimo.txt" for p in with_stubs)


def test_draft_case_from_stub_without_curated():
    stub = DEFAULT_ACERVO / "stubs" / "principio-minimo.txt"
    case = draft_case(stub, DEFAULT_ACERVO, curated=None)
    assert case["id"] == "acervo-principio-minimo"
    assert case["match_mode"] == "density"
    assert "No princípio" in case["input"]
    assert case["expect"]["min_nodes"] == 1


def test_build_suite_curated_only_requires_sidecars():
    files = iter_txt(DEFAULT_ACERVO, include_stubs=False)
    cases = build_suite(DEFAULT_ACERVO, files, curated_only=True)
    assert len(cases) >= 15
    assert all("expect" in c for c in cases)


def test_preview_uses_core_seam():
    preview = preview_one(InProcessCore(), "No princípio existia a ideia.")
    assert "render_l1" in preview
    assert "expand" in preview
    assert isinstance(preview["symbols"], list)


def test_gold_acervo_suite_has_curated_cases():
    cases = json.loads(DEFAULT_SUITE.read_text(encoding="utf-8"))
    assert len(cases) >= 15
    assert all("id" in c and "expect" in c for c in cases)


def test_preview_json_serializable():
    preview = preview_one(InProcessCore(), "No princípio existia a ideia.")
    json.dumps(preview)  # must not raise on Span


def test_compress_acervo_runs_on_stub():
    from logos_eval.acervo_bridge import compress_acervo

    stub = DEFAULT_ACERVO / "stubs" / "principio-minimo.txt"
    rows = compress_acervo(DEFAULT_ACERVO, [stub])
    assert len(rows) == 1
    assert "metrics" in rows[0]
    assert "level1" in rows[0]
    assert rows[0]["metrics"]["source_tokens_est"] >= 1


def test_cli_list_include_stubs(capsys):
    assert main(["--acervo", str(DEFAULT_ACERVO), "list", "--include-stubs"]) == 0
    out = capsys.readouterr().out
    assert "principio-minimo.txt" in out
