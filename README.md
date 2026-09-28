# Logos OS

**Plataforma unificada de compressão, análise e tradução semântica.**

Logos OS extrai a *alma* (estrutura de significado) de qualquer texto e a representa numa interlíngua simbólica hierárquica.

## Status v1

- [x] Logos Core (`extract` / `render` / `expand` / `describe_symbol`) — SYMBOLS v3
- [x] Eval Suite (gold corpus + CI gate)
- [x] Benchmark Suite (latency / ratio / coverage)
- [x] HTTP adapter (FastAPI)
- [x] Web Workspace (DeepFlowRun look)
- [ ] LogosCompress / Analyzer / Lang (fora de escopo v1)

## Install

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Logos Core (in-process)

```bash
logos                          # demo João 1:1-5 → render L1
logos --level 3 --expand
logos --json "é obrigado a cumprir o prazo"
```

```python
from logos_core import extract, render, expand, describe_symbol

c = extract("No princípio era o Verbo…")
print(render(c, 1))   # BE(Γ, Σ) ∧ RELATE(Ρ, Κ, Neg) ∧ DYN(Λ vs Δ)
print(expand(c))
print(describe_symbol("Obl"))
```

Primary seam only — no public Parser/Index API. The legacy `semantic_compressor.py` is a deprecated shim over Core.

## Evals & benchmarks

```bash
logos-eval                 # exit 1 on regression
logos-bench --repeats 5    # p50/p95, ratio, coverage (L1)
logos-bench-quality        # qualidade L1/L2/L3 vs gold
logos-bench-quality --from-acervo --write acervo/reports/quality-acervo.json
pytest -q
```

## Acervo em txt

Textos fonte (`.txt`) em `acervo/` alimentam gold/coverage via o seam Core (`extract` / `render` / `expand`):

```bash
logos-acervo list
logos-acervo preview                   # extract → render → expand
logos-acervo compress                  # LogosCompress L1 + tokens sobre o acervo
logos-acervo compress --write acervo/reports/compress-acervo.json
logos-acervo draft --write             # casos com sidecar curated/
logos-acervo eval                      # gold_acervo.json
```

Ver `acervo/README.md` e `acervo/reports/README.md`.

## HTTP adapter

```bash
logos-http                 # http://127.0.0.1:8000
# POST /v1/extract | /v1/render | /v1/expand | /v1/describe_symbol | /v1/compress
```

## Web Workspace

```bash
# terminal 1
logos-http

# terminal 2
cd web
cp .env.local.example .env.local   # NEXT_PUBLIC_LOGOS_API=http://127.0.0.1:8000
npm install
npm run dev                        # http://127.0.0.1:3000
```

## Architecture (v1)

```text
SYMBOLS v3 (internal to Core)
        ↓
   Logos Core  ←── Eval + Benchmark (same interface)
        ↓
  HTTP adapter
        ↓
  Web Workspace
```

Índice completo: [`SYMBOLS.md`](SYMBOLS.md) · Plataforma: [`PLATFORM.md`](PLATFORM.md)

---

*Logos OS — Compressão, análise e tradução da alma dos textos.*
