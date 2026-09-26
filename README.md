# Logos OS

**Plataforma unificada de compressão, análise e tradução semântica.**

Logos OS extrai a *alma* (estrutura de significado) de qualquer texto e a representa numa interlíngua simbólica hierárquica.

---

## Hipótese central

> É possível expressar qualquer ideia em expressões matemáticas / símbolos de modo a comprimir textos, preservando o significado.

---

## Arquitetura

```text
┌─────────────────────────────────────────────────────┐
│                      LOGOS OS                       │
├─────────────────────────────────────────────────────┤
│                   Logos Core                        │
│         (Índice Ontológico + Motor Simbólico)       │
├─────────────────┬─────────────────┬─────────────────┤
│  LogosCompress  │  LogosAnalyzer  │    LogosLang    │
│  Compressão &   │  Coesão lógica  │  Tradução &     │
│  Tokens / LLM   │  & Argumentação │  Cross-domain   │
└─────────────────┴─────────────────┴─────────────────┘
```

Documentação completa da plataforma: [`PLATFORM.md`](PLATFORM.md)

---

## Núcleo Simbólico (3 Níveis)

```
Nível 1  →  Macro-funções (BE, RELATE, MODAL, DYN, COMM, EPIST, SCOPE, VAL)
Nível 2  →  12 Categorias
Nível 3  →  Símbolos base
```

### Macro-funções

| Macro | Nome | Dimensão |
|-------|------|----------|
| **BE** | Existir / Ser | O que há e o que algo é |
| **RELATE** | Relacionar | Conexões e agência |
| **MODAL** | Modular | Necessidade, dever, permissão |
| **DYN** | Dinamizar | Tensão e mudança |
| **COMM** | Comunicar | Atos de fala e persuasão |
| **EPIST** | Justificar | Evidência e argumentação |
| **SCOPE** | Delimitar | Escopo e tempo |
| **VAL** | Avaliar | Julgamento de valor |

Índice completo: [`SYMBOLS.md`](SYMBOLS.md)

---

## Módulos

| Módulo | Foco | Principais capacidades |
|--------|------|------------------------|
| **LogosCompress** | Eficiência | Economia de tokens, acelerador de LLM, condensador de conhecimento |
| **LogosAnalyzer** | Rigor | Coesão lógica, mapa argumentativo, Idea Diff |
| **LogosLang** | Ponte | Tradução semântica, transferência cross-domain |

---

## Exemplo rápido (João 1:1-5)

**Nível 3:**
```text
Γ(Σ) ∧ Ρ(Σ, Deus) ∧ Σ(Σ, Deus) ∧ Κ(Σ) ∧ Neg(Σ) ∧ Λ vs Δ
```

**Nível 1:**
```text
BE(Γ, Σ) ∧ RELATE(Ρ, Κ) ∧ DYN(Λ vs Δ)
```

---

## Status

- [x] Hipótese e índice ontológico
- [x] Hierarquia de 3 níveis + lógica modal
- [x] Visão de plataforma Logos OS
- [x] Protótipo Python básico
- [ ] Motor de extração simbólica robusto (Fase 1)
- [ ] LogosCompress MVP
- [ ] LogosAnalyzer MVP
- [ ] LogosLang MVP

---

## Código experimental

```bash
python semantic_compressor.py
```

```python
from semantic_compressor import compress, expand, SYMBOLS, list_symbols
```

---

## Roadmap resumido

1. **Fase 1** — Núcleo mínimo viável  
2. **Fase 2** — LogosCompress  
3. **Fase 3** — LogosAnalyzer  
4. **Fase 4** — LogosLang  
5. **Fase 5** — Integração e polimento  

Detalhes em [`PLATFORM.md`](PLATFORM.md)

---

*Logos OS — Compressão, análise e tradução da alma dos textos.*
