"""Thin FastAPI adapter for Logos Core (secondary transport seam)."""

from __future__ import annotations

from typing import Any, Literal, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from logos_core.api import describe_symbol, expand, extract, render
from logos_core.engine import CoreError
from logos_compress import compress, prompt_pack

Level = Literal[1, 2, 3]


class ExtractRequest(BaseModel):
    text: str
    options: Optional[dict[str, Any]] = None


class RenderRequest(BaseModel):
    canonical: dict[str, Any]
    level: Level = 1


class ExpandRequest(BaseModel):
    canonical: dict[str, Any]


class DescribeRequest(BaseModel):
    symbol_id: str = Field(..., min_length=1)


def _canonical_from_dict(data: dict[str, Any]):
    """Rebuild CanonicalRepresentation from JSON (web client round-trip)."""
    from logos_core.types import (
        CanonicalEdge,
        CanonicalNode,
        CanonicalRepresentation,
        Coverage,
        ModalTag,
        Span,
    )

    nodes = []
    for n in data.get("nodes", []):
        span = None
        if n.get("span"):
            span = Span(start=n["span"]["start"], end=n["span"]["end"])
        modal = None
        if n.get("modal"):
            modal = ModalTag(system=n["modal"]["system"], operator=n["modal"]["operator"])
        nodes.append(
            CanonicalNode(
                symbol=n["symbol"],
                macro=n.get("macro"),
                category=n.get("category"),
                args=list(n.get("args") or []),
                span=span,
                modal=modal,
                gloss=n.get("gloss"),
            )
        )
    edges = [
        CanonicalEdge(op=e["op"], left=e["left"], right=e["right"])
        for e in data.get("edges", [])
    ]
    cov = data.get("coverage") or {}
    unmatched = [
        Span(start=s["start"], end=s["end"]) for s in cov.get("unmatched_spans", [])
    ]
    coverage = Coverage(
        matched_ratio=float(cov.get("matched_ratio", 0.0)),
        unmatched_spans=unmatched,
        matched_chars=int(cov.get("matched_chars", 0)),
        total_chars=int(cov.get("total_chars", 0)),
    )
    return CanonicalRepresentation(
        source_text=data.get("source_text", ""),
        version="v3",
        nodes=nodes,
        edges=edges,
        coverage=coverage,
        renders=dict(data.get("renders") or {}),
    )


def create_app() -> FastAPI:
    app = FastAPI(title="Logos Core HTTP Adapter", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "seam": "logos-core"}

    @app.post("/v1/extract")
    def api_extract(body: ExtractRequest) -> dict[str, Any]:
        try:
            canonical = extract(body.text, body.options)
        except CoreError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return canonical.to_dict()

    @app.post("/v1/render")
    def api_render(body: RenderRequest) -> dict[str, Any]:
        try:
            canonical = _canonical_from_dict(body.canonical)
            text = render(canonical, body.level)
        except (CoreError, KeyError, TypeError, ValueError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return {"level": body.level, "text": text}

    @app.post("/v1/expand")
    def api_expand(body: ExpandRequest) -> dict[str, Any]:
        try:
            canonical = _canonical_from_dict(body.canonical)
            text = expand(canonical)
        except (CoreError, KeyError, TypeError, ValueError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return {"text": text}

    @app.post("/v1/describe_symbol")
    def api_describe(body: DescribeRequest) -> dict[str, Any]:
        try:
            meta = describe_symbol(body.symbol_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        return meta.__dict__

    @app.post("/v1/compress")
    def api_compress(body: ExtractRequest) -> dict[str, Any]:
        """Thin adapter over LogosCompress (consumes Core; adds metrics)."""
        try:
            result = compress(body.text, body.options)
        except CoreError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        payload = result.to_dict()
        # Ensure L2 present for web clients that expect three levels
        payload["renders"]["2"] = render(result.canonical, 2)
        payload["prompt_pack"] = prompt_pack(result)
        return payload

    return app


app = create_app()


def main() -> None:
    import uvicorn

    uvicorn.run("logos_http.app:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    main()
