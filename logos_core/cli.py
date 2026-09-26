"""CLI for Logos Core — calls only the public Core seam."""

from __future__ import annotations

import argparse
import json
import sys

from logos_core.api import describe_symbol, expand, extract, render


JOAO = """No princípio era o Verbo, e o Verbo estava com Deus, e o Verbo era Deus.
Ele estava no princípio com Deus.
Todas as coisas foram feitas por ele, e sem ele nada do que foi feito se fez.
Nele estava a vida, e a vida era a luz dos homens.
A luz resplandece nas trevas, e as trevas não prevaleceram contra ela."""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="logos", description="Logos Core CLI")
    parser.add_argument("text", nargs="?", help="Text to extract (default: João 1:1-5 demo)")
    parser.add_argument("--level", type=int, choices=[1, 2, 3], default=1)
    parser.add_argument("--json", action="store_true", help="Print full canonical JSON")
    parser.add_argument("--expand", action="store_true", help="Also print approximate expand")
    parser.add_argument("--describe", metavar="SYMBOL", help="Describe a symbol and exit")
    args = parser.parse_args(argv)

    if args.describe:
        meta = describe_symbol(args.describe)
        print(json.dumps(meta.__dict__, ensure_ascii=False, indent=2))
        return 0

    text = args.text if args.text else JOAO
    canonical = extract(text)
    if args.json:
        print(json.dumps(canonical.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(render(canonical, args.level))  # type: ignore[arg-type]
        print(
            f"\n# coverage={canonical.coverage.matched_ratio:.2f} "
            f"nodes={len(canonical.nodes)} version={canonical.version}",
            file=sys.stderr,
        )
    if args.expand:
        print("--- expand ---")
        print(expand(canonical))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
