# Documentação da Gramática e Análise Sintática

> **Disciplina:** Projetos de Engenharia da Computação — 2026/1
> **Instituição:** PUCPR — Pontifícia Universidade Católica do Paraná
> **Grupo no Canvas:** `RA2_8`

Este documento atende ao item **11.4** do enunciado da Fase 2, contendo:

1. O conjunto de regras de produção da gramática (em EBNF);
2. Os conjuntos **FIRST** e **FOLLOW** de cada não-terminal;
3. A **Tabela de Análise LL(1)**;
4. A representação da **árvore sintática** gerada para um arquivo de teste.

Todos os dados aqui apresentados são produzidos automaticamente pelo módulo
`construirGramatica.py` (regras, FIRST, FOLLOW, tabela) e pelo pipeline
`lerTokens` → `parsear` (derivação e árvore). O arquivo de exemplo usado
para a árvore é `testes/teste_doc.txt`.

---

## 1. Convenções

- Não-terminais em **minúsculas**;
- Terminais em **MAIÚSCULAS** (correspondem aos tipos de token gerados pelo lexer);
- `ε` denota a produção vazia;
- `$` denota o marcador de fim de entrada.

### Mapeamento token → símbolo terminal

| Categoria | Terminal | Símbolo concreto |
|---|---|---|
| Pontuação | `LPAREN`, `RPAREN` | `(`, `)` |
| Literais | `INT`, `REAL` | inteiro, ponto flutuante |
| Identificador | `MEM_ID` | letras maiúsculas (ex.: `VAR`, `CONT`) |
| Aritméticos | `OP_SUM`, `OP_SUB`, `OP_MUL`, `OP_DIVR`, `OP_DIVI`, `OP_MOD`, `OP_POW` | `+`, `-`, `*`, `\|`, `/`, `%`, `^` |
| Relacionais | `OP_LT`, `OP_GT` | `<`, `>` |
| Palavras reservadas | `KW_START`, `KW_END`, `KW_RES`, `KW_MEM`, `KW_IF`, `KW_WHILE`, `KW_FOR` | `START`, `END`, `RES`, `MEM`, `IF`, `WHILE`, `FOR` |

> **Nota:** os operadores relacionais compostos `<=`, `>=`, `==`, `!=`
> **não** fazem parte da linguagem. Seu uso gera erro léxico.

---

## 2. Regras de Produção (EBNF)

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

operando       ::= INT
                 | REAL
                 | MEM_ID
                 | linha

operador_arit  ::= OP_SUM | OP_SUB | OP_MUL
                 | OP_DIVR | OP_DIVI | OP_MOD | OP_POW

condicao       ::= LPAREN operando operando op_rel RPAREN

