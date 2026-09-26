"""CoreInterface protocol and in-process adapter."""

from __future__ import annotations

from typing import Any, Optional, Protocol, runtime_checkable

from logos_core.types import CanonicalRepresentation, Level, SymbolMeta


@runtime_checkable
class CoreInterface(Protocol):
    def extract(
        self, text: str, options: Optional[dict[str, Any]] = None
    ) -> CanonicalRepresentation: ...

    def render(self, canonical: CanonicalRepresentation, level: Level) -> str: ...

    def expand(self, canonical: CanonicalRepresentation) -> str: ...

    def describe_symbol(self, symbol_id: str) -> SymbolMeta: ...


class InProcessCore:
    """Thin in-process adapter (tests, evals, benchmarks, CLI)."""

    def extract(
        self, text: str, options: Optional[dict[str, Any]] = None
    ) -> CanonicalRepresentation:
        from logos_core.api import extract

        return extract(text, options)

    def render(self, canonical: CanonicalRepresentation, level: Level) -> str:
        from logos_core.api import render

        return render(canonical, level)

    def expand(self, canonical: CanonicalRepresentation) -> str:
        from logos_core.api import expand

        return expand(canonical)

    def describe_symbol(self, symbol_id: str) -> SymbolMeta:
        from logos_core.api import describe_symbol

        return describe_symbol(symbol_id)
