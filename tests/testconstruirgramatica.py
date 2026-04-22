# Victor Rahal Basseto - Aluno 1

import os
import sys
import unittest

# Permite rodar com "python3 tests/test_construirGramatica.py"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from construirGramatica import (  # noqa: E402
    construirGramatica,
    calcularFirst,
    calcularFollow,
    construirTabelaLL1,
    firstDeCadeia,
    GRAMATICA, INICIO, EPSILON, EOF,
)


class TestGramaticaLL1(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.info = construirGramatica()
        cls.first = cls.info["first"]
        cls.follow = cls.info["follow"]
        cls.tabela = cls.info["tabela_ll1"]

    def test_first_programa_tem_apenas_LPAREN(self):
        self.assertEqual(self.first["programa"], {"LPAREN"})

    def test_first_operador_arit_tem_todos_os_operadores(self):
        esperado = {"OP_SUM", "OP_SUB", "OP_MUL",
                    "OP_DIVR", "OP_DIVI", "OP_MOD", "OP_POW"}
        self.assertEqual(self.first["operador_arit"], esperado)

    def test_first_op_rel_tem_todos_os_relacionais(self):
        esperado = {"OP_LT", "OP_GT", "OP_LE", "OP_GE", "OP_EQ", "OP_NE"}
        self.assertEqual(self.first["op_rel"], esperado)

    def test_first_cauda_mem_inclui_epsilon(self):
        # cauda_mem é anulável (produz ε)
        self.assertIn(EPSILON, self.first["cauda_mem"])

    def test_first_corpo_nao_inclui_epsilon(self):
        self.assertNotIn(EPSILON, self.first["corpo"])

    def test_first_linhas_rest_inclui_KW_END(self):
        # é fundamental que KW_END esteja em FIRST(linhas_rest)
        # — é ele quem permite terminar o programa.
        self.assertIn("KW_END", self.first["linhas_rest"])

    def test_follow_programa_so_EOF(self):
        self.assertEqual(self.follow["programa"], {EOF})

    def test_follow_cauda_mem_so_RPAREN(self):
        self.assertEqual(self.follow["cauda_mem"], {"RPAREN"})

    def test_follow_resto_corpo_so_RPAREN(self):
        self.assertEqual(self.follow["resto_corpo"], {"RPAREN"})

    def test_follow_operador_arit_so_RPAREN(self):
        self.assertEqual(self.follow["operador_arit"], {"RPAREN"})

    def test_follow_operando_inclui_inicios_de_outros_operandos(self):
        # operando pode ser seguido por outro operando (segundo A/B
        # da tripla A B op) ou pelo operador aritmético.
        f = self.follow["operando"]
        for t in {"INT", "REAL", "MEM_ID", "LPAREN",
                  "OP_SUM", "OP_SUB", "OP_MUL",
                  "OP_DIVR", "OP_DIVI", "OP_MOD", "OP_POW"}:
            self.assertIn(t, f, f"FOLLOW(operando) deveria conter {t}")

    def test_tabela_nao_esta_vazia(self):
        self.assertGreater(len(self.tabela), 0)

    def test_tabela_sem_conflitos(self):
        # A própria construirGramatica() lança ValueError em caso de
        # conflito, mas validamos de novo chamando diretamente.
        _, conflitos = construirTabelaLL1(GRAMATICA, self.first, self.follow)
        self.assertEqual(conflitos, [], f"Conflitos: {conflitos}")

    def test_entrada_programa_LPAREN(self):
        self.assertIn(("programa", "LPAREN"), self.tabela)

    def test_entrada_linhas_rest_KW_END(self):
        prod = self.tabela[("linhas_rest", "KW_END")]
        self.assertEqual(prod, ["KW_END", "RPAREN"])

    def test_entrada_corpo_para_cada_inicio_de_estrutura(self):
        for kw in {"KW_IF", "KW_WHILE", "KW_FOR",
                   "INT", "REAL", "MEM_ID", "LPAREN"}:
            self.assertIn(("corpo", kw), self.tabela,
                          f"Falta M[corpo, {kw}]")

    def test_cauda_mem_RPAREN_vai_para_epsilon(self):
        self.assertEqual(self.tabela[("cauda_mem", "RPAREN")], [EPSILON])

    def test_resto_corpo_decide_os_tres_casos(self):
        self.assertEqual(self.tabela[("resto_corpo", "KW_RES")], ["KW_RES"])
        self.assertEqual(self.tabela[("resto_corpo", "KW_MEM")],
                         ["KW_MEM", "MEM_ID"])
        self.assertEqual(self.tabela[("resto_corpo", "INT")],
                         ["operando", "operador_arit"])
        self.assertEqual(self.tabela[("resto_corpo", "LPAREN")],
                         ["operando", "operador_arit"])

    def test_first_cadeia_vazia_retorna_epsilon(self):
        self.assertEqual(firstDeCadeia([], self.first), {EPSILON})

    def test_first_cadeia_operando_operador_arit(self):
        # FIRST(operando operador_arit) = FIRST(operando) (operando
        # não gera ε), logo deve ser exatamente FIRST(operando).
        self.assertEqual(
            firstDeCadeia(["operando", "operador_arit"], self.first),
            self.first["operando"],
        )


class TestRegressaoSemConflitos(unittest.TestCase):
    """Se alguém alterar a gramática introduzindo um conflito, este
    teste quebra imediatamente."""

    def test_construirGramatica_nao_levanta(self):
        try:
            construirGramatica()
        except ValueError as e:
            self.fail(f"Gramática deixou de ser LL(1): {e}")


if __name__ == "__main__":
    unittest.main(verbosity=2)