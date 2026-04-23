def tokens():
    tokens = [
        # (START)
        {"tipo": "LPAREN", "valor": "(", "linha": 1},
        {"tipo": "KW_START", "valor": "START", "linha": 1},
        {"tipo": "RPAREN", "valor": ")", "linha": 1},

        # ( 3 RES )
        {"tipo": "LPAREN", "valor": "(", "linha": 1},

            {"tipo": "INT", "valor": "3", "linha": 1},
            {"tipo": "KW_RES", "valor": "A", "linha": 1},

        {"tipo": "RPAREN", "valor": ")", "linha": 1},

        # (END)
        {"tipo": "LPAREN", "valor": "(", "linha": 1},
        {"tipo": "KW_END", "valor": "END", "linha": 1},
        {"tipo": "RPAREN", "valor": ")", "linha": 1},

        {"tipo": "$", "valor": "$", "linha": 1},
    ]
    return tokens