# Aluno 4 - Lucas Balint Vilar

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