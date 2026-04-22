# Gramática LL(1), Conjuntos FIRST/FOLLOW e Tabela de Análise

> **Projeto:** Analisador Sintático — Fase 2
> **Disciplina:** Projetos de Engenharia da Computação — 2026/1
> **Instituição:** PUCPR — Pontifícia Universidade Católica do Paraná
> **Responsável pelo módulo:** Victor Rahal Basseto - Aluno 1
> **Grupo no Canvas:** `RA2_8`

Este documento descreve formalmente a gramática usada pelo analisador
sintático, demonstra que ela é **LL(1)** (sem conflitos na tabela de
análise) e apresenta os conjuntos FIRST/FOLLOW e a tabela `M[A, a]`
consumida pelo parser descendente recursivo.

---

## 1. Convenções

- **Não-terminais** aparecem em `minúsculas`.
- **Terminais** aparecem em `MAIÚSCULAS` e correspondem às categorias de
  token emitidas pelo analisador léxico da Fase 1.
- `ε` (épsilon) denota a produção vazia.
- `$` denota o marcador de fim de entrada (*end of input*).

### Terminais (tokens)

| Terminal  | Lexema / Descrição                                  |
|-----------|-----------------------------------------------------|
| `LPAREN`  | `(`                                                 |
| `RPAREN`  | `)`                                                 |
| `INT`     | literal inteiro (ex.: `3`, `-42`)                   |
| `REAL`    | literal real IEEE 754 double (ex.: `3.14`, `-0.5`)  |
| `MEM_ID`  | identificador de memória (letras maiúsculas latinas)|
| `OP_SUM`  | `+`                                                 |
| `OP_SUB`  | `-`                                                 |
| `OP_MUL`  | `*`                                                 |
| `OP_DIVR` | `\|` (divisão real)                                 |
| `OP_DIVI` | `/` (divisão inteira)                               |
| `OP_MOD`  | `%`                                                 |
| `OP_POW`  | `^`                                                 |
| `OP_LT`   | `<`                                                 |
| `OP_GT`   | `>`                                                 |
| `OP_LE`   | `<=`                                                |
| `OP_GE`   | `>=`                                                |
| `OP_EQ`   | `==`                                                |
| `OP_NE`   | `!=`                                                |
| `KW_START`| palavra reservada `START`                           |
| `KW_END`  | palavra reservada `END`                             |
| `KW_RES`  | palavra reservada `RES`                             |
| `KW_MEM`  | palavra reservada `MEM`                             |
| `KW_IF`   | palavra reservada `IF`                              |
| `KW_WHILE`| palavra reservada `WHILE`                           |
| `KW_FOR`  | palavra reservada `FOR`                             |

---

## 2. Regras de produção (EBNF)

Símbolo inicial: **`programa`**.

```ebnf
programa       ::= LPAREN KW_START RPAREN linhas

linhas         ::= LPAREN linhas_rest

linhas_rest    ::= KW_END RPAREN
                 | corpo RPAREN linhas

linha          ::= LPAREN corpo RPAREN

corpo          ::= KW_IF condicao linha linha
                 | KW_WHILE condicao linha
                 | KW_FOR INT INT MEM_ID linha
                 | INT    resto_corpo
                 | REAL   resto_corpo
                 | MEM_ID cauda_mem
                 | linha  resto_corpo

cauda_mem      ::= ε
                 | resto_corpo

resto_corpo    ::= KW_RES
                 | KW_MEM MEM_ID
                 | operando operador_arit

operando       ::= INT | REAL | MEM_ID | linha

operador_arit  ::= OP_SUM | OP_SUB | OP_MUL
                 | OP_DIVR | OP_DIVI | OP_MOD | OP_POW

condicao       ::= LPAREN operando operando op_rel RPAREN

op_rel         ::= OP_LT | OP_GT | OP_LE
                 | OP_GE | OP_EQ | OP_NE
```

### 2.1. Observações sobre as decisões de projeto

- **Parênteses explícitos em tudo.** A linguagem é totalmente
  parentizada (um par `( )` por comando/expressão). A gramática
  aproveita o `(` como âncora para decidir qual produção aplicar pelo
  **primeiro token após o `(`**.
- **Fatoração de `linhas`.** A versão ingênua
  `linhas ::= linha linhas | ε` produziria conflito em `LPAREN`
  (tanto uma nova linha quanto o `(END)` começam com `(`). Movemos o
  `LPAREN` para dentro de `linhas` e usamos o token seguinte
  (`KW_END` vs. qualquer outro) para decidir — eliminando o conflito.
- **Fatoração de `corpo` / `cauda_mem`.** `MEM_ID` é ambíguo: pode ser
  o comando `(MEM)` (consulta) ou o operando A de `(A B op)`. O
  não-terminal `cauda_mem` resolve isso com `ε` se o próximo token for
  `RPAREN` (caso `(MEM)`) e `resto_corpo` caso contrário.
