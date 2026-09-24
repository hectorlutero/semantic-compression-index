# Índice de Símbolos Agnósticos (v3)

Sistema hierárquico de compressão semântica em **três níveis**, ancorado em ontologias filosóficas e lógica modal.

---

## Arquitetura em 3 Níveis

```
Nível 1  →  Macro-funções (alta abstração)
Nível 2  →  Categorias (as 12 famílias)
Nível 3  →  Símbolos base (operadores atômicos)
```

Quanto mais alto o nível, maior a compressão e maior o grau de agnosticismo.

---

# NÍVEL 1 — Macro-funções

As macro-funções são operadores de ordem superior. Cada uma corresponde a uma dimensão ontológica fundamental.

| Macro | Nome | Dimensão ontológica | Categorias que agrupa | Raiz filosófica principal |
|-------|------|---------------------|-----------------------|---------------------------|
| **BE** | Existir / Ser | O que há e o que algo é | Existência + Identidade | Aristóteles (ousia), Heidegger (Sein), BFO Continuant |
| **RELATE** | Relacionar | Como as coisas se conectam e agem | Relação + Agência | Aristóteles (relação + causa eficiente), Whitehead |
| **MODAL** | Modular | Necessidade, possibilidade, dever, permissão | Modalidade + Condição | Lógica modal (Kripke, von Wright), deôntica |
| **DYN** | Dinamizar | Tensão, oposição e mudança | Oposição + Transformação | Heráclito, Hegel (dialética), processo |
| **COMM** | Comunicar | Atos de fala e persuasão | Comunicação | Austin / Searle (speech acts), retórica clássica |
| **EPIST** | Justificar | Como se conhece e se prova | Evidência + Justificação | Epistemologia, justificação (Gettier, Goldman) |
| **SCOPE** | Delimitar | Limites de aplicação e tempo | Escopo + Temporalidade | Quantificação, temporal logic |
| **VAL** | Avaliar | Julgamento de valor | Avaliação + Valor | Axiologia, ética normativa |

### Notação das macro-funções

```text
BE(Γ, Σ)                     → origem + identidade
RELATE(Κ, Caus)              → agência + causalidade
MODAL(Obl, Cond → Sanc)      → obrigação condicionada com sanção
DYN(Λ vs Δ, Τ)               → oposição que gera transformação
COMM(Quest → Resp → Arg)     → sequência dialógica
EPIST(Hip, Evid, Conc)       → estrutura de argumentação científica
SCOPE(∀, Temp)               → universalidade temporal
VAL(Θ, Val+)                 → princípio orientador positivo
```

---

# Lógica Modal integrada ao sistema

A macro-função **MODAL** incorpora os principais sistemas de lógica modal.

## 1. Lógica Alética (necessidade e possibilidade)

| Símbolo | Significado | Leitura |
|---------|-------------|--------|
| **□** / **Nec** | Necessidade | É necessário que… (verdadeiro em todos os mundos possíveis relevantes) |
| **◇** / **Poss** | Possibilidade | É possível que… (verdadeiro em pelo menos um mundo possível) |

Relações clássicas:
- `□P → P` (o necessário é verdadeiro)
- `P → ◇P` (o verdadeiro é possível)
- `□P ↔ ¬◇¬P`

## 2. Lógica Deôntica (obrigação, permissão, proibição)

| Símbolo | Significado | Leitura |
|---------|-------------|--------|
| **Obl** / **O** | Obrigação | Deve ser feito |
| **Perm** / **P** | Permissão | Pode ser feito |
| **Proib** / **F** | Proibição | É proibido (O¬) |

Relações clássicas (von Wright):
- `Obl(p) → Perm(p)`
- `Proib(p) ↔ Obl(¬p)`
- `¬(Obl(p) ∧ Obl(¬p))` (consistência deôntica)

## 3. Lógica Epistêmica (conhecimento e crença)

Pode ser usada dentro de **EPIST**:

| Símbolo | Significado |
|---------|-------------|
| **K** | Sabe que… |
| **B** | Acredita que… |

## 4. Condicionais e consequências

| Símbolo | Significado |
|---------|-------------|
| **Cond** / **→** | Se A então B |
| **Sanc** | Consequência normativa ou causal |
| **Exc** | Exceção (derrotabilidade) |

Exemplo de fórmula deôntica comprimida:

```text
MODAL( Obl(Part, ação) ∧ Cond(¬ação → Sanc) ∧ Exc(justa_causa) )
```

---

# Fundamentos Ontológicos

O sistema se inspira em várias tradições, sem se prender a nenhuma:

### 1. Aristóteles (Categorias + Física + Metafísica)
- Substância ≈ **BE**
- Relação + Ação/Paixão ≈ **RELATE**
- Potência e Ato ≈ **DYN** + **Μ** (manifestação)
- Quatro causas → especialmente causa eficiente dentro de **Κ / Caus**

### 2. Lógica Modal contemporânea (Kripke, Hintikka, von Wright)
- Mundos possíveis → sustentam **Nec** e **Poss**
- Deôntica → sustenta **Obl / Perm / Proib**
- Epistêmica → dialoga com **EPIST**

### 3. Ontologias formais modernas
- **BFO (Basic Formal Ontology)**: distinção Continuant / Occurrent  
  → Continuant ≈ **BE** + **RELATE**  
  → Occurrent / Process ≈ **DYN**
- **DOLCE**: endurants / perdurants → mesma intuição

