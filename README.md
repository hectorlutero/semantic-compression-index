# Semantic Compression Index

Sistema de compressão semântica de textos por meio de **símbolos/funções encapsuladas** de ideias agnósticas.

Inspirado na Complexidade de Kolmogorov e desenvolvido a partir de experimentos com o Evangelho de João.

O objetivo é comprimir a **alma** (ideias geradoras) de um texto, e não apenas o seu corpo (sequência de palavras).

## Hipótese central

> É possível expressar qualquer ideia em expressões matemáticas / símbolos de modo a comprimir textos, preservando o significado.

## Como funciona

1. Identificamos padrões de significado **agnósticos** (reutilizáveis em qualquer tipo de texto).
2. Cada padrão vira um **símbolo** (como uma função ou helper).
3. O texto é reescrito como composição desses símbolos.
4. A expansão (descompressão) recupera as ideias originais.

## Índice de Símbolos (v2 — Agnóstico Multidominio)

O índice foi expandido para cobrir de forma equilibrada:

- Narrativa (qualquer gênero)
- Diálogo
- Retórica
- Textos jurídicos
- Textos científicos

### Categorias principais

1. **Existência e Origem** → Γ, ∃, ∄, Μ  
2. **Identidade e Definição** → Σ, Def, ≈, ≠  
3. **Relação e Estrutura** → Ρ, ∈, ⊂, Hier, Part  
4. **Agência e Causação** → Κ, Caus, Neg, Obj  
5. **Modalidade** → Obl, Perm, Proib, Nec, Poss  
6. **Condição e Consequência** → Cond, Sanc, Exc, →  
7. **Oposição e Dualidade** → Λ, Δ, vs, ¬  
8. **Transformação** → Τ, Β, Δt  
9. **Comunicação e Atos de Fala** → Ω, Ι, Quest, Resp, Arg, Pers, Iron  
10. **Evidência e Justificação** → Evid, Hip, Conc, Interp, Met  
11. **Escopo e Temporalidade** → ∀, ∃, Temp, Esc  
12. **Avaliação e Valor** → Val+, Val−, Θ  

O arquivo completo e detalhado está em [`SYMBOLS.md`](SYMBOLS.md).

## Gramática básica de combinação

- `A ∧ B` → justaposição / coordenação
- `A(B)` → aplicação (A age sobre B)
- `A → B` ou `Cond(A → B)` → condição / implicação
- `A vs B` → oposição
- `¬A` ou `Neg(A)` → negação
- `A ∘ B` → composição / sequência
- Aninhamento permitido: `Τ(Π(Μ(Σ)))`

## Exemplo clássico: João 1:1-5

```
(1) Γ(Σ) ∧ Ρ(Σ, Deus) ∧ Σ(Σ, Deus)
(2) Ρ(Σ, Deus) ∘ Γ
(3) Κ(Σ) ∧ Neg(Σ)
(4) Σ(vida) ∧ Σ(vida, Λ_homens)
(5) Λ vs Δ   (Δ não prevalece)
```

## Ferramenta Python (Compressor / Expander)

O arquivo `semantic_compressor.py` contém uma implementação experimental em Python.

### Funcionalidades

- `compress(text)` → tenta comprimir texto para a forma simbólica
- `expand(symbolic)` → expande símbolos de volta para texto aproximado
- `list_symbols()` → mostra o índice completo
- `export_symbols_json()` → exporta o índice para JSON
- Importação e exportação de arquivos de texto

### Como usar

```bash
python semantic_compressor.py
```

Ou como módulo:

```python
from semantic_compressor import compress, expand, SYMBOLS

texto = "No princípio era o Verbo..."
comprimido = compress(texto)
print(comprimido)
```

> **Nota**: A compressão atual ainda é baseada em regras. É um protótipo educacional.

## Status do projeto

- [x] Hipótese formulada
- [x] Índice inicial de símbolos
- [x] Índice expandido agnóstico (v2) — narrativa, diálogo, retórica, jurídico, científico
- [x] Gramática de combinação
- [x] Teste com João 1:1-5
- [x] Teste com texto secular
- [x] Ferramenta Python básica
- [ ] Atualização do compressor Python para o índice v2
- [ ] Mais exemplos em textos jurídicos e científicos
- [ ] Melhoria do motor de compressão

## Como contribuir

Sugestões de novos símbolos, testes em outros domínios ou melhorias no código são bem-vindas.