- **Estruturas de controle.** Mantêm o padrão pós-fixado e totalmente
  parentizado da linguagem:
  - `(IF (cond) (then) (else))`
  - `(WHILE (cond) (corpo))`
  - `(FOR ini fim VAR (corpo))`
  - Condições usam operadores relacionais em pós-fixo:
    `(A B <)`, `(A B ==)`, etc.

---

## 3. Conjuntos FIRST

Calculados sobre os não-terminais **efetivamente usados pelo parser**
(ver `NAO_TERMINAIS_ATIVOS` em `construirGramatica.py`).

| Não-terminal     | FIRST                                                                 |
|------------------|-----------------------------------------------------------------------|
| `programa`       | { `LPAREN` }                                                          |
| `linhas`         | { `LPAREN` }                                                          |
| `linhas_rest`    | { `INT`, `KW_END`, `KW_FOR`, `KW_IF`, `KW_WHILE`, `LPAREN`, `MEM_ID`, `REAL` } |
| `linha`          | { `LPAREN` }                                                          |
| `corpo`          | { `INT`, `KW_FOR`, `KW_IF`, `KW_WHILE`, `LPAREN`, `MEM_ID`, `REAL` }  |
| `cauda_mem`      | { `INT`, `KW_MEM`, `KW_RES`, `LPAREN`, `MEM_ID`, `REAL`, `ε` }        |
| `resto_corpo`    | { `INT`, `KW_MEM`, `KW_RES`, `LPAREN`, `MEM_ID`, `REAL` }             |
| `operando`       | { `INT`, `LPAREN`, `MEM_ID`, `REAL` }                                 |
| `operador_arit`  | { `OP_DIVI`, `OP_DIVR`, `OP_MOD`, `OP_MUL`, `OP_POW`, `OP_SUB`, `OP_SUM` } |
| `condicao`       | { `LPAREN` }                                                          |
| `op_rel`         | { `OP_EQ`, `OP_GE`, `OP_GT`, `OP_LE`, `OP_LT`, `OP_NE` }              |

---

## 4. Conjuntos FOLLOW

| Não-terminal     | FOLLOW                                                                |
|------------------|-----------------------------------------------------------------------|
| `programa`       | { `$` }                                                               |
| `linhas`         | { `$` }                                                               |
| `linhas_rest`    | { `$` }                                                               |
| `linha`          | { `INT`, `KW_MEM`, `KW_RES`, `LPAREN`, `MEM_ID`, `OP_DIVI`, `OP_DIVR`, `OP_EQ`, `OP_GE`, `OP_GT`, `OP_LE`, `OP_LT`, `OP_MOD`, `OP_MUL`, `OP_NE`, `OP_POW`, `OP_SUB`, `OP_SUM`, `REAL`, `RPAREN` } |
| `corpo`          | { `RPAREN` }                                                          |
| `cauda_mem`      | { `RPAREN` }                                                          |
| `resto_corpo`    | { `RPAREN` }                                                          |
| `operando`       | { `INT`, `LPAREN`, `MEM_ID`, `OP_DIVI`, `OP_DIVR`, `OP_EQ`, `OP_GE`, `OP_GT`, `OP_LE`, `OP_LT`, `OP_MOD`, `OP_MUL`, `OP_NE`, `OP_POW`, `OP_SUB`, `OP_SUM`, `REAL` } |
| `operador_arit`  | { `RPAREN` }                                                          |
| `condicao`       | { `LPAREN` }                                                          |
| `op_rel`         | { `RPAREN` }                                                          |

> O detalhe completo dos conjuntos (com cada operador listado) está
> disponível na saída executável `docs/saida_validacao.txt`, gerada
> automaticamente ao rodar `python3 src/construirGramatica.py`.

---

## 5. Tabela de Análise LL(1) — `M[A, a]`

Cada linha abaixo corresponde a uma entrada
`M[ não_terminal , terminal ] = produção_a_aplicar`.

