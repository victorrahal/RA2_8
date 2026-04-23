# Victor Rahal Basseto - Aluno 1

from collections import defaultdict

EPSILON = "ε"
EOF = "$"

TERMINAIS = {
    "LPAREN", "RPAREN",
    "INT", "REAL", "MEM_ID",
    # Operadores aritméticos
    "OP_SUM", "OP_SUB", "OP_MUL",
    "OP_DIVR", "OP_DIVI", "OP_MOD", "OP_POW",
    # Operadores relacionais 
    "OP_LT", "OP_GT", "OP_LE", "OP_GE", "OP_EQ", "OP_NE",
    # Palavras reservadas
    "KW_START", "KW_END",
    "KW_RES", "KW_MEM",
    "KW_IF", "KW_WHILE", "KW_FOR",
    EOF,
}

NAO_TERMINAIS = {
    "programa", "linhas", "linhas_rest",
    "linha",
    "expressao", "corpo", "resto_corpo",
    "cauda_mem",
    "operando", "operador_arit",
    "comando_especial",
    "estrutura_controle", "cond_if", "laco_while", "laco_for",
    "condicao", "op_rel",
}

INICIO = "programa"

GRAMATICA = {
    "programa": [
        ["LPAREN", "KW_START", "RPAREN", "linhas"],
    ],
    "linhas": [
        ["LPAREN", "linhas_rest"],
    ],
    "linhas_rest": [
        ["KW_END", "RPAREN"],
        ["corpo", "RPAREN", "linhas"],
    ],
    "linha": [
        ["LPAREN", "corpo", "RPAREN"],
    ],
    "corpo": [
        ["KW_IF", "condicao", "linha", "linha"],
        ["KW_WHILE", "condicao", "linha"],
        ["KW_FOR", "operando", "operando", "MEM_ID", "linha"],
        ["INT", "resto_corpo"],
        ["REAL", "resto_corpo"],
        ["MEM_ID", "cauda_mem"],
        ["linha", "resto_corpo"],
    ],
    "cauda_mem": [
        [EPSILON],
        ["resto_corpo"],
    ],
    "resto_corpo": [
        ["KW_RES"],
        ["KW_MEM", "MEM_ID"],
        ["operando", "operador_arit"],
    ],
    "operando": [
        ["INT"],
        ["REAL"],
        ["MEM_ID"],
        ["linha"],
    ],
    "operador_arit": [
        ["OP_SUM"], ["OP_SUB"], ["OP_MUL"],
        ["OP_DIVR"], ["OP_DIVI"], ["OP_MOD"], ["OP_POW"],
    ],
    "expressao": [
        ["LPAREN", "operando", "operando", "operador_arit", "RPAREN"],
    ],
    "comando_especial": [
        ["LPAREN", "INT", "KW_RES", "RPAREN"],
        ["LPAREN", "REAL", "KW_MEM", "MEM_ID", "RPAREN"],
        ["LPAREN", "INT",  "KW_MEM", "MEM_ID", "RPAREN"],
        ["LPAREN", "MEM_ID", "RPAREN"],
    ],
    "estrutura_controle": [
        ["cond_if"], ["laco_while"], ["laco_for"],
    ],
    "cond_if": [
        ["LPAREN", "KW_IF", "condicao", "linha", "linha", "RPAREN"],
    ],
    "laco_while": [
        ["LPAREN", "KW_WHILE", "condicao", "linha", "RPAREN"],
    ],
    "laco_for": [
        ["LPAREN", "KW_FOR", "operando", "operando", "MEM_ID", "linha", "RPAREN"],
    ],
    "condicao": [
        ["LPAREN", "operando", "operando", "op_rel", "RPAREN"],
    ],
    "op_rel": [
        ["OP_LT"], ["OP_GT"], ["OP_LE"],
        ["OP_GE"], ["OP_EQ"], ["OP_NE"],
    ],
}

NAO_TERMINAIS_ATIVOS = {
    "programa", "linhas", "linhas_rest", "linha",
    "corpo", "cauda_mem", "resto_corpo",
    "operando", "operador_arit",
    "condicao", "op_rel",
}

def eh_terminal(simbolo: str) -> bool:
    return simbolo in TERMINAIS or simbolo == EPSILON

def eh_nao_terminal(simbolo: str) -> bool:
    return simbolo in GRAMATICA

def calcularFirst(gramatica=GRAMATICA):
    first = defaultdict(set)
    for terminal in TERMINAIS:
        first[terminal] = {terminal}
    first[EPSILON] = {EPSILON}

    houve_mudanca = True
    while houve_mudanca:
        houve_mudanca = False
        for nao_terminal, producoes in gramatica.items():
            for producao in producoes:
                if producao == [EPSILON]:
                    if EPSILON not in first[nao_terminal]:
                        first[nao_terminal].add(EPSILON)
                        houve_mudanca = True
                    continue
                # Percorre cada símbolo da produção
                todos_anulaveis = True
                for simbolo in producao:
                    a_adicionar = first[simbolo] - {EPSILON}
                    if not a_adicionar.issubset(first[nao_terminal]):
                        first[nao_terminal] |= a_adicionar
                        houve_mudanca = True
                    if EPSILON not in first[simbolo]:
                        todos_anulaveis = False
                        break
                if todos_anulaveis:
                    if EPSILON not in first[nao_terminal]:
                        first[nao_terminal].add(EPSILON)
                        houve_mudanca = True
    return dict(first)

