tokens = ["(", "id", "id", "+", ")", "$"]

tabela = {
    ("E", "("): ["(", "E", "E", "op", ")"],
    ("E", "id"): ["id"],
    ("op", "+"): ["+"],
}

class No:
    def __init__(self, tipo, valor=None):
        self.tipo = tipo
        self.valor = valor
        self.filhos = []

    def add(self, filho):
        self.filhos.append(filho)

    def __repr__(self):
        return f"{self.tipo}({self.valor})"

def validar_terminal(simbolo, tabela):
    nao_terminais = {chave[0] for chave in tabela}
    return simbolo not in nao_terminais and simbolo != "ε"


def parsear(tokens, tabela):
    pilha = ["$", "E"]
    pilha_semantica = []
    derivacao = []
    i = 0

    while pilha:  # ✅ corrigido
        if i >= len(tokens):
            raise Exception("Fim inesperado dos tokens")

        atual = tokens[i]
        topo = pilha.pop()

        print(f"topo: {topo}")
        print(f"atual: {atual}")

        # condição de parada
        if topo == "$" and atual == "$":
            break

        # ✅ TERMINAL
        if validar_terminal(topo, tabela) or topo == "$":
            if atual == topo:

                # 🌳 AST
                if topo == "id":
                    pilha_semantica.append(No("id", "x"))

                elif topo == "+":
                    if len(pilha_semantica) >= 2:
                        dir = pilha_semantica.pop()
                        esq = pilha_semantica.pop()
                        no = No("+")
                        no.add(esq)
                        no.add(dir)
                        pilha_semantica.append(no)

                i += 1

            else:
                raise Exception(f"Erro sintático: esperado '{topo}', encontrado '{atual}' na posicao {i}")

        # ✅ NÃO TERMINAL
        elif (topo, atual) in tabela:
            prod = tabela[(topo, atual)]
            resultado = ' '
            derivacao.append(f"{topo} -> {resultado.join(prod)}")

            for s in reversed(prod):
                if s != "ε":
                    pilha.append(s)

        else:
            raise Exception(f"Erro sintático: esperado '{topo}', encontrado '{atual}' na posicao {i}")

    # 🌳 RAIZ
    raiz = No("RAIZ")
    temp = []

    while pilha_semantica:
        temp.append(pilha_semantica.pop())

    for no in reversed(temp):
        raiz.add(no)

    return derivacao, raiz


a = parsear(tokens,tabela)
print(a)
