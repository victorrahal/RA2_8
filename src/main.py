# Alunos
# João Henrique Tomaz Dutra - @Jhtomaz
# Lucas Balint Vilar        - @lucasdxl
# Paulo Henrique Eidi Mino  - @phmino
# Victor Rahal Basseto      - @victorrahal

import os
import sys
import json
from gerarAssembly import gerarAssembly
from lerTokens import lerTokens
from parsear import parsear 
from gerarArvore import gerarArvore, imprimirArvore, simplificarArvore, salvarArvore, salvarArvoreSimplificada
from construirGramatica import construirGramatica

raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <arquivo_teste.txt>")
        return
    
    arquivoEntrada = os.path.join(raiz, "testes", sys.argv[1])
    if not os.path.isfile(arquivoEntrada):
        print(f"Erro: arquivo '{sys.argv[1]}' não encontrado")
        return

    print(f'Processando arquivo: {arquivoEntrada}')
    print()

    try:
        # Tokens
        tokens = lerTokens(arquivoEntrada)

        # Construção da gramática LL(1)
        info = construirGramatica()

        # Parser / derivação
        derivacaotxt, derivacaojson = parsear(tokens, info["tabela_ll1"], info["inicio"])

        print("====DERIVAÇÃO====")
        for regra in derivacaotxt:
            print(regra)

        # Geração da árvore Sintática
        arvore = gerarArvore(derivacaojson)

        print("\n====ÁRVORE SINÁTICA====")
        imprimirArvore(arvore)

        # Simplificação da árvore
        arvoreSimplificada = simplificarArvore(arvore)

        print("\n====ÁRVORE SIMPLIFICADA====")
        print(json.dumps(arvoreSimplificada, indent=2, ensure_ascii=False))

        # Salvando arquivos JSON
        caminhoArvore = salvarArvore(arvore)
        print(f"\nÁrvore salva em: {caminhoArvore}")

        caminhoArvoreSimplificada = salvarArvoreSimplificada(arvoreSimplificada)
        print(f"\nÁrvore simplificada salva em: {caminhoArvoreSimplificada}")

        # Gerando Gráfico da Árvore Sintática
        # caminhoGráfico = gerarGraficoArvoreSimplificada(arvoreSimplificada)
        # print(f"\nGráfico da árvore salvo em: {caminhoGráfico}")

        # Gerando Assembly
        gerarAssembly(arvoreSimplificada)
        print("\nAssembly gerado com sucesso")

        print("\nProcessamento concluído com sucesso!")
    except Exception as erro:
        print(f"Erro durante o processamento: {erro}")

if __name__ == "__main__":
    main()
