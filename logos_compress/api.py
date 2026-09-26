"""LogosCompress public interface — consumes Logos Core only."""

from __future__ import annotations

import re
from typing import Any, Optional

from logos_core.interface import CoreInterface, InProcessCore
from logos_core.types import CanonicalRepresentation

from logos_compress.types import CompressMetrics, CompressResult

# Deterministic whitespace/punctuation token estimate (not a model tokenizer).
_TOKEN_RE = re.compile(r"\S+")


def estimate_tokens(text: str) -> int:
    """Estimate token count by non-whitespace runs. Documented as an estimate."""
    if not text:
        return 0
    return len(_TOKEN_RE.findall(text))


def _metrics(source: str, compressed: str) -> CompressMetrics:
    src_tok = estimate_tokens(source)
    cmp_tok = estimate_tokens(compressed)
    ratio = (cmp_tok / src_tok) if src_tok else 0.0
    return CompressMetrics(
        source_chars=len(source),
        compressed_chars=len(compressed),
        source_tokens_est=src_tok,
        compressed_tokens_est=cmp_tok,
        reduction_ratio=ratio,
    )


def compress(
    text: str,
    options: Optional[dict[str, Any]] = None,
    *,
    core: Optional[CoreInterface] = None,
) -> CompressResult:
    engine = core or InProcessCore()
    canonical = engine.extract(text, options)
    return compress_canonical(canonical, core=engine)


def compress_canonical(
    canonical: CanonicalRepresentation,
    *,
    core: Optional[CoreInterface] = None,
) -> CompressResult:
    engine = core or InProcessCore()
    level1 = engine.render(canonical, 1)
    level3 = engine.render(canonical, 3)
    expand_preview = engine.expand(canonical)
    return CompressResult(
        canonical=canonical,
        level1=level1,
        level3=level3,
        metrics=_metrics(canonical.source_text, level1),
        expand_preview=expand_preview,
    )


def explain(
    result: CompressResult,
    *,
    core: Optional[CoreInterface] = None,
) -> list[dict[str, str]]:
    """Gloss symbols used in the compressed form via Core.describe_symbol."""
    engine = core or InProcessCore()
    seen: set[str] = set()
    out: list[dict[str, str]] = []
    for node in result.canonical.nodes:
        if node.symbol in seen:
            continue
        seen.add(node.symbol)
        try:
            meta = engine.describe_symbol(node.symbol)
        except KeyError:
            continue
        out.append(
            {
                "symbol_id": meta.symbol_id,
                "name": meta.name,
                "definition": meta.definition,
                "macro": meta.macro,
            }
        )
    return out


def prompt_pack(result: CompressResult, instruction: str = "") -> str:
    """Pure helper: embed Level-1 skeleton in a prompt string (no network)."""
    header = instruction.strip() or "Use the following symbolic skeleton as context:"
    return f"{header}\n\n{result.level1}\n"
