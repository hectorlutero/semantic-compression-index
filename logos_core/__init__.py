"""Logos Core — public seam only: extract / render / expand / describe_symbol."""

from logos_core.engine import CoreError
from logos_core.interface import CoreInterface, InProcessCore
from logos_core.types import (
    CanonicalEdge,
    CanonicalNode,
    CanonicalRepresentation,
    Coverage,
    ModalTag,
    Span,
    SymbolMeta,
)
from logos_core.api import extract, render, expand, describe_symbol

__all__ = [
    "CoreInterface",
    "InProcessCore",
    "CoreError",
    "CanonicalEdge",
    "CanonicalNode",
    "CanonicalRepresentation",
    "Coverage",
    "ModalTag",
    "Span",
    "SymbolMeta",
    "extract",
    "render",
    "expand",
    "describe_symbol",
]
