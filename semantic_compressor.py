#!/usr/bin/env python3
"""
Semantic Compression Index - Basic Compressor / Expander
=======================================================

Ferramenta experimental para comprimir e expandir textos
usando o sistema de símbolos agnósticos.

Uso básico:
    python semantic_compressor.py

Ou importe como módulo:
    from semantic_compressor import compress, expand, SYMBOLS
"""

from typing import Dict, List, Tuple
import re
import json
from pathlib import Path

# ============================================================
# ÍNDICE DE SÍMBOLOS (fonte única da verdade)
# ============================================================

SYMBOLS: Dict[str, Dict[str, str]] = {
    "Γ": {
        "name": "Origem / Princípio",
        "definition": "Existe desde o início, antes de tudo",
        "expand": "no princípio existia",
    },
    "Σ": {
        "name": "Identidade profunda",
        "definition": "A é B (essência ou natureza)",
        "expand": "era",
    },
    "Ρ": {
        "name": "Relação de presença",
        "definition": "X está com Y / junto de Y",
        "expand": "estava com",
    },
    "Κ": {
        "name": "Agência criadora",
        "definition": "Tudo (ou o essencial) foi feito por meio de X",
        "expand": "todas as coisas foram feitas por",
    },
    "Neg": {
        "name": "Negação universal",
        "definition": "Sem X, nada do que existe teria existido",
        "expand": "sem ele nada do que foi feito se fez",
    },
    "Λ": {
        "name": "Luz / Revelação",
        "definition": "Aquilo que ilumina, torna visível ou revela",
        "expand": "a luz",
    },
    "Δ": {
        "name": "Trevas / Oposição",
        "definition": "Aquilo que resiste, oculta ou não compreende",
        "expand": "as trevas",
    },
    "Μ": {
        "name": "Manifestação",
        "definition": "O que era eterno ou oculto se torna presente",
        "expand": "veio / se manifestou",
    },
    "Π": {
        "name": "Recepção",
        "definition": "Alguém acolhe / aceita / crê",
        "expand": "receberam / acolheram",
    },
    "Ρej": {
        "name": "Rejeição",
        "definition": "Os “seus” não acolhem",
        "expand": "os seus não o receberam",
    },
    "Τ": {
        "name": "Transformação de status",
        "definition": "Quem acolhe recebe novo estatuto",
        "expand": "deu-lhes o poder de se tornarem",
    },
    "Ω": {
        "name": "Testemunho",
        "definition": "Alguém ou algo aponta / dá testemunho",
        "expand": "deu testemunho",
    },
    "Ι": {
        "name": "Autodeclaração",
        "definition": "“Eu sou” + predicado",
        "expand": "eu sou",
    },
    "Η": {
        "name": "Hora / Momento decisivo",
        "definition": "O tempo marcado chega",
        "expand": "chegou a hora",
    },
    "Α": {
        "name": "Permanência",
        "definition": "Ficar / permanecer / habitar em relação",
        "expand": "permaneceu / habitou",
    },
    "Β": {
        "name": "Novo nascimento",
        "definition": "Nascer de novo / transformação radical",
        "expand": "nascer de novo",
    },
    "Φ": {
        "name": "Dom / Oferta",
        "definition": "Algo é dado gratuitamente",
        "expand": "foi dado",
    },
    "Ψ": {
        "name": "Conflito de compreensão",
        "definition": "Mal-entendido que revela verdade mais profunda",
        "expand": "não compreenderam",
    },
    "Ξ": {
        "name": "Exaltação",
        "definition": "Ser elevado (literal ou figurado)",
        "expand": "foi exaltado / levantado",
    },
    "Θ": {
        "name": "Amor como mandamento",
        "definition": "Amar da mesma forma que se foi amado",
        "expand": "amai-vos uns aos outros",
    },
}

# ============================================================
# REGRAS SIMPLES DE COMPRESSÃO (baseadas em padrões conhecidos)
# ============================================================

# Padrões de texto → símbolo (ordem importa: mais específicos primeiro)
COMPRESSION_PATTERNS: List[Tuple[str, str]] = [
    # João 1 específicos
    (r"no princ[ií]pio era o verbo.*?o verbo era deus", "Γ(Σ) ∧ Ρ(Σ, Deus) ∧ Σ(Σ, Deus)"),
    (r"ele estava no princ[ií]pio com deus", "Ρ(Σ, Deus) ∘ Γ"),
    (r"todas as coisas foram feitas por (ele|interm[eé]dio dele).*?nada do que foi feito se fez", "Κ(Σ) ∧ Neg(Σ)"),
    (r"nele estava a vida.*?luz dos homens", "Σ(vida) ∧ Σ(vida, Λ_homens)"),
    (r"a luz resplandece nas trevas.*?n[aã]o (prevaleceram|a compreenderam)", "Λ vs Δ (Δ não prevalece)"),
    # Genéricos
    (r"no princ[ií]pio|desde o (come[cç]o|in[ií]cio)", "Γ"),
    (r"estava com|junto de|com deus", "Ρ"),
    (r"era deus|era o pr[oó]prio", "Σ"),
    (r"todas as coisas foram feitas|tudo foi (criado|feito) por", "Κ"),
    (r"sem (ele|ela) nada", "Neg"),
    (r"a luz|luz dos", "Λ"),
    (r"as trevas|trevas", "Δ"),
    (r"n[aã]o (o |a )?receberam|n[aã]o acolheram", "Ρej"),
    (r"deu-lhes o poder de se tornarem|tornaram-se", "Τ"),
]


