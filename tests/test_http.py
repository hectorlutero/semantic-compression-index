"""HTTP adapter tests (#8)."""

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


def test_http_rejects_empty():
    client = TestClient(create_app())
    r = client.post("/v1/extract", json={"text": ""})
    assert r.status_code == 400


def test_http_describe_symbol():
    client = TestClient(create_app())
    r = client.post("/v1/describe_symbol", json={"symbol_id": "Obl"})
    assert r.status_code == 200
    assert r.json()["macro"] == "MODAL"
