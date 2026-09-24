# Semantic Compression Index

Sistema de compressão semântica de textos por meio de **símbolos/funções encapsuladas** de ideias agnósticas.

Inspirado na Complexidade de Kolmogorov e desenvolvido a partir de experimentos com o Evangelho de João.

O objetivo é comprimir a **alma** (ideias geradoras) de um texto, e não apenas o seu corpo (sequência de palavras).

## Hipótese central

> É possível expressar qualquer ideia em expressões matemáticas / símbolos de modo a comprimir textos, preservando o significado.

## Arquitetura em 3 Níveis (v3)

```
Nível 1  →  Macro-funções (alta abstração)
Nível 2  →  12 Categorias
Nível 3  →  Símbolos base
```

### Macro-funções (Nível 1)

| Macro | Nome | Dimensão ontológica | Categorias |
|-------|------|---------------------|----------|
| **BE** | Existir / Ser | O que há e o que algo é | Existência + Identidade |
| **RELATE** | Relacionar | Como as coisas se conectam e agem | Relação + Agência |
| **MODAL** | Modular | Necessidade, dever, permissão | Modalidade + Condição |
| **DYN** | Dinamizar | Tensão e mudança | Oposição + Transformação |
| **COMM** | Comunicar | Atos de fala e persuasão | Comunicação |
| **EPIST** | Justificar | Como se conhece e se prova | Evidência + Justificação |
| **SCOPE** | Delimitar | Limites e tempo | Escopo + Temporalidade |
| **VAL** | Avaliar | Julgamento de valor | Avaliação + Valor |

### Lógica Modal integrada

- **Alética**: □ (Nec), ◇ (Poss)
- **Deôntica**: Obl, Perm, Proib
- **Epistêmica**: pode ser usada dentro de EPIST
- Condicionais, sanções e exceções

### Fundamentos filosóficos

- Aristóteles (categorias, potência/ato, causas)
- Lógica modal contemporânea (Kripke, von Wright)
- Ontologias formais (BFO, DOLCE)
- Atos de fala (Austin / Searle)
- Dialética e filosofia do processo

O arquivo completo está em [`SYMBOLS.md`](SYMBOLS.md).

## Gramática de combinação

- `A ∧ B` → coordenação
- `A(B)` → aplicação
- `A → B` → implicação
- `A vs B` → oposição
- `¬A` → negação
- `MACRO(A, B)` → agrupamento de nível 1
- Aninhamento permitido em qualquer nível

## Exemplo clássico: João 1:1-5

**Nível 3 (símbolos base):**
```
Γ(Σ) ∧ Ρ(Σ, Deus) ∧ Σ(Σ, Deus)
Ρ(Σ, Deus) ∘ Γ
Κ(Σ) ∧ Neg(Σ)
Σ(vida) ∧ Σ(vida, Λ)
Λ vs Δ
```

**Nível 1 (macro-funções):**
```
BE(Γ, Σ) ∧ RELATE(Ρ, Κ) ∧ DYN(Λ vs Δ)
```

## Ferramenta Python

O arquivo `semantic_compressor.py` implementa a versão experimental do sistema.

```bash
python semantic_compressor.py
```

```python
from semantic_compressor import compress, expand, SYMBOLS, list_symbols
list_symbols('modalidade')
```

## Status do projeto

- [x] Hipótese formulada
- [x] Índice inicial de símbolos
- [x] Índice expandido agnóstico (v2)
- [x] Hierarquia de 3 níveis + Macro-funções (v3)
- [x] Integração com lógica modal
- [x] Ancoragem em ontologias filosóficas
- [x] Ferramenta Python básica
- [ ] Atualização do compressor Python para reconhecer macro-funções
- [ ] Mais exemplos em textos jurídicos e científicos
- [ ] Melhoria do motor de compressão

## Como contribuir

Sugestões de novos símbolos, testes em outros domínios ou melhorias no código são bem-vindas.
