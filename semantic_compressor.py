#!/usr/bin/env python3
"""
Semantic Compression Index - Compressor / Expander (v2)
=======================================================

Ferramenta experimental para comprimir e expandir textos
usando o sistema de símbolos agnósticos multidominio.

Suporta padrões de:
- Narrativa
- Diálogo
- Retórica
- Textos jurídicos
- Textos científicos

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
# ÍNDICE DE SÍMBOLOS v2 (fonte única da verdade)
# Agnóstico: narrativa | diálogo | retórica | jurídico | científico
# ============================================================

SYMBOLS: Dict[str, Dict[str, str]] = {
    # 1. Existência e Origem
    "Γ": {
        "name": "Origem / Princípio",
        "definition": "Algo existe desde o início ou é o ponto de partida",
        "expand": "no princípio / desde a origem",
        "category": "existência",
    },
    "∃": {
        "name": "Existência",
        "definition": "Algo existe / há",
        "expand": "existe / há",
        "category": "existência",
    },
    "∄": {
        "name": "Inexistência",
        "definition": "Algo não existe / não há",
        "expand": "não existe / não há",
        "category": "existência",
    },
    "Μ": {
        "name": "Manifestação",
        "definition": "O que estava oculto, potencial ou abstrato se torna presente",
        "expand": "se manifesta / torna-se presente",
        "category": "existência",
    },

    # 2. Identidade e Definição
    "Σ": {
        "name": "Identidade",
        "definition": "A é B (essência, natureza ou equivalência)",
        "expand": "é / trata-se de",
        "category": "identidade",
    },
    "Def": {
        "name": "Definição",
        "definition": "Para os fins deste contexto, X significa…",
        "expand": "define-se como / significa",
        "category": "identidade",
    },
    "≈": {
        "name": "Semelhança",
        "definition": "A é semelhante / análogo a B",
        "expand": "é semelhante a / análogo a",
        "category": "identidade",
    },
    "≠": {
        "name": "Diferença",
        "definition": "A não é B / distingue-se de B",
        "expand": "não é / distingue-se de",
        "category": "identidade",
    },

    # 3. Relação e Estrutura
    "Ρ": {
        "name": "Presença / Relação",
        "definition": "X está com / em relação a Y",
        "expand": "está com / em relação a",
        "category": "relação",
    },
    "∈": {
        "name": "Pertencimento",
        "definition": "X pertence a / faz parte de Y",
        "expand": "pertence a / faz parte de",
        "category": "relação",
    },
    "⊂": {
        "name": "Inclusão",
        "definition": "X está contido em Y",
        "expand": "está contido em",
        "category": "relação",
    },
    "Hier": {
        "name": "Hierarquia",
        "definition": "X está acima / subordinado a Y",
        "expand": "está hierarquicamente relacionado a",
        "category": "relação",
    },
    "Part": {
        "name": "Parte / Sujeito",
        "definition": "O agente, paciente ou participante da relação",
        "expand": "a parte / o sujeito",
        "category": "relação",
    },

    # 4. Agência e Causação
    "Κ": {
        "name": "Agência",
        "definition": "X age / é a causa ou o meio pelo qual algo ocorre",
        "expand": "age / é por meio de",
        "category": "agência",
    },
    "Caus": {
        "name": "Nexo causal",
        "definition": "A produz / provoca B",
        "expand": "causa / provoca",
        "category": "agência",
    },
    "Neg": {
        "name": "Negação de agência",
        "definition": "Sem X, B não ocorreria",
        "expand": "sem isso não ocorreria",
        "category": "agência",
    },
    "Obj": {
        "name": "Objeto",
        "definition": "Aquilo sobre o qual a ação ou norma incide",
        "expand": "o objeto / aquilo sobre o que incide",
        "category": "agência",
    },

    # 5. Modalidade
    "Obl": {
        "name": "Obrigação",
        "definition": "X deve fazer / deixar de fazer Y",
        "expand": "deve / é obrigado a",
        "category": "modalidade",
    },
    "Perm": {
        "name": "Permissão",
        "definition": "X pode / tem o direito de fazer Y",
        "expand": "pode / tem permissão para",
        "category": "modalidade",
    },
    "Proib": {
        "name": "Proibição",
        "definition": "X não pode fazer Y",
        "expand": "é proibido / não pode",
        "category": "modalidade",
    },
    "Nec": {
        "name": "Necessidade",
        "definition": "É necessário que…",
        "expand": "é necessário que",
        "category": "modalidade",
    },
    "Poss": {
        "name": "Possibilidade",
        "definition": "É possível que…",
        "expand": "é possível que",
        "category": "modalidade",
    },

    # 6. Condição, Consequência e Exceção
    "Cond": {
        "name": "Condição",
        "definition": "Se A, então B",
        "expand": "se … então",
        "category": "condição",
    },
    "Sanc": {
        "name": "Consequência / Sanção",
        "definition": "Se ocorrer A → segue-se B",
        "expand": "tem como consequência",
        "category": "condição",
    },
    "Exc": {
        "name": "Exceção",
        "definition": "Salvo se / a menos que",
        "expand": "salvo se / a menos que",
        "category": "condição",
    },
    "→": {
        "name": "Implicação",
        "definition": "A implica B",
        "expand": "implica",
        "category": "condição",
    },

    # 7. Oposição e Dualidade
    "Λ": {
        "name": "Polo positivo / Revelação",
        "definition": "O lado que revela, esclarece ou afirma",
        "expand": "o polo positivo / a revelação",
        "category": "oposição",
    },
    "Δ": {
        "name": "Polo negativo / Ocultamento",
        "definition": "O lado que oculta, resiste ou nega",
        "expand": "o polo negativo / o ocultamento",
        "category": "oposição",
    },
    "vs": {
        "name": "Oposição",
        "definition": "A está em tensão ou conflito com B",
        "expand": "em oposição a",
        "category": "oposição",
    },
    "¬": {
        "name": "Negação simples",
        "definition": "Não-A",
        "expand": "não",
        "category": "oposição",
    },

    # 8. Transformação e Mudança
    "Τ": {
        "name": "Transformação de status",
        "definition": "X muda de estado / recebe novo estatuto",
        "expand": "transforma-se / recebe novo estatuto",
        "category": "transformação",
    },
    "Β": {
        "name": "Transformação radical",
        "definition": "Mudança profunda ou renascimento",
        "expand": "transformação radical / renascimento",
        "category": "transformação",
    },
    "Δt": {
        "name": "Mudança no tempo",
        "definition": "Antes → Depois",
        "expand": "muda com o tempo",
        "category": "transformação",
    },

    # 9. Comunicação e Atos de Fala
    "Ω": {
        "name": "Testemunho / Afirmação",
        "definition": "Alguém declara, testemunha ou afirma",
        "expand": "afirma / testemunha",
        "category": "comunicação",
    },
    "Ι": {
        "name": "Autodeclaração",
        "definition": "“Eu sou / eu afirmo” + conteúdo",
        "expand": "eu sou / eu afirmo",
        "category": "comunicação",
    },
    "Quest": {
        "name": "Pergunta",
        "definition": "Interrogação / pedido de informação",
        "expand": "pergunta",
        "category": "comunicação",
    },
    "Resp": {
        "name": "Resposta",
        "definition": "Contestação ou réplica",
        "expand": "responde",
        "category": "comunicação",
    },
    "Arg": {
        "name": "Argumento",
        "definition": "Razão apresentada para sustentar uma tese",
        "expand": "argumenta / apresenta como razão",
        "category": "comunicação",
    },
    "Pers": {
        "name": "Persuasão",
        "definition": "Tentativa de convencer",
        "expand": "tenta persuadir",
        "category": "comunicação",
    },
    "Iron": {
        "name": "Ironia / Tensão retórica",
        "definition": "Dizer o contrário do que se quer enfatizar",
        "expand": "diz ironicamente",
        "category": "comunicação",
    },

    # 10. Evidência e Justificação
    "Evid": {
        "name": "Evidência",
        "definition": "Dado ou fato apresentado como suporte",
        "expand": "evidência / dado que suporta",
        "category": "evidência",
    },
    "Hip": {
        "name": "Hipótese",
        "definition": "Suposição a ser testada ou considerada",
        "expand": "hipótese",
        "category": "evidência",
    },
    "Conc": {
        "name": "Conclusão",
        "definition": "Resultado que se segue das premissas",
        "expand": "conclui-se que",
        "category": "evidência",
    },
    "Interp": {
        "name": "Interpretação",
        "definition": "Modo de entender / ler o fenômeno ou texto",
        "expand": "interpreta-se como",
        "category": "evidência",
    },
    "Met": {
        "name": "Método",
        "definition": "Caminho ou procedimento usado",
        "expand": "pelo método / mediante",
        "category": "evidência",
    },

    # 11. Escopo, Quantificação e Temporalidade
    "∀": {
        "name": "Universal",
        "definition": "Para todo / todos",
        "expand": "para todo / todos",
        "category": "escopo",
    },
    "Temp": {
        "name": "Temporalidade",
        "definition": "Quando / a partir de / durante / até",
        "expand": "no tempo / a partir de",
        "category": "escopo",
    },
    "Esc": {
        "name": "Escopo",
        "definition": "Limite de aplicação da afirmação ou norma",
        "expand": "no âmbito de / com escopo em",
        "category": "escopo",
    },

    # 12. Avaliação e Valor
    "Val+": {
        "name": "Valoração positiva",
        "definition": "É bom / desejável / correto",
        "expand": "é positivo / desejável",
        "category": "valor",
    },
    "Val−": {
        "name": "Valoração negativa",
        "definition": "É mau / indesejável / incorreto",
        "expand": "é negativo / indesejável",
        "category": "valor",
    },
    "Θ": {
        "name": "Princípio orientador",
        "definition": "Norma ou valor que deve guiar a ação",
        "expand": "segundo o princípio",
        "category": "valor",
    },
}

# ============================================================
# REGRAS SIMPLES DE COMPRESSÃO (padrões conhecidos)
# ============================================================

COMPRESSION_PATTERNS: List[Tuple[str, str]] = [
    # João 1 (mantidos para compatibilidade)
    (r"no princ[ií]pio era o verbo.*?o verbo era deus", "Γ(Σ) ∧ Ρ(Σ, Deus) ∧ Σ(Σ, Deus)"),
    (r"ele estava no princ[ií]pio com deus", "Ρ(Σ, Deus) ∘ Γ"),
    (r"todas as coisas foram feitas por (ele|interm[eé]dio dele).*?nada do que foi feito se fez", "Κ(Σ) ∧ Neg(Σ)"),
    (r"nele estava a vida.*?luz dos homens", "Σ(vida) ∧ Σ(vida, Λ)"),
    (r"a luz resplandece nas trevas.*?n[aã]o (prevaleceram|a compreenderam)", "Λ vs Δ"),

    # Padrões jurídicos genéricos
    (r"[eé] obrigado a|deve (fazer|cumprir)|tem o dever de", "Obl"),
    (r"[eé] permitido|pode (fazer|exercer)|tem o direito de", "Perm"),
    (r"[eé] proibido|n[aã]o pode|vedado", "Proib"),
    (r"salvo se|a menos que|exceto se", "Exc"),
    (r"se .* ent[aã]o|caso .* ,", "Cond"),

    # Padrões científicos / argumentativos
    (r"hip[oó]tese", "Hip"),
    (r"evid[eê]ncia|dado (emp[ií]rico|observacional)", "Evid"),
    (r"conclui-se que|portanto|logo", "Conc"),
    (r"m[eé]todo|procedim[e]nto", "Met"),

    # Genéricos de origem e identidade
    (r"no princ[ií]pio|desde o (come[cç]o|in[ií]cio)|na origem", "Γ"),
    (r"define-se como|significa que|entende-se por", "Def"),
    (r"[eé] (igual|id[eê]ntico|equivalente) a", "Σ"),
]


def compress(text: str) -> str:
    """
    Tenta comprimir um texto usando os padrões conhecidos.
    Retorna a versão simbólica (ainda experimental e limitada).
    """
    original = text.strip()
    result = original

    for pattern, symbol in COMPRESSION_PATTERNS:
        result = re.sub(pattern, symbol, result, flags=re.IGNORECASE | re.DOTALL)

    if result.strip() == original.strip():
        return f"[Nenhuma compressão forte detectada]\n\nTexto original:\n{original}"

    return result


def expand(symbolic: str) -> str:
    """
    Expande uma expressão simbólica de volta para texto aproximado
    usando as definições do índice v2.
    """
    text = symbolic

    # Substituições de expressões compostas (ordem importa)
    replacements = [
        ("Γ(Σ) ∧ Ρ(Σ, Deus) ∧ Σ(Σ, Deus)", "No princípio era o Verbo, o Verbo estava com Deus e o Verbo era Deus"),
        ("Ρ(Σ, Deus) ∘ Γ", "Ele estava no princípio com Deus"),
        ("Κ(Σ) ∧ Neg(Σ)", "Todas as coisas foram feitas por ele, e sem ele nada do que foi feito se fez"),
        ("Σ(vida) ∧ Σ(vida, Λ)", "Nele estava a vida, e a vida era a luz"),
        ("Λ vs Δ", "A luz está em oposição às trevas"),
        ("∧", " e "),
        ("∘", " "),
        ("→", " implica "),
        ("vs", " em oposição a "),
    ]

    for old, new in replacements:
        text = text.replace(old, new)

    # Expansão genérica dos símbolos restantes
    # Ordena por tamanho decrescente para evitar substituições parciais
    for symbol in sorted(SYMBOLS.keys(), key=len, reverse=True):
        if symbol in text:
            text = text.replace(symbol, SYMBOLS[symbol]["expand"])

    return text.strip()


def list_symbols(category: str = None) -> None:
    """Imprime o índice de símbolos. Pode filtrar por categoria."""
    print("\nÍNDICE DE SÍMBOLOS v2 (Agnóstico Multidominio)")
    print("=" * 70)

    current_cat = None
    for symbol, info in SYMBOLS.items():
        cat = info.get("category", "")
        if category and cat != category:
            continue
        if cat != current_cat:
            current_cat = cat
            print(f"\n[{cat.upper()}]")
        print(f"  {symbol:6} | {info['name']:<28} | {info['definition']}")
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


def get_symbols_by_category(category: str) -> Dict[str, Dict[str, str]]:
    """Retorna apenas os símbolos de uma categoria."""
    return {k: v for k, v in SYMBOLS.items() if v.get("category") == category}


# ============================================================
# INTERFACE DE LINHA DE COMANDO
# ============================================================

def main():
    print("=" * 70)
    print("  Semantic Compression Index v2 — Compressor Experimental")
    print("  Domínios: narrativa | diálogo | retórica | jurídico | científico")
    print("=" * 70)

    joao_1_5 = """No princípio era o Verbo, e o Verbo estava com Deus, e o Verbo era Deus.
Ele estava no princípio com Deus.
Todas as coisas foram feitas por ele, e sem ele nada do que foi feito se fez.
Nele estava a vida, e a vida era a luz dos homens.
A luz resplandece nas trevas, e as trevas não prevaleceram contra ela."""

    print("\n1. Texto original (João 1:1-5):")
    print("-" * 50)
    print(joao_1_5)

    print("\n2. Versão comprimida:")
    print("-" * 50)
    compressed = compress(joao_1_5)
    print(compressed)

    print("\n3. Expansão de volta (aproximação):")
    print("-" * 50)
    expanded = expand(compressed)
    print(expanded)

    print("\n4. Símbolos por categoria (amostra):")
    list_symbols()

    export_symbols_json("symbols.json")

    print("\nDica de uso como módulo:")
    print("  from semantic_compressor import compress, expand, SYMBOLS, list_symbols")
    print("  list_symbols('modalidade')   # filtra por categoria")
    print("  compress('seu texto')")
    print("  expand('Obl(Part) → Sanc')")


if __name__ == "__main__":
    main()