def firstDeCadeia(cadeia, first):
    """FIRST de uma sequência de símbolos."""
    resultado = set()
    if not cadeia:
        resultado.add(EPSILON)
        return resultado
    todos_anulaveis = True
    for simbolo in cadeia:
        resultado |= (first[simbolo] - {EPSILON})
        if EPSILON not in first[simbolo]:
            todos_anulaveis = False
            break
    if todos_anulaveis:
        resultado.add(EPSILON)
    return resultado

def calcularFollow(gramatica, first, inicio=INICIO):
    follow = defaultdict(set)
    follow[inicio].add(EOF)
    houve_mudanca = True
    while houve_mudanca:
        houve_mudanca = False
        for nao_terminal, producoes in gramatica.items():
            for producao in producoes:
                for i, simbolo in enumerate(producao):
                    if not eh_nao_terminal(simbolo):
                        continue
                    sufixo = producao[i + 1:]
                    first_sufixo = firstDeCadeia(sufixo, first)
                    # Adiciona FIRST(sufixo) \ {ε} ao FOLLOW do símbolo
                    a_adicionar = first_sufixo - {EPSILON}
                    if not a_adicionar.issubset(follow[simbolo]):
                        follow[simbolo] |= a_adicionar
                        houve_mudanca = True
                    # Se sufixo pode gerar ε, propaga FOLLOW do pai
                    if EPSILON in first_sufixo:
                        if not follow[nao_terminal].issubset(follow[simbolo]):
                            follow[simbolo] |= follow[nao_terminal]
                            houve_mudanca = True
    return dict(follow)

def construirTabelaLL1(gramatica, first, follow):
    tabela = {}
    conflitos = []
    for nao_terminal, producoes in gramatica.items():
        if nao_terminal not in NAO_TERMINAIS_ATIVOS:
            continue
        for producao in producoes:
            first_producao = firstDeCadeia(producao, first)
            # Para cada terminal em FIRST(producao) \ {ε}: M[A, t] = producao
            for terminal in first_producao - {EPSILON}:
                entrada = (nao_terminal, terminal)
                if entrada in tabela and tabela[entrada] != producao:
                    conflitos.append(
                        f"Conflito em M[{nao_terminal},{terminal}]: "
                        f"{tabela[entrada]} vs {producao}"
                    )
                tabela[entrada] = producao
            # Se ε ∈ FIRST(producao): para cada t em FOLLOW(A), M[A, t] = producao
            if EPSILON in first_producao:
                for terminal in follow[nao_terminal]:
                    entrada = (nao_terminal, terminal)
                    if entrada in tabela and tabela[entrada] != producao:
                        conflitos.append(
                            f"Conflito em M[{nao_terminal},{terminal}] (ε-regra): "
                            f"{tabela[entrada]} vs {producao}"
                        )
                    tabela[entrada] = producao
    return tabela, conflitos

def construirGramatica():
    first = calcularFirst(GRAMATICA)
    follow = calcularFollow(GRAMATICA, first, INICIO)
    tabela, conflitos = construirTabelaLL1(GRAMATICA, first, follow)
    if conflitos:
        raise ValueError(
            "Gramática NÃO é LL(1). Conflitos encontrados:\n  - "
            + "\n  - ".join(conflitos)
        )
    return {
        "gramatica": GRAMATICA,
        "terminais": TERMINAIS,
        "nao_terminais": NAO_TERMINAIS_ATIVOS,
        "inicio": INICIO,
        "first": first,
        "follow": follow,
        "tabela_ll1": tabela,
    }

def _format_conj(conj):
    return "{ " + ", ".join(sorted(conj)) + " }"

def _exibir_res(info):
    print("=" * 70)
    print("GRAMÁTICA (regras de produção)")
    print("=" * 70)
    for nao_terminal, prods in info["gramatica"].items():
        alternativas = " | ".join(" ".join(p) for p in prods)
        print(f"  {nao_terminal}  ::=  {alternativas}")
    print()
    print("=" * 70)
    print("FIRST")
    print("=" * 70)
    for nao_terminal in sorted(NAO_TERMINAIS_ATIVOS):
        print(f"  FIRST({nao_terminal}) = {_format_conj(info['first'][nao_terminal])}")
    print()
    print("=" * 70)
    print("FOLLOW")
    print("=" * 70)
    for nao_terminal in sorted(NAO_TERMINAIS_ATIVOS):
        print(f"  FOLLOW({nao_terminal}) = {_format_conj(info['follow'][nao_terminal])}")
    print()
    print("=" * 70)
    print("TABELA LL(1) — entradas (nao_terminal, terminal) -> producao")
    print("=" * 70)
    for (nao_terminal, terminal), producao in sorted(info["tabela_ll1"].items()):
        print(f"  M[{nao_terminal:14s}, {terminal:10s}] = {nao_terminal} -> {' '.join(producao)}")

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    info = construirGramatica()
    _exibir_res(info)
    print()
    print("Gramática validada como LL(1) (sem conflitos na tabela).")