# Acervo em txt

Pasta para textos fonte (`.txt`) que alimentam o ciclo de melhoria do Logos Core: **extract → curar símbolos esperados → gold/eval → alargar regras/índice**.

Não renomear esta pasta para slogans tipo “dataset”. O termo do projeto é **acervo**.

## Layout

```text
acervo/
  README.md                 # este ficheiro
  stubs/                    # exemplos mínimos (não são o acervo real)
  curated/                  # sidecars .expect.json após curadoria humana
  *.txt                     # textos do acervo (raiz ou subpastas por domínio)
```

## Naming

| Peça | Convenção |
|------|-----------|
| Texto | `kebab-case.txt` (UTF-8). Ex.: `narrativa-abertura.txt` |
| Domínio (opcional) | subpasta: `juridico/`, `cientifico/`, `narrativa/`, `dialogo/` |
| Expect sidecar | `curated/<mesmo-stem>.expect.json` |
| Case id | stem do ficheiro (sem `.txt`), estável |

## Sidecar `*.expect.json`

Campos alinhados com `logos_eval` (`structural`, `symbols_subset`, `density`, `render_l1`):

```json
{
  "domain": "narrativa",
  "match_mode": "symbols_subset",
  "expect": {
    "symbols": ["Γ", "Σ"]
  }
}
```

Para piso de cobertura em prosa aberta, preferir `match_mode: "density"` com `min_nodes` / `min_matched_ratio` / `macros_any`.

## Loop (resumo)

1. **Drop** — colocar `.txt` nesta pasta (ou enviar ao Project e pedir dump aqui).
2. **Extract** — `logos-acervo preview caminho.txt` (seam Core: extract / render / expand).
3. **Curar** — escrever `curated/<stem>.expect.json` com símbolos/macros desejados.
4. **Draft gold** — `logos-acervo draft` → `logos_eval/suite/gold_acervo.json`.
5. **TDD** — `logos-eval --suite logos_eval/suite/gold_acervo.json` (falha = regra/índice a alargar).
6. **Widen** — padrões no Core / índice; repetir sem inventar acervo sintético grande.

Ver plano do Project: `docs/plano-acervo-txt.md` no Agent Store.
