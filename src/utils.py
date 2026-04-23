# Arquivo utilitário para armazenar as funções da Fase 1, facilitando a leitura dos arquivos

def lerArquivo(nomeArquivo):
    linhas = []

    try:
        with open(nomeArquivo, 'r') as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if linha != "":
                    linhas.append(linha)

    except FileNotFoundError:
        print(f"Erro: arquivo '{nomeArquivo}' não encontrado.")
        return []
    
    except Exception as erro:
        print(f"Erro ao ler o arquivo '{nomeArquivo}': {erro}")
        return[]

    return linhas

def parseExpressao(linha):
    tokens = []
    i = 0
    pilha_parenteses = []
    while i < len(linha):
        entrada = linha[i]

        if entrada == ' ':
            i = i + 1
            continue

        elif entrada.isdigit():
            token, i = estadoNumero(linha, i)
            tokens.append(token)

        elif entrada in ['+','-','*','/','%','^']:
            token, i = estadoOperador(linha, i)
            tokens.append(token)

        elif entrada in "()":
            token, i = estadoParenteses(linha, i, pilha_parenteses)
            tokens.append(token)

        elif entrada.isalpha():
            token, i = estadoComando(linha, i)
            tokens.append(token)

        else:
            raise Exception(f"Entrada inválida")

    return tokens

def estadoNumero(linha, i):
    numero = []
    ponto = 0

    while i < len(linha):
        num = linha[i]
        if num.isdigit():
            numero.append(num)
        elif num == ".":
            if ponto >= 1:
                raise Exception("Número inválido, mais de um ponto")
            ponto = 1
            numero += num
        else:
            break
        i = i + 1
    numero = "".join(numero)
    return numero, i
  
def estadoComando(linha, i):
    letras = []

    while i < len(linha) and linha[i].isalpha():
        letras.append(linha[i])
        i = i + 1
    comando = "".join(letras)
    if not comando.isupper() or not comando.isalpha():
        raise Exception(f"Comando inválido: {comando}")

    return comando, i

def estadoOperador(linha, i):
    if linha[i] == '/' and i+1 < len(linha) and linha[i+1] == '/':
        return "//", i+2
    else:
        return linha[i], i+1

def estadoParenteses(linha, i, pilha):
  if linha[i] == "(":
    pilha.append("(")
  elif linha[i] == ")":
    if not pilha:
      raise Exception("Parenteses não batem")
    pilha.pop()
  return linha[i], i+1

def parseMultiplas(expressoes):
    resultado = []

    for expr in expressoes:
        tokens = parseExpressao(expr)
        resultado.append(tokens)

    return resultado