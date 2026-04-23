# Aluno 4 - Lucas Balint Vilar
import json
import os

class No:
    def __init__(self, valor, filhos=None):
        self.valor = valor
        self.filhos = filhos or []

    def __repr__(self):
        return f"No({self.valor})"

def imprimirArvore(no, nivel=0):
    print("  " * nivel + str(no.valor))
    for filho in no.filhos:
        imprimirArvore(filho, nivel + 1)

# função para converter árvore para dicionário
def convertArvore(no):
    return {
        "valor": no.valor,
        "filhos": [convertArvore(filho) for filho in no.filhos]
    }

# salva a árvore convertida em um arquivo JSON
def salvarArvore(arvore, nomeArquivo="arvore.json"):
    raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    pastaSaida = os.path.join(raiz, "saida")
    caminho = os.path.join(pastaSaida, nomeArquivo)

    with open(caminho, "w") as f:
        json.dump(convertArvore(arvore), f, indent=2)

    return caminho