op_rel         ::= OP_LT | OP_GT
```

### Observações de fatoração

- **`linhas_rest`**: distingue `(END)` de uma nova linha pelo token seguinte ao `(`.
- **`cauda_mem`**: distingue `(VAR)` (consulta de memória) de `VAR` como operando, observando se o próximo token é `)` ou outro símbolo válido em `resto_corpo`.
- **`corpo`**: decide o caminho pelo primeiro token: keyword de controle, literal numérico, identificador de memória ou parêntese aninhado.

A propriedade LL(1) é validada automaticamente em `construirTabelaLL1`: caso surja qualquer conflito durante a construção, a função `construirGramatica()` levanta `ValueError`.

---

## 3. Conjuntos FIRST

| Não-terminal | FIRST |
|---|---|
| `programa` | { `LPAREN` } |
| `linhas` | { `LPAREN` } |
| `linhas_rest` | { `INT`, `KW_END`, `KW_FOR`, `KW_IF`, `KW_WHILE`, `LPAREN`, `MEM_ID`, `REAL` } |
| `linha` | { `LPAREN` } |
| `corpo` | { `INT`, `KW_FOR`, `KW_IF`, `KW_WHILE`, `LPAREN`, `MEM_ID`, `REAL` } |
| `cauda_mem` | { `INT`, `KW_MEM`, `KW_RES`, `LPAREN`, `MEM_ID`, `REAL`, `ε` } |
| `resto_corpo` | { `INT`, `KW_MEM`, `KW_RES`, `LPAREN`, `MEM_ID`, `REAL` } |
| `operando` | { `INT`, `LPAREN`, `MEM_ID`, `REAL` } |
| `operador_arit` | { `OP_DIVI`, `OP_DIVR`, `OP_MOD`, `OP_MUL`, `OP_POW`, `OP_SUB`, `OP_SUM` } |
| `condicao` | { `LPAREN` } |
| `op_rel` | { `OP_GT`, `OP_LT` } |

---

## 4. Conjuntos FOLLOW

| Não-terminal | FOLLOW |
|---|---|
| `programa` | { `$` } |
| `linhas` | { `$` } |
| `linhas_rest` | { `$` } |
| `linha` | { `INT`, `KW_MEM`, `KW_RES`, `LPAREN`, `MEM_ID`, `OP_DIVI`, `OP_DIVR`, `OP_GT`, `OP_LT`, `OP_MOD`, `OP_MUL`, `OP_POW`, `OP_SUB`, `OP_SUM`, `REAL`, `RPAREN` } |
| `corpo` | { `RPAREN` } |
| `cauda_mem` | { `RPAREN` } |
| `resto_corpo` | { `RPAREN` } |
| `operando` | { `INT`, `LPAREN`, `MEM_ID`, `OP_DIVI`, `OP_DIVR`, `OP_GT`, `OP_LT`, `OP_MOD`, `OP_MUL`, `OP_POW`, `OP_SUB`, `OP_SUM`, `REAL` } |
| `operador_arit` | { `RPAREN` } |
| `condicao` | { `LPAREN` } |
| `op_rel` | { `RPAREN` } |

---

## 5. Tabela de Análise LL(1)

A tabela mapeia pares `(não-terminal, terminal)` para a produção a aplicar. Para legibilidade — e porque a maioria das células seria vazia — apresenta-se como uma lista agrupada por não-terminal.

```
M[programa     , LPAREN   ] = programa     -> LPAREN KW_START RPAREN linhas

M[linhas       , LPAREN   ] = linhas       -> LPAREN linhas_rest

M[linhas_rest  , INT      ] = linhas_rest  -> corpo RPAREN linhas
M[linhas_rest  , KW_END   ] = linhas_rest  -> KW_END RPAREN
M[linhas_rest  , KW_FOR   ] = linhas_rest  -> corpo RPAREN linhas
M[linhas_rest  , KW_IF    ] = linhas_rest  -> corpo RPAREN linhas
M[linhas_rest  , KW_WHILE ] = linhas_rest  -> corpo RPAREN linhas
M[linhas_rest  , LPAREN   ] = linhas_rest  -> corpo RPAREN linhas
M[linhas_rest  , MEM_ID   ] = linhas_rest  -> corpo RPAREN linhas
M[linhas_rest  , REAL     ] = linhas_rest  -> corpo RPAREN linhas

M[linha        , LPAREN   ] = linha        -> LPAREN corpo RPAREN

M[corpo        , INT      ] = corpo        -> INT resto_corpo
M[corpo        , KW_FOR   ] = corpo        -> KW_FOR INT INT MEM_ID linha
M[corpo        , KW_IF    ] = corpo        -> KW_IF condicao linha linha
M[corpo        , KW_WHILE ] = corpo        -> KW_WHILE condicao linha
M[corpo        , LPAREN   ] = corpo        -> linha resto_corpo
M[corpo        , MEM_ID   ] = corpo        -> MEM_ID cauda_mem
M[corpo        , REAL     ] = corpo        -> REAL resto_corpo

M[cauda_mem    , INT      ] = cauda_mem    -> resto_corpo
M[cauda_mem    , KW_MEM   ] = cauda_mem    -> resto_corpo
M[cauda_mem    , KW_RES   ] = cauda_mem    -> resto_corpo
M[cauda_mem    , LPAREN   ] = cauda_mem    -> resto_corpo
M[cauda_mem    , MEM_ID   ] = cauda_mem    -> resto_corpo
M[cauda_mem    , REAL     ] = cauda_mem    -> resto_corpo
M[cauda_mem    , RPAREN   ] = cauda_mem    -> ε

M[resto_corpo  , INT      ] = resto_corpo  -> operando operador_arit
M[resto_corpo  , KW_MEM   ] = resto_corpo  -> KW_MEM MEM_ID
M[resto_corpo  , KW_RES   ] = resto_corpo  -> KW_RES
M[resto_corpo  , LPAREN   ] = resto_corpo  -> operando operador_arit
M[resto_corpo  , MEM_ID   ] = resto_corpo  -> operando operador_arit
M[resto_corpo  , REAL     ] = resto_corpo  -> operando operador_arit

