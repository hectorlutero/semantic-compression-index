"""Canonical representation and Core result types (v3)."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal, Optional


Macro = Literal["BE", "RELATE", "MODAL", "DYN", "COMM", "EPIST", "SCOPE", "VAL"]
Level = Literal[1, 2, 3]
ModalSystem = Literal["alethic", "deontic", "epistemic", "conditional"]


@dataclass
class Span:
    start: int
    end: int


@dataclass
class ModalTag:
    system: ModalSystem
    operator: str


@dataclass
class CanonicalNode:
    symbol: str
    macro: Optional[Macro] = None
    category: Optional[str] = None
    args: list[str] = field(default_factory=list)
    span: Optional[Span] = None
    modal: Optional[ModalTag] = None
    gloss: Optional[str] = None


@dataclass
class CanonicalEdge:
    op: str  # ∧ | → | vs | ¬ | ∘ | app
    left: int
    right: int


@dataclass
class Coverage:
    matched_ratio: float
    unmatched_spans: list[Span] = field(default_factory=list)
    matched_chars: int = 0
    total_chars: int = 0


@dataclass
class CanonicalRepresentation:
    source_text: str
    version: Literal["v3"]
    nodes: list[CanonicalNode]
    coverage: Coverage
    edges: list[CanonicalEdge] = field(default_factory=list)
    renders: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class SymbolMeta:
    symbol_id: str
    name: str
    definition: str
    category: str
    macro: Macro
    expand: str
    aliases: list[str] = field(default_factory=list)
