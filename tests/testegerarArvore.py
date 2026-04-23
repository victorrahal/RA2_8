import sys, os, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gerarArvore import gerarArvore, imprimirArvore, salvarArvore, simplificarArvore

derivacao = {
    "tipo_no": "nao_terminal",
    "simbolo": "linha",
    "producao": ["LPAREN", "corpo", "RPAREN"],
    "filhos": [
        {
            "tipo_no": "terminal",
            "simbolo": "LPAREN",
            "token": {"tipo": "LPAREN", "valor": "(", "linha": 1}
        },
        {
            "tipo_no": "nao_terminal",
            "simbolo": "corpo",
            "producao": ["INT", "resto_corpo"],
            "filhos": [
                {
                    "tipo_no": "terminal",
                    "simbolo": "INT",
                    "token": {"tipo": "INT", "valor": "3", "linha": 1}
                },
                {
                    "tipo_no": "nao_terminal",
                    "simbolo": "resto_corpo",
                    "producao": ["operando", "operador_arit"],
                    "filhos": [
                        {
                            "tipo_no": "nao_terminal",
                            "simbolo": "operando",
                            "producao": ["INT"],
                            "filhos": [
                                {
                                    "tipo_no": "terminal",
                                    "simbolo": "INT",
                                    "token": {"tipo": "INT", "valor": "4", "linha": 1}
                                }
                            ]
                        },
                        {
                            "tipo_no": "nao_terminal",
                            "simbolo": "operador_arit",
                            "producao": ["OP_SUM"],
                            "filhos": [
                                {
                                    "tipo_no": "terminal",
                                    "simbolo": "OP_SUM",
                                    "token": {"tipo": "OP_SUM", "valor": "+", "linha": 1}
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "tipo_no": "terminal",
            "simbolo": "RPAREN",
            "token": {"tipo": "RPAREN", "valor": ")", "linha": 1}
        }
    ]
}

arvore = gerarArvore(derivacao)

print('----ARVORE DE DERIVAÇÃO----')
imprimirArvore(arvore)

arvoreSimplificada = simplificarArvore(arvore)
print('----ARVORE SIMPLIFICADA----')
print(json.dumps(arvoreSimplificada, indent=2, ensure_ascii=False))

caminho = salvarArvore(arvore)
print(f"Árvore salva em: {caminho}")