def compress(text: str) -> str:
    """
    Tenta comprimir um texto usando os padrões conhecidos.
    Retorna a versão simbólica (ainda experimental e limitada).
    """
    original = text.strip()
    result = original.lower()

    for pattern, symbol in COMPRESSION_PATTERNS:
        result = re.sub(pattern, symbol, result, flags=re.IGNORECASE | re.DOTALL)

    # Se quase não mudou, avisa
    if result.lower() == original.lower():
        return f"[Nenhuma compressão forte detectada]\n\nTexto original:\n{original}"

    return result


def expand(symbolic: str) -> str:
    """
    Expande uma expressão simbólica de volta para texto aproximado
    usando as definições do índice.
    """
    text = symbolic

    # Substituições simples (ordem importa)
    replacements = [
        ("Γ(Σ)", "No princípio era o Verbo"),
        ("Ρ(Σ, Deus)", "o Verbo estava com Deus"),
        ("Σ(Σ, Deus)", "o Verbo era Deus"),
        ("Ρ(Σ, Deus) ∘ Γ", "Ele estava no princípio com Deus"),
        ("Κ(Σ)", "Todas as coisas foram feitas por ele"),
        ("Neg(Σ)", "sem ele nada do que foi feito se fez"),
        ("Σ(vida)", "Nele estava a vida"),
        ("Σ(vida, Λ_homens)", "a vida era a luz dos homens"),
        ("Λ vs Δ (Δ não prevalece)", "A luz resplandece nas trevas, e as trevas não prevaleceram contra ela"),
        ("Λ vs Δ", "A luz resplandece nas trevas"),
        ("∧", ". "),
        ("∘", " "),
    ]

    for old, new in replacements:
        text = text.replace(old, new)

    # Expansão genérica dos símbolos restantes
    for symbol, info in SYMBOLS.items():
        if symbol in text:
            text = text.replace(symbol, info["expand"])

    return text.strip()


def list_symbols() -> None:
    """Imprime o índice de símbolos de forma legível."""
    print("\nÍNDICE DE SÍMBOLOS")
    print("=" * 60)
    for symbol, info in SYMBOLS.items():
        print(f"{symbol:6} | {info['name']:<25} | {info['definition']}")
    print()


def export_symbols_json(path: str = "symbols.json") -> None:
    """Exporta o índice de símbolos para um arquivo JSON."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(SYMBOLS, f, ensure_ascii=False, indent=2)
    print(f"Símbolos exportados para: {path}")


def import_text_from_file(filepath: str) -> str:
    """Importa texto de um arquivo."""
    return Path(filepath).read_text(encoding="utf-8")


def export_text_to_file(text: str, filepath: str) -> None:
    """Exporta texto para um arquivo."""
    Path(filepath).write_text(text, encoding="utf-8")
    print(f"Texto salvo em: {filepath}")


# ============================================================
# INTERFACE DE LINHA DE COMANDO SIMPLES
# ============================================================

def main():
    print("=" * 60)
    print("  Semantic Compression Index - Compressor Experimental")
    print("=" * 60)

    # Exemplo embutido: João 1:1-5
    joao_1_5 = """No princípio era o Verbo, e o Verbo estava com Deus, e o Verbo era Deus.
Ele estava no princípio com Deus.
Todas as coisas foram feitas por ele, e sem ele nada do que foi feito se fez.
Nele estava a vida, e a vida era a luz dos homens.
A luz resplandece nas trevas, e as trevas não prevaleceram contra ela."""

    print("\n1. Texto original (João 1:1-5):")
    print("-" * 40)
    print(joao_1_5)

    print("\n2. Versão comprimida:")
    print("-" * 40)
    compressed = compress(joao_1_5)
    print(compressed)

    print("\n3. Expansão de volta (aproximação):")
    print("-" * 40)
    expanded = expand(compressed)
    print(expanded)

    print("\n4. Lista de símbolos disponíveis:")
    list_symbols()

    # Exporta o índice
    export_symbols_json("symbols.json")

    print("\nDica: Você pode importar este módulo e usar:")
    print("  from semantic_compressor import compress, expand, SYMBOLS")
    print("  compress('seu texto aqui')")
    print("  expand('Γ(Σ) ∧ Ρ(Σ, Deus)')")


if __name__ == "__main__":
    main()
