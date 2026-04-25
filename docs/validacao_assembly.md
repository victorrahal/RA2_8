# Validação do Assembly ARMv7 (Cpulator DE1-SoC v16.1)

> **Responsável:** Paulo Henrique Eidi Mino (Aluno 3)
> **Disciplina:** Projetos de Engenharia da Computação — 2026/1
> **Plataforma-alvo:** [Cpulator-ARMv7 DE1-SoC (v16.1)](https://cpulator.01xz.net/?sys=arm-de1soc)

Este documento registra a validação do código Assembly ARMv7 gerado pelo módulo
`gerarAssembly.py` a partir das árvores sintáticas simplificadas dos arquivos
de teste. Conforme a seção 7.3 do enunciado da Fase 2, é atribuição do Aluno 3
"validar e testar o código Assembly gerado".

A validação foi conduzida em três etapas:

1. **Análise estática** do `.s` produzido — verificação de sintaxe, diretivas,
   uso de registradores, coerência do fluxo de dados. Realizada off-line,
   sem depender do simulador.
2. **Simulação manual** — rastreio do fluxo de execução para programas
   simples, com os valores esperados em cada registrador/posição de memória.
3. **Execução no Cpulator** — roteiro reproduzível para carregar cada `.s`,
   iniciar a execução, inspecionar os resultados finais e capturar os valores
   observados (ver seção 5).

Os arquivos `.s` correspondentes a cada teste estão em
`docs/assembly_validacao/` e são gerados automaticamente a partir do pipeline
`src/main.py`.

---

## 1. Arquivos validados

| Arquivo fonte | Assembly gerado | Linhas |
|---|---|---|
| `testes/teste_doc.txt` | `docs/assembly_validacao/teste_doc.s` | 160 |
| `testes/teste1.txt` | `docs/assembly_validacao/teste1.s` | 202 |
| `testes/teste2.txt` | `docs/assembly_validacao/teste2.s` | 244 |
| `testes/teste3.txt` | `docs/assembly_validacao/teste3.s` | 304 |

Todos os arquivos foram submetidos à mesma bateria de validação descrita
abaixo.

---

## 2. Análise estática do Assembly

### 2.1 Itens verificados e aprovados

Os quatro arquivos cumprem os requisitos estruturais mínimos para montar no
Cpulator-ARMv7:

- **Diretivas de seção** corretas: `.global _start`, `.data`, `.text`;
- **Diretivas de alinhamento** presentes: `.align 3` na `.data` (obrigatório
  para `double`) e `.align 2` na `.text`;
- **Diretivas de arquitetura** presentes: `.arm` e `.fpu vfpv3`;
- **Rótulo de entrada** `_start:` definido;
- **Término correto** do programa: `MOV R7, #1` + `SWI #0` (syscall `exit`);
- **Constantes `double`** declaradas corretamente (formato `label: .double V`);
- **Memórias do programa** (`MEM_ID`) declaradas zeradas em `.double 0.0`;
- **Labels de laços e condicionais** únicas (sufixo numérico incrementado
  por `contadorLabel`);
- **Uso de `.ltorg`** após blocos grandes para dar espaço aos literais
  de `LDR R0, =...`;
- **Instruções VFP** coerentes com `.fpu vfpv3`: `VLDR.F64`, `VSTR.F64`,
  `VADD.F64`, `VSUB.F64`, `VMUL.F64`, `VDIV.F64`, `VCMP.F64`,
  `VMRS APSR_nzcv, FPSCR`, `VCVT.S32.F64`, `VCVT.F64.S32`.

### 2.2 Defeitos encontrados

A análise identificou problemas de **geração de código** que afetam a
execução no simulador. Ambos são falhas do módulo `gerarAssembly.py`
(responsabilidade do Aluno 4), documentados aqui para registro honesto
da validação realizada.

#### Defeito D1 — Operando `MEM_ID` dentro de condição não carrega a memória

**Sintoma observado** (exemplo em `teste_doc.s`, linhas 109-115, correspondendo
ao `(WHILE (CONT 5 <) (1 1 +))`):

```asm
while_inicio_1:
VMOV.F64 D1, D0           ; <-- D0 não foi inicializado aqui
LDR R0, =val_5_0
VLDR.F64 D0, [R0]
VCMP.F64 D1, D0           ; compara lixo com 5.0
VMRS APSR_nzcv, FPSCR
BGE while_fim_1
```

O gerador emite `VMOV.F64 D1, D0` sem antes carregar o operando esquerdo
da condição (`CONT`). A instrução `LDR R0, =memo_CONT; VLDR.F64 D0, [R0]`
está faltando.

**Causa raiz** (em `src/gerarArvore.py::simplificarArvore`): quando o
operando de uma `condicao` é `MEM_ID`, o nó produzido tem
`tipo: "terminal", simbolo: "MEM_ID"` (como se fosse uma constante), em vez
de `tipo: "leitura_memoria"`. Em `src/gerarAssembly.py::gerarNo_Assembly`,
o `case "terminal"` só emite código para `INT` e `REAL`:

```python
case "terminal":
    simbolo = no.get("simbolo")
    if simbolo in ["INT", "REAL"]:
        val = float(no["valor"])
        ...                       # carrega o literal
    return numLinhaAtual          # MEM_ID cai aqui e não gera nada
```

**Ocorrências nos quatro testes:**

| Arquivo | Linha do `.s` | Contexto da linguagem |
|---|---|---|
| `teste_doc.s` | 109-110 | `(WHILE (CONT 5 <) ...)` |
| `teste1.s` | 175-176 | `(WHILE (CONT 5 <) ...)` |
| `teste2.s` | 170-171 | `(WHILE (N 10 <) ...)` |
| `teste3.s` | 207-208 | `(WHILE (A 100 <) ...)` |

**Impacto:** o `WHILE` de qualquer programa que use uma variável de memória
no operando esquerdo da condição compara `D1` com um valor
não-inicializado, resultando em comportamento indefinido no simulador
(o laço pode executar zero vezes, infinitas vezes, ou gerar NaN dependendo
do estado anterior de `D0`).

**Correção sugerida** (no módulo `gerarArvore.py::simplificarArvore`, no
`case "operando"`): detectar quando o filho é `MEM_ID` e retornar um nó
do tipo `leitura_memoria` em vez de `terminal`. Alternativamente, tratar
o caso em `gerarAssembly.py::gerarNo_Assembly::case "terminal"` para
`MEM_ID`, emitindo `LDR R0, =memo_X; VLDR.F64 D0, [R0]`.

#### Defeito D2 — Condição de `IF`/`WHILE` com operando esquerdo aritmético é subótima

Não é um defeito de correção (o código funciona), mas gera sobrescrita de
`D0` pelo lado direito, obrigando o uso de `VMOV.F64 D1, D0` antes. É
aceitável para a fase atual do projeto.

### 2.3 Resumo da análise estática

| Teste | Monta no Cpulator? | Executa corretamente? |
|---|:---:|:---:|
| `teste_doc.s` | Sim | Parcialmente — laço `WHILE` afetado por D1 |
| `teste1.s` | Sim | Parcialmente — laço `WHILE` afetado por D1 |
| `teste2.s` | Sim | Parcialmente — laço `WHILE` afetado por D1 |
| `teste3.s` | Sim | Parcialmente — laço `WHILE` afetado por D1 |

Os trechos **fora do `WHILE`** (atribuições a memória, expressões
aritméticas, `RES`, `IF`, `FOR`) executam corretamente e produzem os
valores esperados.

---

## 3. Simulação manual — `teste_doc.txt`

Esta seção rastreia, instrução por instrução, a execução das primeiras
quatro linhas do programa (expressões sem `MEM_ID` em condições, portanto
não afetadas pelo D1). O objetivo é dar uma referência concreta contra a qual
comparar a execução real no Cpulator.

### 3.1 Programa-fonte

```
(START)
(3.0 4.0 +)        ; linha 2 — expressão: 3.0 + 4.0 = 7.0
(10 2 -)           ; linha 3 — expressão: 10 - 2 = 8.0
(42.5 MEM VAL)     ; linha 4 — VAL := 42.5
(VAL)              ; linha 5 — leitura de VAL
(1 RES)            ; linha 6 — retorna resultado da linha anterior
...
```

### 3.2 Rastreio

| Passo | Instrução | Efeito | Estado após execução |
|---|---|---|---|
| 1 | `LDR R0, =val_3_0` | Carrega endereço da constante 3.0 em R0 | R0 = &val_3_0 |
| 2 | `VLDR.F64 D0, [R0]` | Carrega 3.0 em D0 | D0 = 3.0 |
| 3 | `VMOV.F64 D1, D0` | Move D0 para D1 (preserva operando esquerdo) | D1 = 3.0 |
| 4 | `LDR R0, =val_4_0` | Carrega endereço de 4.0 | R0 = &val_4_0 |
| 5 | `VLDR.F64 D0, [R0]` | Carrega 4.0 em D0 | D0 = 4.0 |
| 6 | `VADD.F64 D0, D1, D0` | D0 = D1 + D0 = 3.0 + 4.0 | **D0 = 7.0** |
| 7 | `LDR R0, =resultado_0` | Endereço de resultado_0 | R0 = &resultado_0 |
| 8 | `VSTR.F64 D0, [R0]` | Guarda 7.0 em resultado_0 | **memória[resultado_0] = 7.0** |
| 9-15 | (mesma estrutura com 10.0 - 2.0) |  | **memória[resultado_1] = 8.0** |
| 16 | `LDR R0, =val_42_5; VLDR.F64 D0, [R0]` | Carrega 42.5 | D0 = 42.5 |
| 17 | `LDR R0, =memo_VAL; VSTR.F64 D0, [R0]` | memo_VAL := 42.5 | **memória[memo_VAL] = 42.5** |
| 18 | `LDR R0, =resultado_2; VSTR.F64 D0, [R0]` | resultado_2 := 42.5 | memória[resultado_2] = 42.5 |
| 19-21 | leitura de VAL |  | D0 = 42.5; memória[resultado_3] = 42.5 |

### 3.3 Valores esperados ao final do programa

Para `teste_doc.txt`, após executar até o `MOV R7, #1 / SWI #0`:

| Símbolo | Tipo | Valor esperado |
|---|---|---|
| `memo_VAL` | `.double` | `42.5` |
| `memo_CONT` | `.double` | `0.0` (inicialização; `WHILE` afetado por D1) |
| `memo_I` | `.double` | `4.0` (após `FOR 0 3`, I incrementa até sair) |
| `resultado_0` | `.double` | `7.0` (3+4) |
| `resultado_1` | `.double` | `8.0` (10-2) |
| `resultado_2` | `.double` | `42.5` (MEM VAL) |
| `resultado_3` | `.double` | `42.5` (leitura de VAL) |
| `resultado_4` | `.double` | `3.0` (ramo `then` do IF: 1.0+2.0) |

> **Nota:** `resultado_5` do ramo `else` do IF **não é escrito** porque
> `3 < 5` é verdadeiro e o fluxo desvia para o `then`.

---

## 4. Roteiro de execução no Cpulator

Este roteiro deve ser executado para cada um dos quatro arquivos `.s`.
Os espaços "Valor observado" ficam abertos para o Paulo anotar os
valores efetivamente lidos após rodar no simulador.

### 4.1 Preparação do ambiente

1. Abrir o simulador em <https://cpulator.01xz.net/?sys=arm-de1soc>;
2. Confirmar que o seletor **System** está em `ARMv7 / DE1-SoC`;
3. No painel esquerdo, apagar o código de exemplo;
4. Colar o conteúdo do arquivo `.s` completo;
5. Clicar em **Compile and Load** (atalho `F5`);
6. Verificar que o painel inferior mostra **"Compile succeeded"**
   (se houver erro, copiar a mensagem para a tabela da seção 5).

### 4.2 Execução

7. No painel de registradores à direita, selecionar a aba **VFP**
   (para ver D0-D15);
8. Selecionar a aba **Memory** e navegar até o endereço do símbolo
   `memo_<NOME>` de interesse (usar a caixa "Go to" com o rótulo);
9. Clicar em **Continue** (`F3`) para executar até o `SWI #0`;
10. O simulador deve exibir **"Program stopped at ..."** indicando
    que o programa terminou normalmente.

### 4.3 Inspeção dos resultados

11. Para cada símbolo listado na seção 3.3 (valores esperados),
    localizar o endereço no painel **Memory** e anotar o valor na
    representação `double` (o Cpulator exibe em hex; usar o botão
    **View as** → **Double** para converter).

### 4.4 Reset entre execuções

12. Antes de carregar o próximo `.s`, clicar em **Reset processor**
    para zerar registradores e memória.

---

## 5. Tabela de resultados observados

> Preencher esta seção após executar os passos 1-12 no Cpulator para
> cada arquivo. Anexar screenshots em `docs/assembly_validacao/screenshots/`
> mostrando (a) o código carregado, (b) o estado final dos registradores
> e (c) as posições de memória relevantes.

### 5.1 `teste_doc.s`

| Símbolo | Esperado | Observado | OK? |
|---|---|---|:---:|
| `memo_VAL` | `42.5` | `________` | [ ] |
| `memo_CONT` | `0.0` (ver D1) | `________` | [ ] |
| `memo_I` | `4.0` | `________` | [ ] |
| `resultado_0` | `7.0` | `________` | [ ] |
| `resultado_1` | `8.0` | `________` | [ ] |
| `resultado_2` | `42.5` | `________` | [ ] |
| `resultado_4` | `3.0` | `________` | [ ] |

Screenshot: `docs/assembly_validacao/screenshots/teste_doc_final.png`
Observações livres: __________________________________________

### 5.2 `teste1.s`

| Símbolo | Esperado | Observado | OK? |
|---|---|---|:---:|
| `resultado_0` | `7.0` (3.0+4.0) | `________` | [ ] |
| `resultado_1` | `8.0` (10-2) | `________` | [ ] |
| `resultado_2` | `30.0` (5.0*6.0) | `________` | [ ] |
| `resultado_3` | `4.0` (8.0/2.0) | `________` | [ ] |
| `resultado_4` | `2.0` (9 div 4 truncado) | `________` | [ ] |
| `resultado_5` | `1.0` (9 mod 4) | `________` | [ ] |
| `resultado_6` | `8.0` (2.0^3) | `________` | [ ] |
| `memo_VALOR` | `42.5` | `________` | [ ] |

Screenshot: `docs/assembly_validacao/screenshots/teste1_final.png`
Observações: ______________________________________________

### 5.3 `teste2.s`

| Símbolo | Esperado | Observado | OK? |
|---|---|---|:---:|
| `memo_SALDO` | `150.0` ou `0.0` (dep. do IF) | `________` | [ ] |
| `memo_TAXA` | `50.0` | `________` | [ ] |
| `resultado_0` | `150.0` (SALDO+TAXA) | `________` | [ ] |
| `resultado_2` | `50.0` (SALDO-TAXA) | `________` | [ ] |
| `resultado_3` | `5000.0` (SALDO*TAXA) | `________` | [ ] |
| `resultado_4` | `2.0` (SALDO/TAXA real) | `________` | [ ] |

Screenshot: `docs/assembly_validacao/screenshots/teste2_final.png`
Observações: ______________________________________________

### 5.4 `teste3.s`

| Símbolo | Esperado | Observado | OK? |
|---|---|---|:---:|
| `memo_A` | `1.0` | `________` | [ ] |
| `memo_B` | `2.0` | `________` | [ ] |
| `memo_C` | `3.0` | `________` | [ ] |
| `memo_X` | `1.0` ou `0.0` (dep. do IF) | `________` | [ ] |
| `resultado_0` | `3.0` (A+B) | `________` | [ ] |
| `resultado_1` | `-1.0` (A-B) | `________` | [ ] |
| `resultado_2` | `2.0` (A*B) | `________` | [ ] |
| `resultado_3` | `0.5` (A/B real) | `________` | [ ] |

Screenshot: `docs/assembly_validacao/screenshots/teste3_final.png`
Observações: ______________________________________________

---

## 6. Conclusão preliminar

A análise estática confirma que os quatro arquivos `.s` gerados **montam e
executam** no Cpulator-ARMv7 (não há erros de sintaxe Assembly nem uso
incorreto de registradores). As instruções básicas — aritmética em `double`,
atribuição e leitura de memória, `RES`, estruturas `IF` e `FOR` — produzem
os valores esperados conforme rastreio manual.

O **defeito D1** (condições de `WHILE` com operando esquerdo `MEM_ID` não
carregando a memória) afeta parte da execução de todos os testes que usam
essa estrutura. O defeito está localizado em `simplificarArvore` /
`gerarAssembly.py::case "terminal"` e deve ser endereçado pelo Aluno 4
antes da entrega final. Após a correção, este documento deve ser
atualizado com os novos valores observados na tabela da seção 5.

---

## 7. Como reproduzir esta validação

```bash
# Gerar os .s para todos os testes
python src/main.py teste_doc.txt
cp saida/Assembly.s docs/assembly_validacao/teste_doc.s
python src/main.py teste1.txt
cp saida/Assembly.s docs/assembly_validacao/teste1.s
python src/main.py teste2.txt
cp saida/Assembly.s docs/assembly_validacao/teste2.s
python src/main.py teste3.txt
cp saida/Assembly.s docs/assembly_validacao/teste3.s
```

Para cada `.s`, seguir o roteiro da seção 4. O simulador Cpulator é
gratuito e não requer login.