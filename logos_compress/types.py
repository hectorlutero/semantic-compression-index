"""Compress result types."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from logos_core.types import CanonicalRepresentation


@dataclass
class CompressMetrics:
    source_chars: int
    compressed_chars: int
    source_tokens_est: int
    compressed_tokens_est: int
    reduction_ratio: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CompressResult:
    canonical: CanonicalRepresentation
    level1: str
    metrics: CompressMetrics
    expand_preview: str
    level3: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "canonical": self.canonical.to_dict(),
            "level1": self.level1,
            "level3": self.level3,
            "metrics": self.metrics.to_dict(),
            "expand_preview": self.expand_preview,
            # Back-compat shape for HTTP / web clients
            "renders": {
                "1": self.level1,
                "3": self.level3,
            },
            "expand": self.expand_preview,
        }
