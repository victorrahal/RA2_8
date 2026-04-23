# Aluno 4 - Lucas Balint Vilar
import json
import os

class No:
    def __init__(self, tipo_no, simbolo, producao=None, token=None, filhos=None):
        self.tipo_no = tipo_no
        self.simbolo = simbolo
        self.producao = producao or []
        self.token = token
        self.filhos = filhos or []

    def __repr__(self):
        return f"No(tipo_no={self.tipo_no}, simbolo={self.simbolo})"
    
def gerarArvore(derivacao): #cria a árvore a partir da derivação recebida
    no = No( # cria os nós a partir do dicionario
        tipo_no = derivacao.get("tipo_no"),
        simbolo = derivacao.get("simbolo"),
        producao = derivacao.get("producao", []),
        token = derivacao.get("token"),
        filhos = []
    )

    # percorrer recursivamente os filhos da derivação e covnerter em nós de árvore
    for filho in derivacao.get("filhos", []):
        no.filhos.append(gerarArvore(filho))

    return no

# função para converter árvore para dicionário
def converterArvore(no):
    return {
        "tipo_no": no.tipo_no,
        "simbolo": no.simbolo,
        "producao": no.producao,
        "token": no.token,
        "filhos": [converterArvore(filho) for filho in no.filhos]
    }

def imprimirArvore(no, nivel=0):
    espaco = "  " * nivel

    if no.tipo_no == "terminal" and no.token:
        valor = no.token.get("valor")
        linha = no.token.get("linha")
        print(f"{espaco} {no.simbolo}: '{valor}' (linha {linha})")
    else:
        if no.producao:
            producao = " ".join(no.producao)
            print(f"{espaco}{no.simbolo} -> {producao}")
        else:
            print(f"{espaco}{no.simbolo}")

    for filho in no.filhos:
        imprimirArvore(filho, nivel + 1)

# salva a árvore convertida em um arquivo JSON
def salvarArvore(arvore, nomeArquivo="arvore.json"):
    raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    pastaSaida = os.path.join(raiz, "saida")
    caminho = os.path.join(pastaSaida, nomeArquivo)

    with open(caminho, "w") as f:
        json.dump(converterArvore(arvore), f, indent=2)

    return caminho