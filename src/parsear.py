from construirGramatica import construirGramatica

EPSILON = "ε"
EOF = "$"

def validar_terminal(simbolo, tabela):
    nao_terminais = {chave[0] for chave in tabela}
    return simbolo not in nao_terminais and simbolo != EPSILON


def parsear(tokens, tabela, simbolo_inicial):
    # 🔹 pilha sintática
    pilha = [EOF, simbolo_inicial]

    # 🔹 derivação
    derivacao = []

    # 🔹 ponteiro de entrada
    i = 0

    while pilha:
        if i >= len(tokens):
            raise Exception("Erro sintático: fim inesperado da entrada")

        topo = pilha.pop()
        atual = tokens[i]

        tipo_atual = atual["tipo"]
        linha_atual = atual["linha"]

        print(f"Topo: {topo} | Token atual: {tipo_atual}")

        # ✅ condição de parada
        if topo == EOF and tipo_atual == EOF:
            break

        # ✅ TERMINAL
        if validar_terminal(topo, tabela) or topo == EOF:
            if topo == tipo_atual:
                i += 1  # consome token
            else:
                raise Exception(
                    f"Erro sintático na linha {linha_atual}: "
                    f"esperado '{topo}', encontrado '{tipo_atual}'"
                )

        # ✅ NÃO TERMINAL
        else:
            chave = (topo, tipo_atual)

            if chave in tabela:
                prod = tabela[chave]

                # salva derivação
                derivacao.append(f"{topo} -> {' '.join(prod)}")

                # empilha produção (invertida)
                for s in reversed(prod):
                    if s != EPSILON:
                        pilha.append(s)
            else:
                raise Exception(
                    f"Erro sintático na linha {linha_atual}: "
                    f"não há regra para ({topo}, {tipo_atual})"
                )

    return derivacao


# 1. construir gramática (Aluno 1)
info = construirGramatica()

# 2. exemplo de tokens (Aluno 3)
tokens = [
    {"tipo": "LPAREN", "valor": "(", "linha": 1},
    {"tipo": "KW_START", "valor": "START", "linha": 1},
    {"tipo": "RPAREN", "valor": ")", "linha": 1},

    {"tipo": "LPAREN", "valor": "(", "linha": 1},
    {"tipo": "KW_END", "valor": "END", "linha": 1},
    {"tipo": "RPAREN", "valor": ")", "linha": 1},

    {"tipo": "$", "valor": "$", "linha": 1},
]

# 3. rodar parser
derivacao = parsear(tokens, info["tabela_ll1"], info["inicio"])

# 4. saída
for d in derivacao:
    print(d)