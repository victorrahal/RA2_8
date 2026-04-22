# Saída de Validação — `construirGramatica.py`

Gerado automaticamente ao executar `python src/construirGramatica.py`.

```
======================================================================
GRAMÁTICA (regras de produção)
======================================================================
  programa  ::=  LPAREN KW_START RPAREN linhas
  linhas  ::=  LPAREN linhas_rest
  linhas_rest  ::=  KW_END RPAREN | corpo RPAREN linhas
  linha  ::=  LPAREN corpo RPAREN
  corpo  ::=  KW_IF condicao linha linha | KW_WHILE condicao linha | KW_FOR INT INT MEM_ID linha | INT resto_corpo | REAL resto_corpo | MEM_ID cauda_mem | linha resto_corpo
  cauda_mem  ::=  ε | resto_corpo
  resto_corpo  ::=  KW_RES | KW_MEM MEM_ID | operando operador_arit
  operando  ::=  INT | REAL | MEM_ID | linha
  operador_arit  ::=  OP_SUM | OP_SUB | OP_MUL | OP_DIVR | OP_DIVI | OP_MOD | OP_POW
  condicao  ::=  LPAREN operando operando op_rel RPAREN
  op_rel  ::=  OP_LT | OP_GT | OP_LE | OP_GE | OP_EQ | OP_NE

======================================================================
FIRST
======================================================================
  FIRST(cauda_mem) = { INT, KW_MEM, KW_RES, LPAREN, MEM_ID, REAL, ε }
  FIRST(condicao) = { LPAREN }
  FIRST(corpo) = { INT, KW_FOR, KW_IF, KW_WHILE, LPAREN, MEM_ID, REAL }
  FIRST(linha) = { LPAREN }
  FIRST(linhas) = { LPAREN }
  FIRST(linhas_rest) = { INT, KW_END, KW_FOR, KW_IF, KW_WHILE, LPAREN, MEM_ID, REAL }
  FIRST(op_rel) = { OP_EQ, OP_GE, OP_GT, OP_LE, OP_LT, OP_NE }
  FIRST(operador_arit) = { OP_DIVI, OP_DIVR, OP_MOD, OP_MUL, OP_POW, OP_SUB, OP_SUM }
  FIRST(operando) = { INT, LPAREN, MEM_ID, REAL }
  FIRST(programa) = { LPAREN }
  FIRST(resto_corpo) = { INT, KW_MEM, KW_RES, LPAREN, MEM_ID, REAL }

======================================================================
FOLLOW
======================================================================
  FOLLOW(cauda_mem) = { RPAREN }
  FOLLOW(condicao) = { LPAREN }
  FOLLOW(corpo) = { RPAREN }
  FOLLOW(linha) = { INT, KW_MEM, KW_RES, LPAREN, MEM_ID, OP_DIVI, OP_DIVR, OP_EQ, OP_GE, OP_GT, OP_LE, OP_LT, OP_MOD, OP_MUL, OP_NE, OP_POW, OP_SUB, OP_SUM, REAL, RPAREN }
  FOLLOW(linhas) = { $ }
  FOLLOW(linhas_rest) = { $ }
  FOLLOW(op_rel) = { RPAREN }
  FOLLOW(operador_arit) = { RPAREN }
  FOLLOW(operando) = { INT, LPAREN, MEM_ID, OP_DIVI, OP_DIVR, OP_EQ, OP_GE, OP_GT, OP_LE, OP_LT, OP_MOD, OP_MUL, OP_NE, OP_POW, OP_SUB, OP_SUM, REAL }
  FOLLOW(programa) = { $ }
  FOLLOW(resto_corpo) = { RPAREN }

======================================================================
TABELA LL(1) — entradas (nao_terminal, terminal) -> produção
======================================================================
  M[cauda_mem     , INT       ] = cauda_mem -> resto_corpo
  M[cauda_mem     , KW_MEM    ] = cauda_mem -> resto_corpo
  M[cauda_mem     , KW_RES    ] = cauda_mem -> resto_corpo
  M[cauda_mem     , LPAREN    ] = cauda_mem -> resto_corpo
  M[cauda_mem     , MEM_ID    ] = cauda_mem -> resto_corpo
  M[cauda_mem     , REAL      ] = cauda_mem -> resto_corpo
  M[cauda_mem     , RPAREN    ] = cauda_mem -> ε
  M[condicao      , LPAREN    ] = condicao -> LPAREN operando operando op_rel RPAREN
  M[corpo         , INT       ] = corpo -> INT resto_corpo
  M[corpo         , KW_FOR    ] = corpo -> KW_FOR INT INT MEM_ID linha
  M[corpo         , KW_IF     ] = corpo -> KW_IF condicao linha linha
  M[corpo         , KW_WHILE  ] = corpo -> KW_WHILE condicao linha
  M[corpo         , LPAREN    ] = corpo -> linha resto_corpo
  M[corpo         , MEM_ID    ] = corpo -> MEM_ID cauda_mem
  M[corpo         , REAL      ] = corpo -> REAL resto_corpo
  M[linha         , LPAREN    ] = linha -> LPAREN corpo RPAREN
  M[linhas        , LPAREN    ] = linhas -> LPAREN linhas_rest
  M[linhas_rest   , INT       ] = linhas_rest -> corpo RPAREN linhas
  M[linhas_rest   , KW_END    ] = linhas_rest -> KW_END RPAREN
  M[linhas_rest   , KW_FOR    ] = linhas_rest -> corpo RPAREN linhas
  M[linhas_rest   , KW_IF     ] = linhas_rest -> corpo RPAREN linhas
  M[linhas_rest   , KW_WHILE  ] = linhas_rest -> corpo RPAREN linhas
  M[linhas_rest   , LPAREN    ] = linhas_rest -> corpo RPAREN linhas
  M[linhas_rest   , MEM_ID    ] = linhas_rest -> corpo RPAREN linhas
  M[linhas_rest   , REAL      ] = linhas_rest -> corpo RPAREN linhas
  M[op_rel        , OP_EQ     ] = op_rel -> OP_EQ
  M[op_rel        , OP_GE     ] = op_rel -> OP_GE
  M[op_rel        , OP_GT     ] = op_rel -> OP_GT
  M[op_rel        , OP_LE     ] = op_rel -> OP_LE
  M[op_rel        , OP_LT     ] = op_rel -> OP_LT
  M[op_rel        , OP_NE     ] = op_rel -> OP_NE
  M[operador_arit , OP_DIVI   ] = operador_arit -> OP_DIVI
  M[operador_arit , OP_DIVR   ] = operador_arit -> OP_DIVR
  M[operador_arit , OP_MOD    ] = operador_arit -> OP_MOD
  M[operador_arit , OP_MUL    ] = operador_arit -> OP_MUL
  M[operador_arit , OP_POW    ] = operador_arit -> OP_POW
  M[operador_arit , OP_SUB    ] = operador_arit -> OP_SUB
  M[operador_arit , OP_SUM    ] = operador_arit -> OP_SUM
  M[operando      , INT       ] = operando -> INT
  M[operando      , LPAREN    ] = operando -> linha
  M[operando      , MEM_ID    ] = operando -> MEM_ID
  M[operando      , REAL      ] = operando -> REAL
  M[programa      , LPAREN    ] = programa -> LPAREN KW_START RPAREN linhas
  M[resto_corpo   , INT       ] = resto_corpo -> operando operador_arit
  M[resto_corpo   , KW_MEM    ] = resto_corpo -> KW_MEM MEM_ID
  M[resto_corpo   , KW_RES    ] = resto_corpo -> KW_RES
  M[resto_corpo   , LPAREN    ] = resto_corpo -> operando operador_arit
  M[resto_corpo   , MEM_ID    ] = resto_corpo -> operando operador_arit
  M[resto_corpo   , REAL      ] = resto_corpo -> operando operador_arit

✔ Gramática validada como LL(1) (sem conflitos na tabela).
```
