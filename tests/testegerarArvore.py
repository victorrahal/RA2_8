# Aluno 4 - Lucas Balint Vilar
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gerarArvore import gerarArvore, imprimirArvore, salvarArvore, simplificarArvore, salvarArvoreSimplificada, carregarDerivacao
from src.gerarAssembly import gerarAssembly
from src.gerarArvore import gerarGraficoArvoreSimplificada

derivacao = carregarDerivacao()
arvore = gerarArvore(derivacao)

print('----ARVORE SINTÁTICA----')
imprimirArvore(arvore)

arvoreSimplificada = simplificarArvore(arvore) #salva arvore simplificada

caminho1 = salvarArvore(arvore)
print(f"Árvore salva em: {caminho1}")

caminho2 = salvarArvoreSimplificada(arvoreSimplificada)
print(f"Árvore Simplificada salva em: {caminho2}")

codigoAssembly = gerarAssembly(arvoreSimplificada) #salva assembly

# caminhoImg = gerarGraficoArvoreSimplificada(arvoreSimplificada)
# print("Imagem da árvore salva em:", caminhoImg)