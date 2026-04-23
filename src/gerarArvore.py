# Aluno 4 - Lucas Balint Vilar
import json
import os

raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
caminhoArvore = os.path.join(raiz, "saida", "arvore.json")
caminhoArvore_simplificada = os.path.join(raiz, "saida", "arvore_simplficada.json")
caminhoDerivacao = os.path.join(raiz, "saida", "derivacao.json")

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

    # percorrer recursivamente os filhos da derivação e converte em nós de árvore
    for filho in derivacao.get("filhos", []):
        no.filhos.append(gerarArvore(filho))

    return no

def simplificarArvore(no):
    if no.tipo_no == "terminal" and no.token:
        return { # caso terminal
            "tipo": "terminal",
            "simbolo": no.simbolo,
            "valor": no.token.get("valor"),
            "linha": no.token.get("linha")
        }
    match no.simbolo:
        case "programa":
            for filho in no.filhos:
                if filho.simbolo == "linhas":
                    return simplificarArvore(filho)

        case "linhas":
            for filho in no.filhos:
                if filho.simbolo == "linhas_rest":
                    return simplificarArvore(filho)
        
        case "linhas_rest":
            if len(no.filhos) == 2:
                primeiroTermo = no.filhos[0]
                if primeiroTermo.tipo_no == "terminal" and primeiroTermo.simbolo == "KW_END":
                    return {
                        "tipo": "fim_programa",
                        "linha": primeiroTermo.token.get("linha")
                    }
                
            # caso linhas normais
            if len(no.filhos) == 3:
                termoAtual = simplificarArvore(no.filhos[0])
                proximoTermo = simplificarArvore(no.filhos[2])
                return {
                    "tipo": "sequencia",
                    "atual": termoAtual,
                    "proximo": proximoTermo 
                }
            
        case "linha":
            for filho in no.filhos:
                if filho.simbolo == "corpo":
                    return simplificarArvore(filho)
                
        case "corpo": 
            if len(no.filhos) == 2:
                primeiroTermo = no.filhos[0]
                segundoTermo = no.filhos[1]

                #para RES
                if (primeiroTermo.tipo_no == "terminal" and primeiroTermo.simbolo == "INT" and segundoTermo.simbolo == "resto_corpo" and len(segundoTermo.filhos) == 1 and segundoTermo.filhos[0].tipo_no == "terminal" and segundoTermo.filhos[0].simbolo == "KW_RES"):
                    return {
                        "tipo": "res",
                        "indice": int(primeiroTermo.token.get("valor")),
                        "linha": primeiroTermo.token.get("linha")
                    }
                
                #caso expressão aritmética
                esquerdo = simplificarArvore(no.filhos[0])
                resto = no.filhos[1]
                if resto.simbolo == "resto_corpo" and len(resto.filhos) == 2:
                    direito = simplificarArvore(resto.filhos[0])
                    operador = simplificarArvore(resto.filhos[1])
                    return {
                        "tipo": "expressao_aritmetica",
                        "operador": operador["valor"],
                        "operandos": [esquerdo, direito],
                        "linha": esquerdo.get("linha")
                    }
                
        case "operando":
            if len(no.filhos) == 1:
                return simplificarArvore(no.filhos[0])
            
        case "operador_arit":
            if len(no.filhos) == 1:
                return simplificarArvore(no.filhos[0])
            
    return {
        "tipo": no.simbolo,
        "filhos": [simplificarArvore(filho) for filho in no.filhos]
    }

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
def salvarArvore(arvore):
    with open(caminhoArvore, "w") as f:
        json.dump(converterArvore(arvore), f, indent=2)

    return caminhoArvore

def salvarArvoreSimplificada(arvoreSimplificada):
    with open(caminhoArvore_simplificada, "w") as f:
        json.dump((arvoreSimplificada), f, indent=2)

    return caminhoArvore_simplificada

def carregarDerivacao():
    with open(caminhoDerivacao, 'r') as f:
        return json.load(f)