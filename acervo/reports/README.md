# Relatório: Compress sobre o acervo

Gerado com `logos-acervo compress --write acervo/reports/compress-acervo.json`.

## Leitura rápida

O Compress corre sobre a base; ratio baixo com poucos nós = extract esparso, não compressão rica. Densificar Core (FAIL `gold_acervo`) é o próximo passo útil.

## Resumo

- Ficheiros: **72**
- Extract vazio (Compress sem L1 útil): **8**
- Nós médios: **2.49**
- Tokens (est.): **12938 → 198** (corpus_ratio=0.015)
- `reduction_ratio` médio por ficheiro: **0.016** (L1/fonte; menor = mais compressão)

### Por domínio

| Domínio | n | vazios | avg_nodes | tokens src→L1 | corpus_ratio |
|---------|---|--------|-----------|---------------|--------------|
| cientifico | 5 | 2 | 0.80 | 760→4 | 0.005 |
| dialogo | 17 | 1 | 3.18 | 3099→62 | 0.020 |
| etica | 6 | 0 | 3.00 | 1093→21 | 0.019 |
| juridico | 18 | 3 | 1.83 | 2818→35 | 0.012 |
| narrativa | 26 | 2 | 2.69 | 5168→76 | 0.015 |

## Melhor compressão (ratio baixo, com nós)

- `narrativa/eca-contos-01.txt` — 277→1 (ratio=0.004) · `BE(∃)`
- `etica/jose-matias-valor-02.txt` — 241→1 (ratio=0.004) · `SCOPE(Temp)`
- `narrativa/dom-casmurro-02.txt` — 227→1 (ratio=0.004) · `BE(∃)`
- `narrativa/fialho-contos-02.txt` — 227→1 (ratio=0.004) · `SCOPE(∀)`
- `dialogo/dom-casmurro-dialogo-03.txt` — 224→1 (ratio=0.004) · `COMM(Ω)`
- `juridico/cf-art225-ambiente.txt` — 222→1 (ratio=0.005) · `SCOPE(∀)`
- `narrativa/braz-cubas-01.txt` — 175→1 (ratio=0.006) · `COMM(Ω)`
- `juridico/cc-br-artigo-03.txt` — 167→1 (ratio=0.006) · `MODAL(Proib)`

## Pior compressão / L1 fraco (ratio alto)

- `dialogo/eca-dialogo-03.txt` — 141→6 (ratio=0.043) · `DYN(Λ) ∧ COMM(Ω) ∧ SCOPE(∀, Temp)`
- `narrativa/eca-contos-05.txt` — 141→6 (ratio=0.043) · `DYN(Λ) ∧ COMM(Ω) ∧ SCOPE(∀, Temp)`
- `narrativa/chinela-turca-01.txt` — 228→9 (ratio=0.039) · `BE(∃) ∧ MODAL(Cond) ∧ EPIST(Conc) ∧ SCOPE(∀) ∧ VAL(Val+)`
- `dialogo/cartomante-dialogo-01.txt` — 133→5 (ratio=0.038) · `BE(∃) ∧ DYN(Λ) ∧ COMM(Ω)`
- `dialogo/carteira-dialogo-01.txt` — 204→7 (ratio=0.034) · `RELATE(Caus) ∧ EPIST(Conc) ∧ SCOPE(Temp) ∧ VAL(Θ)`
- `narrativa/carteira-01.txt` — 204→7 (ratio=0.034) · `RELATE(Caus) ∧ EPIST(Conc) ∧ SCOPE(Temp) ∧ VAL(Θ)`
- `etica/cf-art1-fundamentos.txt` — 88→3 (ratio=0.034) · `RELATE(Κ) ∧ SCOPE(∀)`
- `dialogo/eca-dialogo-02.txt` — 150→5 (ratio=0.033) · `COMM(Ω) ∧ EPIST(Conc) ∧ SCOPE(∀)`

## Extract vazio

- `cientifico/oa-ccby-01-propriedades-psicometricas.txt`
- `cientifico/oa-ccby-04-pesquisa-qualitativa.txt`
- `dialogo/teoria-medalhao-01.txt`
- `juridico/cdc-artigo-05.txt`
- `juridico/cf-art37-admin.txt`
- `juridico/cf-art6-sociais.txt`
- `narrativa/iracema-01.txt`
- `narrativa/iracema-02.txt`

## Como repetir

```bash
cd /home/ubuntu/worktrees/semantic-compression-index-acervo
logos-acervo compress
logos-acervo compress --json --write acervo/reports/compress-acervo.json
# um ficheiro:
logos-compress "$(cat acervo/juridico/cdc-artigo-01.txt)"
```


## Quality L1/L2/L3

```bash
logos-bench-quality
logos-bench-quality --from-acervo --write acervo/reports/quality-acervo.json
```

Plano: Project store `docs/plano-melhoria-extracao.md`.
