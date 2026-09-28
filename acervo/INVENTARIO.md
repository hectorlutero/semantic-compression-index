# Acervo puxado — inventário

Snippets curtos (UTF-8 `.txt`) + sidecars em `curated/`.  
**Não** há dump integral de livros.

| Domínio | Papel |
|---------|--------|
| `narrativa/` | Prosa literária PD (Gutenberg + Wikisource) |
| `dialogo/` | Actos de fala / diálogo |
| `juridico/` | Atos oficiais BR + Código Civil PT |
| `cientifico/` | Abstracts OpenAlex **CC BY** |
| `etica/` | CF fundamentos + prosa valorativa PD |
| `curated/` | `*.expect.json` (gold draft) |

Contagens (aprox.): ver `find acervo -name '*.txt' | wc -l` no worktree (~72).

## Fontes alternativas usadas (além do 1.º lote)

| Fonte | Uso |
|-------|-----|
| Gutenberg *Dom Casmurro*, *Brás Cubas*, *Iracema* | narrativa / diálogo |
| Wikisource *A Cartomante*, *A causa secreta*, *A chinela turca*, *A carteira*, *Teoria do medalhão* | narrativa / diálogo / ética |
| Planalto Código Civil BR (Lei 10.406) | jurídico |
| PGDL Lisboa — Código Civil PT | jurídico PT-PT |
| OpenAlex CC BY | científico (SciELO HTML bloqueado 403) |

Atribuição: `SOURCES.md` por domínio.

## Gold / eval

- `logos_eval/suite/gold_acervo.json` — gerado via `logos-acervo draft --write`
- Baseline recente: ~54/72 PASS; FAIL restantes = piso de densidade / COMM / EPIST a densificar no Core
- **Não** ligado ao `logos-eval` CI default (`gold_v1`) — correr `logos-acervo eval`