### 4. Filosofia da linguagem e atos de fala
- Austin e Searle → fundamentam a macro **COMM**  
  (assertivos, diretivos, comissivos, expressivos, declarativos)

### 5. Dialética e processo
- Heráclito / Hegel → **DYN** (oposição e transformação)
- Whitehead (Process and Reality) → reforça a primazia do processo

---

# NÍVEL 2 — As 12 Categorias

## 1. Existência e Origem
| Símbolo | Nome | Definição |
|---------|------|-----------|
| **Γ** | Origem / Princípio | Algo existe desde o início ou é o ponto de partida |
| **∃** | Existência | Algo existe / há |
| **∄** | Inexistência | Algo não existe / não há |
| **Μ** | Manifestação | O que estava oculto ou potencial se torna presente |

## 2. Identidade e Definição
| Símbolo | Nome | Definição |
|---------|------|-----------|
| **Σ** | Identidade | A é B |
| **Def** | Definição | Para os fins deste contexto, X significa… |
| **≈** | Semelhança | A é semelhante / análogo a B |
| **≠** | Diferença | A não é B |

## 3. Relação e Estrutura
| Símbolo | Nome | Definição |
|---------|------|-----------|
| **Ρ** | Presença / Relação | X está com / em relação a Y |
| **∈** | Pertencimento | X pertence a Y |
| **⊂** | Inclusão | X está contido em Y |
| **Hier** | Hierarquia | X está acima ou subordinado a Y |
| **Part** | Parte / Sujeito | Agente, paciente ou participante |

## 4. Agência e Causação
| Símbolo | Nome | Definição |
|---------|------|-----------|
| **Κ** | Agência | X age ou é o meio pelo qual algo ocorre |
| **Caus** | Nexo causal | A produz / provoca B |
| **Neg** | Negação de agência | Sem X, B não ocorreria |
| **Obj** | Objeto | Aquilo sobre o qual a ação incide |

## 5. Modalidade
| Símbolo | Nome | Definição |
|---------|------|-----------|
| **Obl** | Obrigação | X deve fazer Y |
| **Perm** | Permissão | X pode fazer Y |
| **Proib** | Proibição | X não pode fazer Y |
| **Nec** / **□** | Necessidade | É necessário que… |
| **Poss** / **◇** | Possibilidade | É possível que… |

## 6. Condição e Consequência
| Símbolo | Nome | Definição |
|---------|------|-----------|
| **Cond** | Condição | Se A, então B |
| **Sanc** | Consequência / Sanção | Se A → segue-se B |
| **Exc** | Exceção | Salvo se / a menos que |
| **→** | Implicação | A implica B |

## 7. Oposição e Dualidade
| Símbolo | Nome | Definição |
|---------|------|-----------|
| **Λ** | Polo positivo | O lado que revela ou afirma |
| **Δ** | Polo negativo | O lado que oculta ou resiste |
| **vs** | Oposição | A em tensão com B |
| **¬** | Negação | Não-A |

## 8. Transformação
| Símbolo | Nome | Definição |
|---------|------|-----------|
| **Τ** | Transformação de status | X muda de estado |
| **Β** | Transformação radical | Mudança profunda |
| **Δt** | Mudança no tempo | Antes → Depois |

## 9. Comunicação e Atos de Fala
| Símbolo | Nome | Definição |
|---------|------|-----------|
| **Ω** | Afirmação / Testemunho | Declara ou testemunha |
| **Ι** | Autodeclaração | “Eu sou / eu afirmo” |
| **Quest** | Pergunta | Interrogação |
| **Resp** | Resposta | Réplica |
| **Arg** | Argumento | Razão apresentada |
| **Pers** | Persuasão | Tentativa de convencer |
| **Iron** | Ironia | Tensão retórica |

## 10. Evidência e Justificação
| Símbolo | Nome | Definição |
|---------|------|-----------|
| **Evid** | Evidência | Dado apresentado como suporte |
| **Hip** | Hipótese | Suposição a ser testada |
| **Conc** | Conclusão | Resultado das premissas |
| **Interp** | Interpretação | Modo de entender |
| **Met** | Método | Procedimento usado |

## 11. Escopo e Temporalidade
| Símbolo | Nome | Definição |
|---------|------|-----------|
| **∀** | Universal | Para todo |
| **Temp** | Temporalidade | Quando / durante / até |
| **Esc** | Escopo | Limite de aplicação |

## 12. Avaliação e Valor
| Símbolo | Nome | Definição |
|---------|------|-----------|
| **Val+** | Valoração positiva | É bom / desejável |
| **Val−** | Valoração negativa | É mau / indesejável |
| **Θ** | Princípio orientador | Norma ou valor guia |

---

# Gramática de combinação (todos os níveis)

- `A ∧ B` → coordenação
- `A(B)` → aplicação
- `A → B` → implicação / condição
- `A vs B` → oposição
- `¬A` → negação
- `A ∘ B` → composição sequencial
- `MACRO(A, B, C)` → agrupamento de nível 1
- Aninhamento permitido em qualquer nível

---

# Princípios de design

1. **Agnosticismo de domínio e de língua**
2. **Hierarquia de abstração** (3 níveis)
3. **Composicionalidade**
4. **Ancoragem ontológica explícita**
5. **Integração com lógica modal** (alética + deôntica + epistêmica)
6. **Compressão da alma** (padrão de significado, não superfície linguística)

---

*Versão 3 — Hierárquica, modal e ontologicamente fundamentada.*
