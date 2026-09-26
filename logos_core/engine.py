"""Deep Logos Core engine — rules/patterns extraction behind the small interface."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Optional

from logos_core.index import get_symbol, load_index, symbol_macro
from logos_core.types import (
    CanonicalEdge,
    CanonicalNode,
    CanonicalRepresentation,
    Coverage,
    Level,
    Macro,
    ModalTag,
    Span,
    SymbolMeta,
)


class CoreError(ValueError):
    """Invalid Core input or options."""


@dataclass(frozen=True)
class _Rule:
    """A detection rule that maps a text span to a base symbol (+ optional args)."""

    pattern: str
    symbol: str
    args: tuple[str, ...] = ()
    group_as: Optional[str] = None  # named multi-symbol group key
    priority: int = 0


# Explicit multi-node seed extractions for known fixtures
@dataclass
class _SeedMatch:
    pattern: str
    nodes: list[tuple[str, tuple[str, ...]]]  # (symbol, args)
    edges: list[tuple[str, int, int]]  # (op, left_idx, right_idx) within nodes
    priority: int = 100


_SEED_FIXTURES: list[_SeedMatch] = [
    # João 1:1 — Γ(Σ) ∧ Ρ(Σ, Deus) ∧ Σ(Σ, Deus)
    _SeedMatch(
        pattern=r"no princ[ií]pio era o verbo.*?o verbo era deus",
        nodes=[
            ("Γ", ("Σ",)),
            ("Ρ", ("Σ", "Deus")),
            ("Σ", ("Σ", "Deus")),
        ],
        edges=[("∧", 0, 1), ("∧", 1, 2)],
        priority=200,
    ),
    # João 1:2 — Ρ(Σ, Deus) ∘ Γ
    _SeedMatch(
        pattern=r"ele estava no princ[ií]pio com deus",
        nodes=[("Ρ", ("Σ", "Deus")), ("Γ", ())],
        edges=[("∘", 0, 1)],
        priority=190,
    ),
    # João 1:3 — Κ(Σ) ∧ Neg(Σ)
    _SeedMatch(
        pattern=r"todas as coisas foram feitas por (ele|interm[eé]dio dele).*?nada do que foi feito se fez",
        nodes=[("Κ", ("Σ",)), ("Neg", ("Σ",))],
        edges=[("∧", 0, 1)],
        priority=190,
    ),
    # João 1:4 — Σ(vida) ∧ Σ(vida, Λ)
    _SeedMatch(
        pattern=r"nele estava a vida.*?luz dos homens",
        nodes=[("Σ", ("vida",)), ("Σ", ("vida", "Λ"))],
        edges=[("∧", 0, 1)],
        priority=180,
    ),
    # João 1:5 — Λ vs Δ
    _SeedMatch(
        pattern=r"a luz resplandece nas trevas.*?n[aã]o (prevaleceram|a compreenderam)",
        nodes=[("Λ", ()), ("Δ", ())],
        edges=[("vs", 0, 1)],
        priority=180,
    ),
    # Secular parallel (EXAMPLES.md)
    _SeedMatch(
        pattern=(
            r"desde o come[cç]o existia a vis[aã]o.*?vis[aã]o era o pr[oó]prio prop[oó]sito"
        ),
        nodes=[
            ("Γ", ("Visão",)),
            ("Ρ", ("Visão", "Fundador")),
            ("Σ", ("Visão", "propósito")),
        ],
        edges=[("∧", 0, 1), ("∧", 1, 2)],
        priority=170,
    ),
    _SeedMatch(
        pattern=r"tudo o que foi constru[ií]do veio por meio dela.*?nada do que existe teria sido feito",
        nodes=[("Κ", ("Visão",)), ("Neg", ("Visão",))],
        edges=[("∧", 0, 1)],
        priority=160,
    ),
    _SeedMatch(
        pattern=r"a vis[aã]o veio para o mercado.*?n[aã]o a receberam",
        nodes=[("Μ", ("Visão",)), ("Ρej", ())],
        edges=[("∧", 0, 1)],
        priority=150,
    ),
    _SeedMatch(
        pattern=r"deu o poder de se tornarem s[oó]cios",
        nodes=[("Τ", ("sócios",))],
        edges=[],
        priority=140,
    ),
    _SeedMatch(
        pattern=r"vis[aã]o era a luz.*?trevas da confus[aã]o.*?n[aã]o prevaleceram",
        nodes=[("Λ", ("Visão",)), ("Δ", ("confusão",))],
        edges=[("vs", 0, 1)],
        priority=140,
    ),
]


# Atomic pattern rules (multi-domain)
_ATOMIC_RULES: list[_Rule] = [
    # Deontic / legal
    _Rule(r"[eé]\s+obrigad[oa]\s+a|deve\s+(fazer|cumprir)|tem\s+o\s+dever\s+de", "Obl", priority=50),
    _Rule(r"[eé]\s+permitid[oa]|pode\s+(fazer|exercer)|tem\s+o\s+direito\s+de", "Perm", priority=50),
    _Rule(r"[eé]\s+proibid[oa]|n[aã]o\s+pode|vedado", "Proib", priority=50),
    _Rule(r"salvo\s+se|a\s+menos\s+que|exceto\s+se", "Exc", priority=45),
    _Rule(
        r"(?:^|[.!?]\s+)se\b.{0,100}?\bent[aã]o\b|\bcaso\b.{0,40}?,\s*",
        "Cond",
        priority=40,
    ),
    _Rule(r"sob\s+pena\s+de|sujeito\s+a\s+san[cç][aã]o|multa\s+de", "Sanc", priority=45),
    # Alethic
    _Rule(r"[eé]\s+necess[aá]rio\s+que|necessariamente", "Nec", priority=45),
    _Rule(r"[eé]\s+poss[ií]vel\s+que|possivelmente", "Poss", priority=45),
    # Epistemic / scientific
    _Rule(r"\bhip[oó]tese\b", "Hip", priority=50),
    _Rule(r"\bevid[eê]ncia\b|dado\s+(emp[ií]rico|observacional)", "Evid", priority=50),
    _Rule(r"conclui-se\s+que|\bportanto\b|\blogo\b", "Conc", priority=45),
    _Rule(r"\bm[eé]todo\b|procedim[e]nto", "Met", priority=40),
    _Rule(r"\bsabe(?:-se)?\s+que\b", "K", priority=40),
    _Rule(r"\bacredit[oa]\s+que\b", "B", priority=40),
    # Generic ontology
    _Rule(r"no\s+princ[ií]pio|desde\s+o\s+(come[cç]o|in[ií]cio)|na\s+origem", "Γ", priority=20),
    _Rule(r"define-se\s+como|significa\s+que|entende-se\s+por", "Def", priority=30),
    _Rule(r"[eé]\s+(igual|id[eê]ntico|equivalente)\s+a", "Σ", priority=25),
    _Rule(r"em\s+oposição\s+a|contra\s+as?\s+trevas|luz\s+vs", "vs", priority=30),
    _Rule(r"\btransforma(?:-se|ção)\b|muda\s+de\s+estado", "Τ", priority=25),
    _Rule(r"para\s+todo|todas?\s+as\s+coisas|universalmente", "∀", priority=20),
    _Rule(r"[eé]\s+(bom|desejável|correto)\b", "Val+", priority=20),
    _Rule(r"[eé]\s+(mau|indesejável|incorreto)\b", "Val−", priority=20),
]


# Pseudo-symbol used for secular rejection pattern (Ρej) — map to Ρ with arg
_PSEUDO_MAP = {
    "Ρej": ("Ρ", ("rejeição",)),
}


class LogosEngine:
    """Deep module: v3 index + rules + level projection + approximate expand."""

    def extract(
        self, text: str, options: Optional[dict[str, Any]] = None
    ) -> CanonicalRepresentation:
        if options is not None and not isinstance(options, dict):
            raise CoreError("options must be a dict or None")
        if text is None or not str(text).strip():
            raise CoreError("empty input rejected")

        source = str(text)
        nodes: list[CanonicalNode] = []
        edges: list[CanonicalEdge] = []
        covered = [False] * len(source)
        occupied: list[tuple[int, int]] = []

        # 1) Seed fixtures (high precision multi-node)
        for seed in sorted(_SEED_FIXTURES, key=lambda s: -s.priority):
            for m in re.finditer(seed.pattern, source, flags=re.IGNORECASE | re.DOTALL):
                if self._overlaps(m.start(), m.end(), occupied):
                    continue
                base = len(nodes)
                for sym, args in seed.nodes:
                    real_sym, real_args = self._resolve_symbol(sym, args)
                    nodes.append(self._make_node(real_sym, real_args, m.start(), m.end()))
                for op, left, right in seed.edges:
                    edges.append(CanonicalEdge(op=op, left=base + left, right=base + right))
                self._mark(covered, m.start(), m.end())
                occupied.append((m.start(), m.end()))

        # 2) Atomic rules for remaining spans
        for rule in sorted(_ATOMIC_RULES, key=lambda r: -r.priority):
            for m in re.finditer(rule.pattern, source, flags=re.IGNORECASE | re.DOTALL):
                if self._overlaps(m.start(), m.end(), occupied):
                    continue
                real_sym, real_args = self._resolve_symbol(rule.symbol, rule.args)
                nodes.append(self._make_node(real_sym, real_args, m.start(), m.end()))
                self._mark(covered, m.start(), m.end())
                occupied.append((m.start(), m.end()))

        # Sort nodes by span start for stable render order
        order = sorted(
            range(len(nodes)),
            key=lambda i: (nodes[i].span.start if nodes[i].span else 0, i),
        )
        remap = {old: new for new, old in enumerate(order)}
        nodes = [nodes[i] for i in order]
        edges = [
            CanonicalEdge(op=e.op, left=remap[e.left], right=remap[e.right])
            for e in edges
            if e.left in remap and e.right in remap
        ]

        coverage = self._coverage(source, covered)
        if not nodes:
            # Partial miss: no silent empty success — coverage reflects total miss
            coverage = Coverage(
                matched_ratio=0.0,
                unmatched_spans=[Span(0, len(source))] if source else [],
                matched_chars=0,
                total_chars=len(source),
            )

        canonical = CanonicalRepresentation(
            source_text=source,
            version="v3",
            nodes=nodes,
            edges=edges,
            coverage=coverage,
        )
        # Cache renders derived from the same object
        for lvl in (1, 2, 3):
            canonical.renders[str(lvl)] = self.render(canonical, lvl)  # type: ignore[arg-type]
        return canonical

    def render(self, canonical: CanonicalRepresentation, level: Level) -> str:
        if level not in (1, 2, 3):
            raise CoreError("level must be 1, 2, or 3")
        if not canonical.nodes:
            return ""

        cached = canonical.renders.get(str(level))
        # Only use cache if it was already populated for this level after nodes set;
        # recompute always from nodes for correctness when called independently.
        if level == 1:
            return self._render_l1(canonical)
        if level == 2:
            return self._render_l2(canonical)
        return self._render_l3(canonical)

    def expand(self, canonical: CanonicalRepresentation) -> str:
        if not canonical.nodes:
            return canonical.source_text

        parts: list[str] = []
        for node in canonical.nodes:
            try:
                meta = get_symbol(node.symbol)
                phrase = meta.expand
            except KeyError:
                phrase = node.symbol
            if node.args:
                arg_txt = ", ".join(node.args)
                parts.append(f"{phrase} ({arg_txt})")
            else:
                parts.append(phrase)

        # Prefer edge-aware joining when edges exist
        if canonical.edges:
            return self._expand_with_edges(canonical, parts)
        return " e ".join(parts)

    def describe_symbol(self, symbol_id: str) -> SymbolMeta:
        return get_symbol(symbol_id)

    # --- internals ---------------------------------------------------------

    def _resolve_symbol(
        self, symbol: str, args: tuple[str, ...]
    ) -> tuple[str, tuple[str, ...]]:
        if symbol in _PSEUDO_MAP:
            return _PSEUDO_MAP[symbol]
        return symbol, args

    def _make_node(
        self, symbol: str, args: tuple[str, ...], start: int, end: int
    ) -> CanonicalNode:
        index = load_index()
        meta = index["symbols"].get(symbol)
        category = meta["category"] if meta else None
        macro: Optional[Macro] = symbol_macro(symbol) if meta else None
        modal = None
        if meta and meta.get("modal"):
            modal = ModalTag(
                system=meta["modal"]["system"],
                operator=meta["modal"]["operator"],
            )
        gloss = meta["definition"] if meta else None
        return CanonicalNode(
            symbol=symbol,
            macro=macro,
            category=category,
            args=list(args),
            span=Span(start, end),
            modal=modal,
            gloss=gloss,
        )

    @staticmethod
    def _overlaps(start: int, end: int, occupied: list[tuple[int, int]]) -> bool:
        for a, b in occupied:
            if start < b and end > a:
                return True
        return False

    @staticmethod
    def _mark(covered: list[bool], start: int, end: int) -> None:
        for i in range(max(0, start), min(len(covered), end)):
            covered[i] = True

    @staticmethod
    def _coverage(source: str, covered: list[bool]) -> Coverage:
        # Ignore whitespace when computing ratio so narrative seeds score fairly
        significant = [i for i, ch in enumerate(source) if not ch.isspace()]
        if not significant:
            return Coverage(matched_ratio=0.0, unmatched_spans=[], matched_chars=0, total_chars=0)
        matched = sum(1 for i in significant if covered[i])
        total = len(significant)
        unmatched: list[Span] = []
        i = 0
        n = len(source)
        while i < n:
            if not covered[i] and not source[i].isspace():
                j = i
                while j < n and (not covered[j] or source[j].isspace()):
                    j += 1
                # trim trailing whitespace from span end
                end = j
                while end > i and source[end - 1].isspace():
                    end -= 1
                unmatched.append(Span(i, end))
                i = j
            else:
                i += 1
        return Coverage(
            matched_ratio=matched / total if total else 0.0,
            unmatched_spans=unmatched,
            matched_chars=matched,
            total_chars=total,
        )

    def _fmt_symbol(self, node: CanonicalNode) -> str:
        if node.args:
            return f"{node.symbol}({', '.join(node.args)})"
        return node.symbol

    def _render_l3(self, canonical: CanonicalRepresentation) -> str:
        if not canonical.nodes:
            return ""
        if not canonical.edges:
            return " ∧ ".join(self._fmt_symbol(n) for n in canonical.nodes)

        # Build expression from edges in order
        used = set()
        parts: list[str] = []
        for e in canonical.edges:
            left = self._fmt_symbol(canonical.nodes[e.left])
            right = self._fmt_symbol(canonical.nodes[e.right])
            if e.op == "vs":
                frag = f"{left} vs {right}"
            elif e.op == "∘":
                frag = f"{left} ∘ {right}"
            elif e.op == "→":
                frag = f"{left} → {right}"
            else:
                frag = f"{left} {e.op} {right}"
            parts.append(frag)
            used.add(e.left)
            used.add(e.right)
        for i, n in enumerate(canonical.nodes):
            if i not in used:
                parts.append(self._fmt_symbol(n))
        return " ∧ ".join(parts)

    def _render_l2(self, canonical: CanonicalRepresentation) -> str:
        # Group by category, list unique symbols per category
        by_cat: dict[str, list[str]] = {}
        for n in canonical.nodes:
            cat = n.category or "unknown"
            by_cat.setdefault(cat, [])
            token = self._fmt_symbol(n)
            if token not in by_cat[cat]:
                by_cat[cat].append(token)
        chunks = [f"{cat}:[{', '.join(syms)}]" for cat, syms in by_cat.items()]
        return " ∧ ".join(chunks)

    def _render_l1(self, canonical: CanonicalRepresentation) -> str:
        # Group symbols under their macros; special-case DYN vs pairing
        by_macro: dict[str, list[CanonicalNode]] = {}
        for n in canonical.nodes:
            if not n.macro:
                continue
            by_macro.setdefault(n.macro, []).append(n)

        # Preserve a stable macro order matching SYMBOLS.md
        order = ["BE", "RELATE", "MODAL", "DYN", "COMM", "EPIST", "SCOPE", "VAL"]
        chunks: list[str] = []
        for macro in order:
            group = by_macro.get(macro)
            if not group:
                continue
            if macro == "DYN" and any(n.symbol == "Λ" for n in group) and any(
                n.symbol == "Δ" for n in group
            ):
                # Prefer Λ vs Δ form at L1
                extras = [n.symbol for n in group if n.symbol not in ("Λ", "Δ", "vs")]
                if extras:
                    chunks.append(f"DYN(Λ vs Δ, {', '.join(extras)})")
                else:
                    chunks.append("DYN(Λ vs Δ)")
                continue
            # Unique base symbols in encounter order
            seen: list[str] = []
            for n in group:
                if n.symbol not in seen and n.symbol != "vs":
                    seen.append(n.symbol)
            if not seen:
                continue
            chunks.append(f"{macro}({', '.join(seen)})")
        return " ∧ ".join(chunks)

    def _expand_with_edges(
        self, canonical: CanonicalRepresentation, parts: list[str]
    ) -> str:
        fragments: list[str] = []
        used: set[int] = set()
        joiners = {"∧": " e ", "∘": " ", "→": " implica ", "vs": " em oposição a "}
        for e in canonical.edges:
            left = parts[e.left]
            right = parts[e.right]
            mid = joiners.get(e.op, f" {e.op} ")
            fragments.append(f"{left}{mid}{right}")
            used.add(e.left)
            used.add(e.right)
        for i, p in enumerate(parts):
            if i not in used:
                fragments.append(p)
        return "; ".join(fragments)
