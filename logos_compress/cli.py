"""Minimal CLI for LogosCompress."""

from __future__ import annotations

import argparse
import json
import sys

from logos_compress import compress


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="logos-compress")
    parser.add_argument("text", nargs="?", help="Text to compress (or stdin)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    text = args.text if args.text is not None else sys.stdin.read()
    result = compress(text)
    if args.json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(result.level1)
        m = result.metrics
        print(
            f"\n# tokens_est {m.source_tokens_est} → {m.compressed_tokens_est} "
            f"(ratio={m.reduction_ratio:.3f})",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
