import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.gerarArvore import No, imprimirArvore, salvarArvore

# gerando árvore manualmente para teste
# exemplo: (A (C D *) +)
arvore = No("+", [
    No("A"),
    No("*", [
        No("C"),
        No("D")
    ])
])

print("----ÁRVORE----")
imprimirArvore(arvore)

# salvar arquivo json
caminho = salvarArvore(arvore)
print(f"Árvore salva em: {caminho}")