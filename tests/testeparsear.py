# Aluno 2

import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from construirGramatica import construirGramatica
from parsear import parsear


def tok(tipo, valor, linha=1):
    return {"tipo": tipo, "valor": valor, "linha": linha}


def programa(*linhas_tokens):
    inicio = [tok("LPAREN","("), tok("KW_START","START"), tok("RPAREN",")")]
    fim    = [tok("LPAREN","("), tok("KW_END","END"),     tok("RPAREN",")")]
    corpo  = []
    for linha in linhas_tokens:
        corpo.extend(linha)
    return inicio + corpo + fim + [tok("$","$",-1)]


class TestParsearValidos(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tabela = construirGramatica()["tabela_ll1"]

    def _parsear(self, tokens):
        derivacao, _ = parsear(tokens, self.tabela, "programa")
        return derivacao

    def test_expressao_simples_soma(self):
        tokens = programa(
            [tok("LPAREN","("), tok("INT","3"), tok("INT","2"),
             tok("OP_SUM","+"), tok("RPAREN",")")],
        )
        derivacao = self._parsear(tokens)
        self.assertIsInstance(derivacao, list)
        self.assertGreater(len(derivacao), 0)

    def test_expressao_simples_todos_operadores(self):
        for op_tipo, op_val in [("OP_SUB","-"), ("OP_MUL","*"),
                                 ("OP_DIVR","|"), ("OP_DIVI","/"),
                                 ("OP_MOD","%"), ("OP_POW","^")]:
            with self.subTest(op=op_val):
                tokens = programa(
                    [tok("LPAREN","("), tok("INT","10"), tok("INT","2"),
                     tok(op_tipo, op_val), tok("RPAREN",")")],
                )
                self.assertGreater(len(self._parsear(tokens)), 0)

    def test_expressao_aninhada(self):
        tokens = programa(
            [tok("LPAREN","("),
               tok("LPAREN","("), tok("INT","3"), tok("INT","2"),
               tok("OP_SUM","+"), tok("RPAREN",")"),
             tok("INT","5"), tok("OP_MUL","*"), tok("RPAREN",")")],
        )
        self.assertGreater(len(self._parsear(tokens)), 0)

    def test_comando_res(self):
        tokens = programa(
            [tok("LPAREN","("), tok("INT","0"),
             tok("KW_RES","RES"), tok("RPAREN",")")],
        )
        self.assertGreater(len(self._parsear(tokens)), 0)

    def test_comando_mem_armazenar(self):
        tokens = programa(
            [tok("LPAREN","("), tok("REAL","3.14"),
             tok("KW_MEM","MEM"), tok("MEM_ID","VAR"), tok("RPAREN",")")],
        )
        self.assertGreater(len(self._parsear(tokens)), 0)

    def test_comando_mem_consultar(self):
        tokens = programa(
            [tok("LPAREN","("), tok("MEM_ID","VAR"), tok("RPAREN",")")],
        )
        self.assertGreater(len(self._parsear(tokens)), 0)

    def test_estrutura_if(self):
        tokens = programa(
            [tok("LPAREN","("), tok("KW_IF","IF"),
               tok("LPAREN","("), tok("INT","1"), tok("INT","2"),
               tok("OP_LT","<"), tok("RPAREN",")"),
               tok("LPAREN","("), tok("INT","3"), tok("INT","3"),
               tok("OP_SUM","+"), tok("RPAREN",")"),
               tok("LPAREN","("), tok("INT","0"), tok("INT","0"),
               tok("OP_SUM","+"), tok("RPAREN",")"),
             tok("RPAREN",")")],
        )
        self.assertGreater(len(self._parsear(tokens)), 0)

    def test_estrutura_while(self):
        tokens = programa(
            [tok("LPAREN","("), tok("KW_WHILE","WHILE"),
               tok("LPAREN","("), tok("INT","1"), tok("INT","10"),
               tok("OP_LT","<"), tok("RPAREN",")"),
               tok("LPAREN","("), tok("INT","1"), tok("INT","2"),
               tok("OP_SUM","+"), tok("RPAREN",")"),
             tok("RPAREN",")")],
        )
        self.assertGreater(len(self._parsear(tokens)), 0)

    def test_estrutura_for(self):
        tokens = programa(
            [tok("LPAREN","("), tok("KW_FOR","FOR"),
             tok("INT","0"), tok("INT","10"), tok("MEM_ID","I"),
               tok("LPAREN","("), tok("INT","1"), tok("INT","2"),
               tok("OP_SUM","+"), tok("RPAREN",")"),
             tok("RPAREN",")")],
        )
        self.assertGreater(len(self._parsear(tokens)), 0)

    def test_multiplas_linhas(self):
        tokens = programa(
            [tok("LPAREN","("), tok("INT","3"), tok("INT","2"),
             tok("OP_SUM","+"), tok("RPAREN",")")],
            [tok("LPAREN","("), tok("MEM_ID","VAR"), tok("RPAREN",")")],
            [tok("LPAREN","("), tok("INT","0"),
             tok("KW_RES","RES"), tok("RPAREN",")")],
        )
        self.assertGreater(len(self._parsear(tokens)), 0)

    def test_derivacao_contem_programa(self):
        tokens = programa(
            [tok("LPAREN","("), tok("INT","1"), tok("INT","1"),
             tok("OP_SUM","+"), tok("RPAREN",")")],
        )
        derivacao = self._parsear(tokens)
        self.assertTrue(any("programa" in p for p in derivacao))


class TestParsearErros(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tabela = construirGramatica()["tabela_ll1"]

    def _parsear(self, tokens):
        derivacao, _ = parsear(tokens, self.tabela, "programa")
        return derivacao

    def test_token_invalido_apos_start(self):
        tokens = programa(
            [tok("LPAREN","("), tok("OP_SUM","+"), tok("INT","2"),
             tok("INT","3"), tok("RPAREN",")")],
        )
        with self.assertRaises((SyntaxError, Exception)):
            self._parsear(tokens)

    def test_sem_start(self):
        tokens = [
            tok("LPAREN","("), tok("INT","3"), tok("INT","2"),
            tok("OP_SUM","+"), tok("RPAREN",")"),
            tok("$","$",-1),
        ]
        with self.assertRaises((SyntaxError, Exception)):
            self._parsear(tokens)

    def test_sem_end(self):
        tokens = [
            tok("LPAREN","("), tok("KW_START","START"), tok("RPAREN",")"),
            tok("LPAREN","("), tok("INT","3"), tok("INT","2"),
            tok("OP_SUM","+"), tok("RPAREN",")"),
            tok("$","$",-1),
        ]
        with self.assertRaises((SyntaxError, Exception)):
            self._parsear(tokens)

    def test_parentese_nao_fechado(self):
        tokens = [
            tok("LPAREN","("), tok("KW_START","START"), tok("RPAREN",")"),
            tok("LPAREN","("), tok("INT","3"), tok("INT","2"),
            tok("OP_SUM","+"),
            tok("$","$",-1),
        ]
        with self.assertRaises((SyntaxError, Exception)):
            self._parsear(tokens)

    def test_mensagem_erro_contem_linha(self):
        tokens = programa(
            [tok("LPAREN","(",5), tok("OP_SUM","+",5),
             tok("RPAREN",")",5)],
        )
        try:
            self._parsear(tokens)
            self.fail("Deveria ter levantado erro sintático")
        except (SyntaxError, Exception) as e:
            self.assertIn("5", str(e))


if __name__ == "__main__":
    unittest.main(verbosity=2)