M[operando     , INT      ] = operando     -> INT
M[operando     , LPAREN   ] = operando     -> linha
M[operando     , MEM_ID   ] = operando     -> MEM_ID
M[operando     , REAL     ] = operando     -> REAL

M[operador_arit, OP_DIVI  ] = operador_arit -> OP_DIVI
M[operador_arit, OP_DIVR  ] = operador_arit -> OP_DIVR
M[operador_arit, OP_MOD   ] = operador_arit -> OP_MOD
M[operador_arit, OP_MUL   ] = operador_arit -> OP_MUL
M[operador_arit, OP_POW   ] = operador_arit -> OP_POW
M[operador_arit, OP_SUB   ] = operador_arit -> OP_SUB
M[operador_arit, OP_SUM   ] = operador_arit -> OP_SUM

M[condicao     , LPAREN   ] = condicao     -> LPAREN operando operando op_rel RPAREN

M[op_rel       , OP_GT    ] = op_rel       -> OP_GT
M[op_rel       , OP_LT    ] = op_rel       -> OP_LT
```

A tabela contém **44 entradas** distribuídas em 11 não-terminais e foi gerada automaticamente sem conflitos, atestando que a gramática é LL(1).

---

## 6. Árvore Sintática — Execução de Exemplo

Esta seção apresenta a derivação e a árvore sintática para o arquivo `testes/teste_doc.txt`, que cobre todos os recursos da linguagem em uma forma compacta:

```text
(START)
(3.0 4.0 +)              # operação aritmética com REAL
(10 2 -)                 # operação aritmética com INT
(42.5 MEM VAL)           # atribuição de memória
(VAL)                    # leitura de memória
(1 RES)                  # comando RES
(IF (3 5 <) (1.0 2.0 +) (3.0 4.0 *))  # tomada de decisão
(0 MEM CONT)             # inicializa contador
(WHILE (CONT 5 <) (1 1 +))            # laço WHILE
(FOR 0 3 I (1 2 +))                   # laço FOR
(END)
```

### 6.1 Derivação (sequência de produções aplicadas)

68 produções foram aplicadas, na seguinte ordem:

```
 1.  programa     -> LPAREN KW_START RPAREN linhas
 2.  linhas       -> LPAREN linhas_rest
 3.  linhas_rest  -> corpo RPAREN linhas
 4.  corpo        -> REAL resto_corpo
 5.  resto_corpo  -> operando operador_arit
 6.  operando     -> REAL
 7.  operador_arit-> OP_SUM
 8.  linhas       -> LPAREN linhas_rest
 9.  linhas_rest  -> corpo RPAREN linhas
