"""Legacy v2 shim — wraps Logos Core; do not use as a second engine."""

from __future__ import annotations

import warnings
from typing import Dict

from logos_core.api import expand as core_expand
from logos_core.api import extract
from logos_core.api import render as core_render
from logos_core.index import all_symbols

warnings.warn(
    "semantic_compressor is a legacy v2 shim; use logos_core.extract/render/expand",
    DeprecationWarning,
    stacklevel=2,
)

# Compatibility export: v3 symbols flattened to the old dict shape
SYMBOLS: Dict[str, Dict[str, str]] = {
    sid: {
        "name": meta.name,
        "definition": meta.definition,
        "expand": meta.expand,
        "category": meta.category,
    }
    for sid, meta in all_symbols().items()
}


def compress(text: str) -> str:
    """Deprecated: prefer logos_core.extract + logos_core.render."""
    canonical = extract(text)
    if not canonical.nodes:
        return f"[Nenhuma compressão forte detectada]\n\nTexto original:\n{text.strip()}"
    return core_render(canonical, 3)


def expand(symbolic: str) -> str:
    """Deprecated: prefer logos_core.expand on a CanonicalRepresentation.

    Best-effort: if the string looks like source prose, extract then expand;
    otherwise try to gloss known symbols in the string.
    """
    try:
        canonical = extract(symbolic)
        if canonical.nodes and canonical.coverage.matched_ratio > 0.05:
            return core_expand(canonical)
    except Exception:
        pass
    text = symbolic
    for symbol in sorted(SYMBOLS.keys(), key=len, reverse=True):
        if symbol in text:
            text = text.replace(symbol, SYMBOLS[symbol]["expand"])
    return text.strip()


def list_symbols(category: str = None) -> None:
    print("\nÍNDICE DE SÍMBOLOS v3 (via Logos Core)")
    print("=" * 70)
    current_cat = None
    for symbol, info in SYMBOLS.items():
        cat = info.get("category", "")
        if category and cat != category:
            continue
        if cat != current_cat:
            current_cat = cat
            print(f"\n[{cat.upper()}]")
        print(f"  {symbol:6} | {info['name']:<28} | {info['definition']}")
    print()


def get_symbols_by_category(category: str) -> Dict[str, Dict[str, str]]:
    return {k: v for k, v in SYMBOLS.items() if v.get("category") == category}


def main() -> None:
    from logos_core.cli import main as logos_main

    raise SystemExit(logos_main())


if __name__ == "__main__":
    main()
