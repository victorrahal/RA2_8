# RA2_8 — Analisador Sintático

> **Disciplina:** Projetos de Engenharia da Computação — 2026/1
> **Instituição:** PUCPR — Pontifícia Universidade Católica do Paraná
> **Grupo no Canvas:** `RA2_8`

## Integrantes

- João Henrique Tomaz Dutra — [@Jhtomaz](https://github.com/Jhtomaz)
- Lucas Balint Vilar — [@lucasdxl](https://github.com/lucasdxl)
- Paulo Henrique Eidi Mino — [@phmino](https://github.com/phmino)
- Victor Rahal Basseto — [@victorrahal](https://github.com/victorrahal)

---

## 1. Objetivo

Implementar um analisador léxico e sintático em **Python** para uma linguagem em **notação polonesa reversa (RPN)**, com suporte a:

- Operações aritméticas em RPN: `+ - * | / % ^`
- Comandos especiais: `RES`, `MEM`
- Estruturas de controle: `IF`, `WHILE`, `FOR`
- Geração de árvore sintática
- Geração de código Assembly (ARMv7)

O parser é **descendente recursivo do tipo LL(1)**, guiado por uma tabela de análise.

---

## 2. Como executar

### Pré-requisitos
- Python 3.10 ou superior
- (Opcional) `graphviz` para gerar a imagem da árvore: `pip install graphviz`

### Executando o programa

```bash
python src/main.py teste1.txt
```

O programa procura o arquivo dentro da pasta `testes/`. Os arquivos de teste fornecidos são:
- `teste1.txt`, `teste2.txt`, `teste3.txt` — programas válidos
- `teste_doc.txt` — programa enxuto usado como exemplo na documentação (`docs/gramatica.md`)
- `teste_erroLexico.txt`, `teste_erroSintatico.txt` — programas inválidos

### Saída

Após a execução, são gerados na pasta `saida/`:
- `derivacao.json` — derivações da gramática
- `arvore.json` — árvore sintática completa
- `arvore_simplificada.json` — árvore reduzida usada para gerar Assembly
- `Assembly.s` — código Assembly ARMv7
- `arvore.png` — imagem da árvore (se `graphviz` estiver instalado)

---

## 3. Estrutura do projeto

```
RA2_8/
├── src/                      # Código-fonte
│   ├── main.py               # Ponto de entrada (Aluno 4)
│   ├── tokensConfig.py       # Configuração de tokens (Aluno 3)
│   ├── estadosLexicos.py     # Estados do lexer (Aluno 3)
│   ├── lerTokens.py          # Analisador léxico (Aluno 3)
│   ├── construirGramatica.py # Gramática + FIRST/FOLLOW + Tabela LL(1) (Aluno 1)
│   ├── parsear.py            # Parser descendente recursivo (Aluno 2)
│   ├── gerarArvore.py        # Construção da árvore sintática (Aluno 4)
│   └── gerarAssembly.py      # Geração de Assembly ARMv7 (Aluno 4)
├── testes/                   # Arquivos de entrada (.txt)
├── tests/                    # Testes unitários (Python unittest)
├── docs/                     # Documentação detalhada (gramática, FIRST/FOLLOW, tabela LL(1), árvore)
├── saida/                    # Arquivos gerados pela execução
└── README.md
```

---

## 4. Sintaxe da linguagem

Toda expressão é **totalmente parentizada** e segue notação **pós-fixada (RPN)**.

### Estrutura geral do programa

```
(START)
... linhas ...
(END)
```

### Expressões aritméticas

Formato: `(A B op)` — operadores binários em pós-fixo.

```
(3.0 4.0 +)        # soma
(10 2 -)           # subtração
(5.0 6.0 *)        # multiplicação
(8.0 2.0 |)        # divisão real
(9 4 /)            # divisão inteira
(9 4 %)            # resto
(2.0 3 ^)          # potenciação (expoente inteiro)
```

Expressões podem ser aninhadas sem limite:

```
((3.0 4.0 +) (5.0 6.0 *) |)
```

### Comandos especiais

| Comando         | Significado                                              |
|-----------------|----------------------------------------------------------|
| `(N RES)`       | Retorna o resultado da expressão N linhas anteriores     |
| `(V MEM NOME)`  | Armazena o valor V na memória `NOME`                     |
| `(NOME)`        | Lê o valor da memória `NOME` (retorna 0 se não inicial.) |

Nomes de memória usam **apenas letras maiúsculas latinas**.

### Estruturas de controle

Mantêm o padrão totalmente parentizado e pós-fixado:

```
(IF (cond) (then) (else))
(WHILE (cond) (corpo))
(FOR ini fim VAR (corpo))
```

Condições usam operadores relacionais em pós-fixo: `(A B <)`, `(A B >)`.

**Operadores relacionais suportados:** `<`, `>`.

> Operadores relacionais compostos (`<=`, `>=`, `==`, `!=`) **não** fazem
> parte da linguagem e seu uso gera erro léxico.

#### Exemplos

```
(IF (X 5 <) (1.0 2.0 +) (3.0 4.0 *))
(WHILE (CONT 10 <) ((CONT) 1 +))
(FOR 0 10 I ((I) 2 *))
```

---

## 5. Gramática (LL(1))

Símbolo inicial: **`programa`**. Não-terminais em minúsculas; terminais em MAIÚSCULAS.

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

op_rel         ::= OP_LT | OP_GT
```

### Decisões de fatoração

- **`linhas_rest`**: distingue `(END)` de uma nova linha pelo token seguinte ao `(`.
- **`cauda_mem`**: distingue `(MEM)` (consulta) de `MEM` como operando, olhando se vem `)` ou outro símbolo.
- **`corpo`** decide o caminho pelo primeiro token após `(`: keyword de controle, literal numérico, identificador de memória ou parêntese aninhado.

A função `construirGramatica()` calcula automaticamente os conjuntos **FIRST** e **FOLLOW** e constrói a tabela de análise. Em caso de conflito, levanta `ValueError`. Para inspecionar a saída completa (regras, FIRST, FOLLOW, tabela):

```bash
python src/construirGramatica.py
```

> **Documentação detalhada:** o arquivo [`docs/gramatica.md`](docs/gramatica.md) contém
> a versão completa exigida pelo enunciado (item 11.4): regras de produção em EBNF,
> conjuntos FIRST e FOLLOW de todos os não-terminais, tabela LL(1) completa e a
> árvore sintática gerada para o arquivo `testes/teste_doc.txt`.

---

## 6. Funcionamento do código

O `main.py` executa o pipeline na seguinte ordem:

1. **`lerTokens(arquivo)`** lê o arquivo e devolve uma lista de tokens (`tipo`, `valor`, `linha`). Implementado como máquina de estados em `estadosLexicos.py`.
2. **`construirGramatica()`** monta a gramática, calcula FIRST/FOLLOW e a tabela LL(1).
3. **`parsear(tokens, tabela, inicio)`** valida a sequência de tokens com um parser descendente recursivo guiado por tabela. Usa pilha de símbolos + pilha paralela de nós. Retorna a derivação e a árvore em formato JSON.
4. **`gerarArvore(derivacao)`** converte a derivação em uma árvore de objetos `No`.
5. **`simplificarArvore(arvore)`** reduz a árvore sintática para uma representação semântica (atribuições, leituras, expressões aritméticas, estruturas de controle).
6. **`gerarAssembly(arvore_simplificada)`** percorre a árvore simplificada e emite o código Assembly ARMv7.

### Tratamento de erros

- **Erro léxico**: caractere inesperado, identificador inválido, número malformado. Mensagem inclui número da linha.
- **Erro sintático**: token inesperado durante o parsing. Mensagem indica linha, símbolo esperado e símbolo encontrado.

---

## 7. Testes

Os testes unitários ficam em `tests/`:

```bash
python -m unittest tests/testconstruirgramatica.py
python -m unittest tests/testelerTokens.py
```

Os arquivos de entrada em `testes/` cobrem:
- Todas as operações aritméticas
- Todos os comandos especiais (`RES`, `MEM`)
- Pelo menos uma estrutura de controle e um laço
- Casos de erro léxico e sintático

---

## 8. Divisão de responsabilidades

| Aluno | Responsabilidade | Arquivos principais |
|-------|------------------|---------------------|
| Victor Rahal Basseto | Gramática, FIRST/FOLLOW, tabela LL(1) | `construirGramatica.py` |
| João Henrique Tomaz Dutra | Parser descendente recursivo | `parsear.py` |
| Paulo Henrique Eidi Mino | Analisador léxico, tokens, estruturas de controle | `lerTokens.py`, `estadosLexicos.py`, `tokensConfig.py` |
| Lucas Balint Vilar | Árvore sintática, geração de Assembly, integração | `gerarArvore.py`, `gerarAssembly.py`, `main.py` |