| Não-terminal       | Terminal     | Produção                                                    |
|--------------------|--------------|-------------------------------------------------------------|
| `programa`         | `LPAREN`     | `programa → LPAREN KW_START RPAREN linhas`                  |
| `linhas`           | `LPAREN`     | `linhas → LPAREN linhas_rest`                               |
| `linhas_rest`      | `KW_END`     | `linhas_rest → KW_END RPAREN`                               |
| `linhas_rest`      | `LPAREN`     | `linhas_rest → corpo RPAREN linhas`                         |
| `linhas_rest`      | `INT`        | `linhas_rest → corpo RPAREN linhas`                         |
| `linhas_rest`      | `REAL`       | `linhas_rest → corpo RPAREN linhas`                         |
| `linhas_rest`      | `MEM_ID`     | `linhas_rest → corpo RPAREN linhas`                         |
| `linhas_rest`      | `KW_IF`      | `linhas_rest → corpo RPAREN linhas`                         |
| `linhas_rest`      | `KW_WHILE`   | `linhas_rest → corpo RPAREN linhas`                         |
| `linhas_rest`      | `KW_FOR`     | `linhas_rest → corpo RPAREN linhas`                         |
| `linha`            | `LPAREN`     | `linha → LPAREN corpo RPAREN`                               |
| `corpo`            | `KW_IF`      | `corpo → KW_IF condicao linha linha`                        |
| `corpo`            | `KW_WHILE`   | `corpo → KW_WHILE condicao linha`                           |
| `corpo`            | `KW_FOR`     | `corpo → KW_FOR INT INT MEM_ID linha`                       |
| `corpo`            | `INT`        | `corpo → INT resto_corpo`                                   |
| `corpo`            | `REAL`       | `corpo → REAL resto_corpo`                                  |
| `corpo`            | `MEM_ID`     | `corpo → MEM_ID cauda_mem`                                  |
| `corpo`            | `LPAREN`     | `corpo → linha resto_corpo`                                 |
| `cauda_mem`        | `RPAREN`     | `cauda_mem → ε`                                             |
| `cauda_mem`        | `INT`        | `cauda_mem → resto_corpo`                                   |
| `cauda_mem`        | `REAL`       | `cauda_mem → resto_corpo`                                   |
| `cauda_mem`        | `MEM_ID`     | `cauda_mem → resto_corpo`                                   |
| `cauda_mem`        | `LPAREN`     | `cauda_mem → resto_corpo`                                   |
| `cauda_mem`        | `KW_RES`     | `cauda_mem → resto_corpo`                                   |
| `cauda_mem`        | `KW_MEM`     | `cauda_mem → resto_corpo`                                   |
| `resto_corpo`      | `KW_RES`     | `resto_corpo → KW_RES`                                      |
| `resto_corpo`      | `KW_MEM`     | `resto_corpo → KW_MEM MEM_ID`                               |
| `resto_corpo`      | `INT`        | `resto_corpo → operando operador_arit`                      |
| `resto_corpo`      | `REAL`       | `resto_corpo → operando operador_arit`                      |
| `resto_corpo`      | `MEM_ID`     | `resto_corpo → operando operador_arit`                      |
| `resto_corpo`      | `LPAREN`     | `resto_corpo → operando operador_arit`                      |
| `operando`         | `INT`        | `operando → INT`                                            |
| `operando`         | `REAL`       | `operando → REAL`                                           |
| `operando`         | `MEM_ID`     | `operando → MEM_ID`                                         |
| `operando`         | `LPAREN`     | `operando → linha`                                          |
| `operador_arit`    | `OP_SUM`     | `operador_arit → OP_SUM`                                    |
| `operador_arit`    | `OP_SUB`     | `operador_arit → OP_SUB`                                    |
| `operador_arit`    | `OP_MUL`     | `operador_arit → OP_MUL`                                    |
| `operador_arit`    | `OP_DIVR`    | `operador_arit → OP_DIVR`                                   |
| `operador_arit`    | `OP_DIVI`    | `operador_arit → OP_DIVI`                                   |
| `operador_arit`    | `OP_MOD`     | `operador_arit → OP_MOD`                                    |
| `operador_arit`    | `OP_POW`     | `operador_arit → OP_POW`                                    |
| `condicao`         | `LPAREN`     | `condicao → LPAREN operando operando op_rel RPAREN`         |
| `op_rel`           | `OP_LT`      | `op_rel → OP_LT`                                            |
| `op_rel`           | `OP_GT`      | `op_rel → OP_GT`                                            |
| `op_rel`           | `OP_LE`      | `op_rel → OP_LE`                                            |
| `op_rel`           | `OP_GE`      | `op_rel → OP_GE`                                            |
| `op_rel`           | `OP_EQ`      | `op_rel → OP_EQ`                                            |
| `op_rel`           | `OP_NE`      | `op_rel → OP_NE`                                            |

Entradas não listadas correspondem a **erro sintático** (a função
`parsear()` deve emitir mensagem clara com linha e token esperado).

---

## 6. Validação LL(1)

A função `construirTabelaLL1()` (em `src/construirGramatica.py`)
detecta conflitos durante a construção. Ao executar:

```bash
python3 src/construirGramatica.py
```

a última linha da saída é:

```
Gramática validada como LL(1) (sem conflitos na tabela).
```

Caso qualquer alteração futura introduza uma produção conflitante, a
função levanta `ValueError` listando cada conflito — prevenindo
regressão silenciosa da propriedade LL(1).

---

## 7. Interface para os demais módulos

```python
from construirGramatica import construirGramatica

info = construirGramatica()
# info["gramatica"]   -> dict { nt: [produções] }
# info["first"]       -> dict { nt: set(terminais) }
# info["follow"]      -> dict { nt: set(terminais) }
# info["tabela_ll1"]  -> dict { (nt, terminal): produção }
# info["inicio"]      -> "programa"
# info["terminais"]   -> set(...)
# info["nao_terminais"] -> set(...)
```

Estes campos são consumidos por:

- `parsear(tokens, tabela_ll1)`
- `gerarArvore(derivacao)`
- `gerarAssembly(arvore)`
