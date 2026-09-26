"""Public Core API — the only engine seam for v1."""

from __future__ import annotations

from typing import Any, Optional

from logos_core.engine import LogosEngine
from logos_core.types import CanonicalRepresentation, Level, SymbolMeta

_engine = LogosEngine()


def extract(text: str, options: Optional[dict[str, Any]] = None) -> CanonicalRepresentation:
    """Extract a v3 canonical representation from text."""
    return _engine.extract(text, options)


def render(canonical: CanonicalRepresentation, level: Level) -> str:
    """Render a canonical form at Level 1, 2, or 3."""
    return _engine.render(canonical, level)


def expand(canonical: CanonicalRepresentation) -> str:
    """Approximate prose expansion from a canonical form (not bit-exact)."""
    return _engine.expand(canonical)


def describe_symbol(symbol_id: str) -> SymbolMeta:
    """Read-only gloss metadata for a symbol id."""
    return _engine.describe_symbol(symbol_id)
