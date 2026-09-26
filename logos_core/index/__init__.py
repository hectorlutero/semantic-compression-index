"""Internal SYMBOLS v3 index — not a public seam."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from logos_core.types import Macro, SymbolMeta

_DATA_PATH = Path(__file__).parent / "data" / "symbols_v3.json"


@lru_cache(maxsize=1)
def load_index() -> dict[str, Any]:
    with _DATA_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def symbol_macro(symbol_id: str) -> Macro | None:
    index = load_index()
    sym = index["symbols"].get(symbol_id)
    if not sym:
        return None
    cat = sym["category"]
    return index["categories"][cat]["macro"]  # type: ignore[return-value]


def get_symbol(symbol_id: str) -> SymbolMeta:
    index = load_index()
    # Resolve aliases
    resolved = symbol_id
    if symbol_id not in index["symbols"]:
        for sid, meta in index["symbols"].items():
            if symbol_id in meta.get("aliases", []):
                resolved = sid
                break
        else:
            raise KeyError(f"Unknown symbol: {symbol_id}")

    meta = index["symbols"][resolved]
    cat = meta["category"]
    macro = index["categories"][cat]["macro"]
    return SymbolMeta(
        symbol_id=resolved,
        name=meta["name"],
        definition=meta["definition"],
        category=cat,
        macro=macro,  # type: ignore[arg-type]
        expand=meta["expand"],
        aliases=list(meta.get("aliases", [])),
    )


def all_symbols() -> dict[str, SymbolMeta]:
    index = load_index()
    return {sid: get_symbol(sid) for sid in index["symbols"]}
