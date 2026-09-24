# Semantic Compression Index

Sistema de compressão semântica de textos por meio de **símbolos/funções encapsuladas** de ideias agnósticas.

Inspirado na Complexidade de Kolmogorov e desenvolvido a partir de experimentos com o Evangelho de João.

O objetivo é comprimir a **alma** (ideias geradoras) de um texto, e não apenas o seu corpo (sequência de palavras).

## Hipótese central

> É possível expressar qualquer ideia em expressões matemáticas / símbolos de modo a comprimir textos, preservando o significado.

## Como funciona

1. Identificamos padrões de significado **agnósticos** (reutilizáveis em qualquer narrativa, diálogo ou texto).
2. Cada padrão vira um **símbolo** (como uma função ou helper).
3. O texto é reescrito como composição desses símbolos.
4. A expansão (descompressão) recupera as ideias originais.

## Índice de Símbolos (versão atual)

| Símbolo     | Nome curto              | Definição agnóstica |
|-------------|-------------------------|---------------------|
| `Γ`         | Origem / Princípio      | Existe desde o início, antes de tudo |
| `Σ`         | Identidade profunda     | A é B (essência ou natureza) |
| `Ρ`         | Relação de presença     | X está com Y / junto de Y |
| `Κ`         | Agência criadora        | Tudo (ou o essencial) foi feito por meio de X |
| `Neg`       | Negação universal       | Sem X, nada do que existe teria existido |
| `Λ`         | Luz / Revelação         | Aquilo que ilumina, torna visível ou revela |
| `Δ`         | Trevas / Oposição       | Aquilo que resiste, oculta ou não compreende |
| `Μ`         | Manifestação            | O que era eterno ou oculto se torna presente |
| `Π`         | Recepção                | Alguém acolhe / aceita / crê |
| `Ρej`       | Rejeição                | Os “seus” não acolhem |
| `Τ`         | Transformação de status | Quem acolhe recebe novo estatuto |
| `Ω`         | Testemunho              | Alguém ou algo aponta / dá testemunho |
| `Ι`         | Autodeclaração          | “Eu sou” + predicado |
| `Η`         | Hora / Momento decisivo | O tempo marcado chega |
| `Α`         | Permanência             | Ficar / permanecer / habitar em relação |
| `Β`         | Novo nascimento         | Nascer de novo / transformação radical |
| `Φ`         | Dom / Oferta            | Algo é dado gratuitamente |
| `Ψ`         | Conflito de compreensão | Mal-entendido que revela verdade mais profunda |
| `Ξ`         | Exaltação               | Ser elevado (literal ou figurado) |
| `Θ`         | Amor como mandamento    | Amar da mesma forma que se foi amado |

## Gramática básica de combinação

- `A ∧ B` → justaposição / sequência
- `A(B)` → aplicação (A age sobre B)
- `¬A` ou `Neg` → negação
- `A vs B` → oposição
- `A → B` → transformação
- Aninhamento permitido: `Τ(Π(Μ(Σ)))`

## Exemplo: João 1:1-5

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
# Executar o exemplo embutido (João 1:1-5)
python semantic_compressor.py
```

Ou como módulo:

```python
from semantic_compressor import compress, expand, SYMBOLS

texto = "No princípio era o Verbo..."
comprimido = compress(texto)
print(comprimido)

expandido = expand(comprimido)
print(expandido)
```

> **Nota**: A compressão atual é baseada em regras e padrões conhecidos (especialmente João 1). É um protótipo educacional, não um compressor genérico de alta precisão.

## Status do projeto

- [x] Hipótese formulada
- [x] Índice inicial de símbolos agnósticos
- [x] Gramática mínima de combinação
- [x] Teste com João 1:1-5
- [x] Teste com texto secular
- [x] Ferramenta de compressão/descompressão (Python)
- [ ] Ampliação do índice com mais padrões de João
- [ ] Mais exemplos em textos literários e noticiosos
- [ ] Melhoria do motor de compressão (NLP / embeddings)

## Como contribuir

Este repositório é o ponto de partida. Sugestões de novos símbolos, melhorias na gramática, testes em outros textos ou melhorias no código Python são bem-vindas.
