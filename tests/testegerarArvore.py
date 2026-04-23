# Aluno 4 - Lucas Balint Vilar
import sys, os, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gerarArvore import gerarArvore, imprimirArvore, salvarArvore, simplificarArvore, salvarArvoreSimplificada, carregarDerivacao
from src.gerarAssembly import gerarAssembly

derivacao = carregarDerivacao()
arvore = gerarArvore(derivacao)

print('----ARVORE DE DERIVAÇÃO----')
imprimirArvore(arvore)

arvoreSimplificada = simplificarArvore(arvore)
print('----ARVORE SIMPLIFICADA----')
print(json.dumps(arvoreSimplificada, indent=2, ensure_ascii=False))

caminho1 = salvarArvore(arvore)
print(f"Árvore salva em: {caminho1}")

caminho2 = salvarArvoreSimplificada(arvoreSimplificada)
print(f"Árvore Simplificada salva em: {caminho2}")

codigoAssembly = gerarAssembly(arvoreSimplificada)

print("\n---- ASSEMBLY ----")
for linha in codigoAssembly:
    print(linha)