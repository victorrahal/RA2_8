import sys, os, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gerarArvore import gerarArvore, imprimirArvore, salvarArvore, simplificarArvore

derivacao = {
  "tipo_no": "nao_terminal",
  "simbolo": "programa",
  "producao": [
    "LPAREN",
    "KW_START",
    "RPAREN",
    "linhas"
  ],
  "filhos": [
    {
      "tipo_no": "terminal",
      "simbolo": "LPAREN",
      "token": {
        "tipo": "LPAREN",
        "valor": "(",
        "linha": 1
      }
    },
    {
      "tipo_no": "terminal",
      "simbolo": "KW_START",
      "token": {
        "tipo": "KW_START",
        "valor": "START",
        "linha": 1
      }
    },
    {
      "tipo_no": "terminal",
      "simbolo": "RPAREN",
      "token": {
        "tipo": "RPAREN",
        "valor": ")",
        "linha": 1
      }
    },
    {
      "tipo_no": "nao_terminal",
      "simbolo": "linhas",
      "producao": [
        "LPAREN",
        "linhas_rest"
      ],
      "filhos": [
        {
          "tipo_no": "terminal",
          "simbolo": "LPAREN",
          "token": {
            "tipo": "LPAREN",
            "valor": "(",
            "linha": 1
          }
        },
        {
          "tipo_no": "nao_terminal",
          "simbolo": "linhas_rest",
          "producao": [
            "corpo",
            "RPAREN",
            "linhas"
          ],
          "filhos": [
            {
              "tipo_no": "nao_terminal",
              "simbolo": "corpo",
              "producao": [
                "INT",
                "resto_corpo"
              ],
              "filhos": [
                {
                  "tipo_no": "terminal",
                  "simbolo": "INT",
                  "token": {
                    "tipo": "INT",
                    "valor": "3",
                    "linha": 1
                  }
                },
                {
                  "tipo_no": "nao_terminal",
                  "simbolo": "resto_corpo",
                  "producao": [
                    "KW_RES"
                  ],
                  "filhos": [
                    {
                      "tipo_no": "terminal",
                      "simbolo": "KW_RES",
                      "token": {
                        "tipo": "KW_RES",
                        "valor": "RES",
                        "linha": 1
                      }
                    }
                  ]
                }
              ]
            },
            {
              "tipo_no": "terminal",
              "simbolo": "RPAREN",
              "token": {
                "tipo": "RPAREN",
                "valor": ")",
                "linha": 1
              }
            },
            {
              "tipo_no": "nao_terminal",
              "simbolo": "linhas",
              "producao": [
                "LPAREN",
                "linhas_rest"
              ],
              "filhos": [
                {
                  "tipo_no": "terminal",
                  "simbolo": "LPAREN",
                  "token": {
                    "tipo": "LPAREN",
                    "valor": "(",
                    "linha": 1
                  }
                },
                {
                  "tipo_no": "nao_terminal",
                  "simbolo": "linhas_rest",
                  "producao": [
                    "KW_END",
                    "RPAREN"
                  ],
                  "filhos": [
                    {
                      "tipo_no": "terminal",
                      "simbolo": "KW_END",
                      "token": {
                        "tipo": "KW_END",
                        "valor": "END",
                        "linha": 1
                      }
                    },
                    {
                      "tipo_no": "terminal",
                      "simbolo": "RPAREN",
                      "token": {
                        "tipo": "RPAREN",
                        "valor": ")",
                        "linha": 1
                      }
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
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