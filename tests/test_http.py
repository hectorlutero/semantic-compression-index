"""HTTP adapter tests — Core + Compress transport."""

from __future__ import annotations

from fastapi.testclient import TestClient

from logos_http import create_app

JOAO = (
    "No princípio era o Verbo, e o Verbo estava com Deus, e o Verbo era Deus. "
    "A luz resplandece nas trevas, e as trevas não prevaleceram contra ela."
)


def test_http_extract_and_compress():
    client = TestClient(create_app())
    r = client.get("/health")
    assert r.status_code == 200

    r = client.post("/v1/extract", json={"text": JOAO})
    assert r.status_code == 200
    data = r.json()
    assert data["version"] == "v3"
    assert data["nodes"]

    r = client.post("/v1/compress", json={"text": JOAO})
    assert r.status_code == 200
    payload = r.json()
    assert payload["renders"]["1"]
    assert payload["renders"]["3"]
    assert payload["expand"]
    assert payload["level1"] == payload["renders"]["1"]
    assert "metrics" in payload
    assert payload["metrics"]["source_tokens_est"] > 0
    assert payload["metrics"]["compressed_tokens_est"] > 0
    assert 0 <= payload["metrics"]["reduction_ratio"] <= 1.0
    assert payload["expand_preview"] == payload["expand"]
    assert "canonical" in payload
    assert payload["canonical"]["nodes"]


def test_http_compress_prompt_pack():
    """Compress endpoint includes pure prompt_pack (no network)."""
    client = TestClient(create_app())
    r = client.post("/v1/compress", json={"text": JOAO})
    assert r.status_code == 200
    payload = r.json()
    assert "prompt_pack" in payload
    assert payload["level1"] in payload["prompt_pack"]


def test_http_rejects_empty():
    client = TestClient(create_app())
    r = client.post("/v1/extract", json={"text": ""})
    assert r.status_code == 400


def test_http_describe_symbol():
    client = TestClient(create_app())
    r = client.post("/v1/describe_symbol", json={"symbol_id": "Obl"})
    assert r.status_code == 200
    assert r.json()["macro"] == "MODAL"
