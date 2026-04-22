# Alunos
# João Henrique Tomaz Dutra - @Jhtomaz
# Lucas Balint Vilar        - @lucasdxl
# Paulo Henrique Eidi Mino  - @phmino
# Victor Rahal Basseto      - @victorrahal

import os
 
from utils import validarArgumentos, salvarTokens
from lerArquivo import lerArquivo
from parseExpressao import parseExpressao
from executarExpressao import executarExpressao
from gerarAssembly import gerarAssembly
from exibirResultados import exibirResultados
 
def main():
    nomeArquivo = validarArgumentos()
    print(f"Processando arquivo: {nomeArquivo}")
    print()
 
    try:
        linhas = lerArquivo(nomeArquivo)
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return
 
    if not linhas:
        print("Erro: nenhuma linha válida encontrada no arquivo.")
        return
 
    print(f"Linhas lidas: {len(linhas)}")
    print()
 
    tokens_todas_linhas = []
    print("Análise léxica:")
    for i, linha in enumerate(linhas):
        try:
            tokens = parseExpressao(linha)
            tokens_todas_linhas.append(tokens)
            print(f"  Linha {i + 1}: {tokens}")
        except Exception as e:
            print(f"  Linha {i + 1}: ERRO LÉXICO - {e}")
            tokens_todas_linhas.append([])
    print()
 
    memorias = {}
    historico = []
    resultados = []
 
    for i, tokens in enumerate(tokens_todas_linhas):
        if not tokens:
            resultados.append(0.0)
            historico.append(0.0)
            continue
        try:
            resultado, memorias = executarExpressao(tokens, memorias, historico)
            resultados.append(resultado)
            historico.append(resultado)
        except Exception as e:
            print(f"Erro ao executar linha {i + 1}: {e}")
            resultados.append(0.0)
            historico.append(0.0)
 
    exibirResultados(resultados)
    print()
 
    dirOutputs = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'outputs')
    os.makedirs(dirOutputs, exist_ok=True)

    try:
        caminhoAssembly = os.path.join(dirOutputs, 'Assembly.s')
        codigoAssembly = gerarAssembly(tokens_todas_linhas, arquivoSaida=caminhoAssembly)
        print(f"Assembly salvo em: {caminhoAssembly}")
    except Exception as e:
        print(f"Erro ao gerar Assembly: {e}")

    try:
        caminhoTokens = os.path.join(dirOutputs, 'tokens.json')
        salvarTokens(tokens_todas_linhas, caminhoTokens)
    except Exception as e:
        print(f"Erro ao salvar tokens: {e}")
 
    print()
    print("Processamento concluído com sucesso!")
 
if __name__ == "__main__":
    main()