10.  corpo        -> INT resto_corpo
11.  resto_corpo  -> operando operador_arit
12.  operando     -> INT
13.  operador_arit-> OP_SUB
14.  linhas       -> LPAREN linhas_rest
15.  linhas_rest  -> corpo RPAREN linhas
16.  corpo        -> REAL resto_corpo
17.  resto_corpo  -> KW_MEM MEM_ID
18.  linhas       -> LPAREN linhas_rest
19.  linhas_rest  -> corpo RPAREN linhas
20.  corpo        -> MEM_ID cauda_mem
21.  cauda_mem    -> ε
22.  linhas       -> LPAREN linhas_rest
23.  linhas_rest  -> corpo RPAREN linhas
24.  corpo        -> INT resto_corpo
25.  resto_corpo  -> KW_RES
26.  linhas       -> LPAREN linhas_rest
27.  linhas_rest  -> corpo RPAREN linhas
28.  corpo        -> KW_IF condicao linha linha
29.  condicao     -> LPAREN operando operando op_rel RPAREN
30.  operando     -> INT
31.  operando     -> INT
32.  op_rel       -> OP_LT
33.  linha        -> LPAREN corpo RPAREN
34.  corpo        -> REAL resto_corpo
35.  resto_corpo  -> operando operador_arit
36.  operando     -> REAL
37.  operador_arit-> OP_SUM
38.  linha        -> LPAREN corpo RPAREN
39.  corpo        -> REAL resto_corpo
40.  resto_corpo  -> operando operador_arit
41.  operando     -> REAL
42.  operador_arit-> OP_MUL
43.  linhas       -> LPAREN linhas_rest
44.  linhas_rest  -> corpo RPAREN linhas
45.  corpo        -> INT resto_corpo
46.  resto_corpo  -> KW_MEM MEM_ID
47.  linhas       -> LPAREN linhas_rest
48.  linhas_rest  -> corpo RPAREN linhas
49.  corpo        -> KW_WHILE condicao linha
50.  condicao     -> LPAREN operando operando op_rel RPAREN
51.  operando     -> MEM_ID
52.  operando     -> INT
53.  op_rel       -> OP_LT
54.  linha        -> LPAREN corpo RPAREN
55.  corpo        -> INT resto_corpo
56.  resto_corpo  -> operando operador_arit
57.  operando     -> INT
58.  operador_arit-> OP_SUM
59.  linhas       -> LPAREN linhas_rest
60.  linhas_rest  -> corpo RPAREN linhas
61.  corpo        -> KW_FOR INT INT MEM_ID linha
62.  linha        -> LPAREN corpo RPAREN
63.  corpo        -> INT resto_corpo
64.  resto_corpo  -> operando operador_arit
65.  operando     -> INT
66.  operador_arit-> OP_SUM
67.  linhas       -> LPAREN linhas_rest
68.  linhas_rest  -> KW_END RPAREN
```

### 6.2 Árvore Sintática (representação textual indentada)

Cada linha mostra um nó da árvore. Não-terminais aparecem como `símbolo -> produção` e folhas terminais aparecem como `TIPO: 'lexema' (linha N)`.

```text
programa -> LPAREN KW_START RPAREN linhas
  LPAREN: '(' (linha 1)
  KW_START: 'START' (linha 1)
  RPAREN: ')' (linha 1)
  linhas -> LPAREN linhas_rest
    LPAREN: '(' (linha 2)
    linhas_rest -> corpo RPAREN linhas
      corpo -> REAL resto_corpo
        REAL: '3.0' (linha 2)
        resto_corpo -> operando operador_arit
          operando -> REAL
            REAL: '4.0' (linha 2)
          operador_arit -> OP_SUM
            OP_SUM: '+' (linha 2)
      RPAREN: ')' (linha 2)
      linhas -> LPAREN linhas_rest
        LPAREN: '(' (linha 3)
        linhas_rest -> corpo RPAREN linhas
          corpo -> INT resto_corpo
            INT: '10' (linha 3)
            resto_corpo -> operando operador_arit
              operando -> INT
                INT: '2' (linha 3)
              operador_arit -> OP_SUB
                OP_SUB: '-' (linha 3)
          RPAREN: ')' (linha 3)
          linhas -> LPAREN linhas_rest
            LPAREN: '(' (linha 4)
            linhas_rest -> corpo RPAREN linhas
              corpo -> REAL resto_corpo
                REAL: '42.5' (linha 4)
                resto_corpo -> KW_MEM MEM_ID
                  KW_MEM: 'MEM' (linha 4)
                  MEM_ID: 'VAL' (linha 4)
              RPAREN: ')' (linha 4)
              linhas -> LPAREN linhas_rest
                LPAREN: '(' (linha 5)
                linhas_rest -> corpo RPAREN linhas
                  corpo -> MEM_ID cauda_mem
                    MEM_ID: 'VAL' (linha 5)
                    cauda_mem -> ε
                  RPAREN: ')' (linha 5)
                  linhas -> LPAREN linhas_rest
                    LPAREN: '(' (linha 6)
                    linhas_rest -> corpo RPAREN linhas
                      corpo -> INT resto_corpo
                        INT: '1' (linha 6)
                        resto_corpo -> KW_RES
                          KW_RES: 'RES' (linha 6)
                      RPAREN: ')' (linha 6)
                      linhas -> LPAREN linhas_rest
                        LPAREN: '(' (linha 7)
                        linhas_rest -> corpo RPAREN linhas
                          corpo -> KW_IF condicao linha linha
                            KW_IF: 'IF' (linha 7)
                            condicao -> LPAREN operando operando op_rel RPAREN
                              LPAREN: '(' (linha 7)
                              operando -> INT
                                INT: '3' (linha 7)
                              operando -> INT
                                INT: '5' (linha 7)
                              op_rel -> OP_LT
                                OP_LT: '<' (linha 7)
                              RPAREN: ')' (linha 7)
                            linha -> LPAREN corpo RPAREN
                              LPAREN: '(' (linha 7)
                              corpo -> REAL resto_corpo
                                REAL: '1.0' (linha 7)
                                resto_corpo -> operando operador_arit
                                  operando -> REAL
                                    REAL: '2.0' (linha 7)
                                  operador_arit -> OP_SUM
                                    OP_SUM: '+' (linha 7)
                              RPAREN: ')' (linha 7)
                            linha -> LPAREN corpo RPAREN
                              LPAREN: '(' (linha 7)
                              corpo -> REAL resto_corpo
                                REAL: '3.0' (linha 7)
                                resto_corpo -> operando operador_arit
                                  operando -> REAL
                                    REAL: '4.0' (linha 7)
                                  operador_arit -> OP_MUL
                                    OP_MUL: '*' (linha 7)
                              RPAREN: ')' (linha 7)
                          RPAREN: ')' (linha 7)
                          linhas -> LPAREN linhas_rest
                            LPAREN: '(' (linha 8)
                            linhas_rest -> corpo RPAREN linhas
                              corpo -> INT resto_corpo
                                INT: '0' (linha 8)
                                resto_corpo -> KW_MEM MEM_ID
                                  KW_MEM: 'MEM' (linha 8)
                                  MEM_ID: 'CONT' (linha 8)
                              RPAREN: ')' (linha 8)
                              linhas -> LPAREN linhas_rest
                                LPAREN: '(' (linha 9)
                                linhas_rest -> corpo RPAREN linhas
                                  corpo -> KW_WHILE condicao linha
                                    KW_WHILE: 'WHILE' (linha 9)
                                    condicao -> LPAREN operando operando op_rel RPAREN
                                      LPAREN: '(' (linha 9)
                                      operando -> MEM_ID
                                        MEM_ID: 'CONT' (linha 9)
                                      operando -> INT
                                        INT: '5' (linha 9)
                                      op_rel -> OP_LT
                                        OP_LT: '<' (linha 9)
                                      RPAREN: ')' (linha 9)
                                    linha -> LPAREN corpo RPAREN
                                      LPAREN: '(' (linha 9)
                                      corpo -> INT resto_corpo
                                        INT: '1' (linha 9)
                                        resto_corpo -> operando operador_arit
                                          operando -> INT
                                            INT: '1' (linha 9)
                                          operador_arit -> OP_SUM
                                            OP_SUM: '+' (linha 9)
                                      RPAREN: ')' (linha 9)
                                  RPAREN: ')' (linha 9)
                                  linhas -> LPAREN linhas_rest
                                    LPAREN: '(' (linha 10)
                                    linhas_rest -> corpo RPAREN linhas
                                      corpo -> KW_FOR INT INT MEM_ID linha
                                        KW_FOR: 'FOR' (linha 10)
                                        INT: '0' (linha 10)
                                        INT: '3' (linha 10)
                                        MEM_ID: 'I' (linha 10)
                                        linha -> LPAREN corpo RPAREN
                                          LPAREN: '(' (linha 10)
                                          corpo -> INT resto_corpo
                                            INT: '1' (linha 10)
                                            resto_corpo -> operando operador_arit
                                              operando -> INT
                                                INT: '2' (linha 10)
                                              operador_arit -> OP_SUM
                                                OP_SUM: '+' (linha 10)
                                          RPAREN: ')' (linha 10)
                                      RPAREN: ')' (linha 10)
                                      linhas -> LPAREN linhas_rest
                                        LPAREN: '(' (linha 11)
                                        linhas_rest -> KW_END RPAREN
                                          KW_END: 'END' (linha 11)
                                          RPAREN: ')' (linha 11)
```

### 6.3 Versão JSON da árvore

A versão completa em JSON da árvore sintática (com todos os tokens, suas linhas e produções aplicadas) está disponível em `saida/arvore.json` no repositório, e é regenerada a cada execução do programa por `gerarArvore.py`. O JSON é o formato canônico utilizado pelas fases seguintes do compilador (geração de Assembly).

---

## 7. Como reproduzir esta documentação

Os dados desta documentação são reprodutíveis a partir do código-fonte:

```bash
# Imprime gramática + FIRST + FOLLOW + tabela LL(1)
python src/construirGramatica.py

# Executa o pipeline e produz saida/arvore.json + saida/derivacao.json
python src/main.py teste_doc.txt
```

A função `construirGramatica()` calcula tudo automaticamente; portanto, qualquer alteração nas regras de produção em `src/construirGramatica.py` reflete imediatamente nos conjuntos FIRST/FOLLOW e na tabela LL(1).