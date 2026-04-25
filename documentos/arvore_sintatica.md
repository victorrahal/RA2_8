# Parser, Árvore Sintática

> **Projeto:** Analisador Sintático — Fase 2
> **Disciplina:** Projetos de Engenharia da Computação — 2026/1
> **Instituição:** PUCPR — Pontifícia Universidade Católica do Paraná
> **Responsável pelo módulo:** João Henrique Tomaz Dutra - Aluno 2
> **Grupo no Canvas:** `RA2_8`

Documento descreve a implantação do parser, utilizando da tabela LL(1)
fornescida pelo arquivo 'construirGramatica.py' e pelos tokens gerados
por 'lerTokens.py'

---

- **Valida uma sequência de tokens**
- **Gera a derivação da gramática**
- **Construir uma árvore sintática**
- **Detecta e reporta erros sintáticos**

---

-> Inicialmente define a classe No, preparando para a montagem da árvore em si
traz simbolo (da gramática), tipo do nó (terminal ou não), produção (regras), token(valores reais) e possíveis filhos.

-> Traz a classe validar_terminal para ver termos presentes ou não dentro da gramática.

-> Dentro da função de parsear, inicializa a pilha com $ e S, também implantando a pilha parelela só para a árvore, guardando em outra lista as derivações e o próprio lookahead.

-> Utiliza dos tipo dos tokens atuais e compara eles com o valor validado da tabela, caso ele seja terminal consome ele.

-> Caso ele seja não terminal ele faz consulta a tabela e monta a derivação, atualizando o nó e empilhando os símbolos, caso não exista dá erro sintático.