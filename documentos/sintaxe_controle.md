# Sintaxe das Estruturas de Controle

## IF

Executa um de dois blocos dependendo de uma condição booleana.

```
( IF <condicao> <linha_verdadeiro> <linha_falso> )
```

- `<condicao>` — expressão relacional entre dois operandos
- `<linha_verdadeiro>` — bloco executado se a condição for verdadeira
- `<linha_falso>` — bloco executado se a condição for falsa

**Exemplo:**
```
( IF ( 3 2 < ) ( 1 2 + ) ( 4 5 + ) )
```
Se 3 < 2 (falso), executa `(4 5 +)`, que resulta em 9.

---

## WHILE

Repete um bloco enquanto a condição for verdadeira.

```
( WHILE <condicao> <linha> )
```

- `<condicao>` — expressão relacional verificada a cada iteração
- `<linha>` — bloco executado enquanto a condição for verdadeira

**Exemplo:**
```
( WHILE ( 1 10 < ) ( 1 2 + ) )
```
Enquanto 1 < 10, executa `(1 2 +)`.

---

## FOR

Itera um número fixo de vezes entre dois valores inteiros, armazenando o contador em uma variável de memória.

```
( FOR <inicio> <fim> <MEM_ID> <linha> )
```

- `<inicio>` — valor inteiro inicial do contador
- `<fim>` — valor inteiro final do contador (exclusive)
- `<MEM_ID>` — identificador de memória que recebe o valor do contador a cada iteração
- `<linha>` — bloco executado a cada iteração

**Exemplo:**
```
( FOR 0 5 I ( 2 3 * ) )
```
Itera de 0 a 4 (5 iterações), salvando o contador em `I` e executando `(2 3 *)` a cada vez.

---

## Condição

As condições usadas em IF e WHILE seguem o formato:

```
( <operando> <operando> <op_rel> )
```

| Operador | Token   | Significado       |
|----------|---------|-------------------|
| `<`      | OP_LT   | menor que         |
| `>`      | OP_GT   | maior que         |
| `<=`     | OP_LE   | menor ou igual    |
| `>=`     | OP_GE   | maior ou igual    |
| `==`     | OP_EQ   | igual             |
| `!=`     | OP_NE   | diferente         |

**Exemplo:**
```
( 3 2 < )   → 3 < 2
( 10 10 == ) → 10 == 10
```
