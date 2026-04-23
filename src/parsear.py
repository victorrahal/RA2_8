from construirGramatica import construirGramatica, eh_terminal

EPSILON = "ε"
EOF = "$"

class No:
    def __init__(self, simbolo, tipo_no):
        self.simbolo = simbolo
        self.tipo_no = tipo_no  # "terminal" ou "nao_terminal"
        self.producao = None
        self.token = None
        self.filhos = []

    def to_dict(self):
        resultado = {
            "tipo_no": self.tipo_no,
            "simbolo": self.simbolo
        }

        if self.producao:
            resultado["producao"] = self.producao

        if self.token:
            resultado["token"] = self.token

        if self.filhos:
            resultado["filhos"] = [f.to_dict() for f in self.filhos]

        return resultado


def validar_terminal(simbolo, tabela):
    nao_terminais = {chave[0] for chave in tabela}
    return simbolo not in nao_terminais and simbolo != EPSILON


def parsear(tokens, tabela, simbolo_inicial):
    pilha = [EOF, simbolo_inicial]
    pilha_nos = []

    derivacao = []
    i = 0

    raiz = No(simbolo_inicial, "nao_terminal")
    pilha_nos.append(No(EOF, "terminal"))  
    pilha_nos.append(raiz)

    while pilha:
        if i >= len(tokens):
            raise Exception("Erro sintático: fim inesperado da entrada")

        topo = pilha.pop()
        no_atual = pilha_nos.pop()

        atual = tokens[i]
        tipo_atual = atual["tipo"]
        linha_atual = atual["linha"]

        print(f"Topo: {topo} | Token atual: {tipo_atual}")

        # parada
        if topo == EOF and tipo_atual == EOF:
            break

        if validar_terminal(topo, tabela) or topo == EOF:
            if topo == tipo_atual:
                no_atual.token = atual  
                i += 1
            else:
                raise Exception(
                    f"Erro sintático na linha {linha_atual}: "
                    f"esperado '{topo}', encontrado '{tipo_atual}'"
                )


        else:
            chave = (topo, tipo_atual)

            if chave in tabela:
                prod = tabela[chave]


                derivacao.append(f"{topo} -> {' '.join(prod)}")

                no_atual.producao = prod

                filhos = []

                for s in prod:
                    if s != EPSILON:
                        tipo_no = "terminal" if validar_terminal(s, tabela) else "nao_terminal"
                        novo = No(s, tipo_no)
                        filhos.append(novo)

             
                no_atual.filhos = filhos

               
                for f in reversed(filhos):
                    pilha.append(f.simbolo)
                    pilha_nos.append(f)

            else:
                raise Exception(
                    f"Erro sintático na linha {linha_atual}: "
                    f"não há regra para ({topo}, {tipo_atual})"
                )

    return derivacao, raiz.to_dict()


# ================= TESTE =================

info = construirGramatica()

tokens = [
    # (START)
    {"tipo": "LPAREN", "valor": "(", "linha": 1},
    {"tipo": "KW_START", "valor": "START", "linha": 1},
    {"tipo": "RPAREN", "valor": ")", "linha": 1},

    # ( 3 RES )
    {"tipo": "LPAREN", "valor": "(", "linha": 1},

        {"tipo": "KW_MEM", "valor": "3", "linha": 1},
        {"tipo": "MEM_ID", "valor": "A", "linha": 1},

    {"tipo": "RPAREN", "valor": ")", "linha": 1},

    # (END)
    {"tipo": "LPAREN", "valor": "(", "linha": 1},
    {"tipo": "KW_END", "valor": "END", "linha": 1},
    {"tipo": "RPAREN", "valor": ")", "linha": 1},

    {"tipo": "$", "valor": "$", "linha": 1},
]

derivacao, arvore = parsear(tokens, info["tabela_ll1"], info["inicio"])

print("\nDERIVAÇÃO:")
for d in derivacao:
    print(d)

import json
print("\nÁRVORE:")
print(json.dumps(arvore, indent=2, ensure_ascii=False))