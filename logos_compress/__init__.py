"""LogosCompress — deep module for Level-1 compression over Core."""

from logos_compress.api import compress, compress_canonical, explain, prompt_pack
from logos_compress.types import CompressMetrics, CompressResult

__all__ = [
    "compress",
    "compress_canonical",
    "explain",
    "prompt_pack",
    "CompressMetrics",
    "CompressResult",
]
