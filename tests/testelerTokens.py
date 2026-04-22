# Paulo Henrique Eidi Mino - Aluno 3
# Testes de integração do lerTokens (Fase 2) com expressões da Fase 1

import os
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from lerTokens import lerTokens

def _criar_temp(conteudo):
    # Cria um arquivo temporário com o conteúdo fornecido e retorna o caminho
    f = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8')
    f.write(conteudo)
    f.close()
    return f.name

def _tipos(tokens):
    # Retorna lista de tipos dos tokens (sem o EOF)
    return [t["tipo"] for t in tokens if t["tipo"] != "$"]

def _valores(tokens):
    # Retorna lista de valores dos tokens (sem o EOF)
    return [t["valor"] for t in tokens if t["valor"] != "$"]

class TestExpressoesFase1(unittest.TestCase):
    # Testa que expressões da Fase 1 são tokenizadas corretamente na Fase 2
    def test_soma_simples(self):
        # Fase 1: (3.0 4.0 +)
        arq = _criar_temp("(3.0 4.0 +)")
        tokens = lerTokens(arq)
        os.unlink(arq)
        self.assertEqual(_tipos(tokens), ["LPAREN", "REAL", "REAL", "OP_SUM", "RPAREN"])

    def test_subtracao(self):
        arq = _criar_temp("(10.0 2.0 -)")
        tokens = lerTokens(arq)
        os.unlink(arq)
        self.assertEqual(_tipos(tokens), ["LPAREN", "REAL", "REAL", "OP_SUB", "RPAREN"])

    def test_multiplicacao(self):
        arq = _criar_temp("(5.0 6.0 *)")
        tokens = lerTokens(arq)
        os.unlink(arq)
        self.assertEqual(_tipos(tokens), ["LPAREN", "REAL", "REAL", "OP_MUL", "RPAREN"])

    def test_potenciacao(self):
        arq = _criar_temp("(2.0 3 ^)")
        tokens = lerTokens(arq)
        os.unlink(arq)
        self.assertEqual(_tipos(tokens), ["LPAREN", "REAL", "INT", "OP_POW", "RPAREN"])

    def test_resto(self):
        arq = _criar_temp("(9 4 %)")
        tokens = lerTokens(arq)
        os.unlink(arq)
        self.assertEqual(_tipos(tokens), ["LPAREN", "INT", "INT", "OP_MOD", "RPAREN"])

    def test_expressao_aninhada(self):
        # Fase 1: ((3.0 4.0 +) 5.0 *)
        arq = _criar_temp("((3.0 4.0 +) 5.0 *)")
        tokens = lerTokens(arq)
        os.unlink(arq)
        self.assertEqual(_tipos(tokens), ["LPAREN", "LPAREN", "REAL", "REAL", "OP_SUM", "RPAREN", "REAL", "OP_MUL", "RPAREN"])

    def test_aninhamento_duplo(self):
        # Fase 1: ((1.5 2.0 *) (3.0 4.0 *) /)
        # Fase 2: / é divisão inteira, | é divisão real
        arq = _criar_temp("((1.5 2.0 *) (3.0 4.0 *) |)")
        tokens = lerTokens(arq)
        os.unlink(arq)
        self.assertEqual(_tipos(tokens), ["LPAREN", "LPAREN", "REAL", "REAL", "OP_MUL", "RPAREN", "LPAREN", "REAL", "REAL", "OP_MUL", "RPAREN", "OP_DIVR", "RPAREN"])

    def test_divisao_inteira_fase2(self):
        # Fase 1: (9 4 //) -> Fase 2: (9 4 /)
        arq = _criar_temp("(9 4 /)")
        tokens = lerTokens(arq)
        os.unlink(arq)
        self.assertEqual(_tipos(tokens), ["LPAREN", "INT", "INT", "OP_DIVI", "RPAREN"])

class TestComandosEspeciais(unittest.TestCase):
    # Testa comandos especiais RES e MEM adaptados para a Fase 2
    def test_res(self):
        arq = _criar_temp("(1 RES)")
        tokens = lerTokens(arq)
        os.unlink(arq)
        self.assertEqual(_tipos(tokens), ["LPAREN", "INT", "KW_RES", "RPAREN"])

    def test_mem_armazenar(self):
        # Fase 1: (5.0 MEM) -> Fase 2: (5.0 MEM VALOR)
        arq = _criar_temp("(5.0 MEM VALOR)")
        tokens = lerTokens(arq)
        os.unlink(arq)
        self.assertEqual(_tipos(tokens), ["LPAREN", "REAL", "KW_MEM", "MEM_ID", "RPAREN"])

    def test_mem_consultar(self):
        # (PRECO) - consulta memória, igual nas duas fases
        arq = _criar_temp("(PRECO)")
        tokens = lerTokens(arq)
        os.unlink(arq)
        self.assertEqual(_tipos(tokens), ["LPAREN", "MEM_ID", "RPAREN"])

    def test_mem_em_expressao(self):
        arq = _criar_temp("((TAXA) 2.0 +)")
        tokens = lerTokens(arq)
        os.unlink(arq)
        self.assertEqual(_tipos(tokens), ["LPAREN", "LPAREN", "MEM_ID", "RPAREN", "REAL", "OP_SUM", "RPAREN"])

class TestNovasKeywordsFase2(unittest.TestCase):
    # Testa keywords que não existiam na Fase 1
    def test_start_end(self):
        arq = _criar_temp("(START)\n(END)")
        tokens = lerTokens(arq)
        os.unlink(arq)
        self.assertEqual(_tipos(tokens), ["LPAREN", "KW_START", "RPAREN", "LPAREN", "KW_END", "RPAREN"])

    def test_if(self):
        arq = _criar_temp("(IF (3 5 <) (1.0 2.0 +) (3.0 4.0 *))")
        tokens = lerTokens(arq)
        os.unlink(arq)
        self.assertIn("KW_IF", _tipos(tokens))

    def test_while(self):
        arq = _criar_temp("(WHILE (X 10 <) (1.0 2.0 +))")
        tokens = lerTokens(arq)
        os.unlink(arq)
        self.assertIn("KW_WHILE", _tipos(tokens))

    def test_for(self):
        arq = _criar_temp("(FOR 0 10 I (1.0 2.0 +))")
        tokens = lerTokens(arq)
        os.unlink(arq)
        self.assertIn("KW_FOR", _tipos(tokens))
        
class TestOperadoresRelacionais(unittest.TestCase):
    #Testa operadores relacionais novos da Fase 2
    def test_menor(self):
        arq = _criar_temp("(3 5 <)")
        tokens = lerTokens(arq)
        os.unlink(arq)
        self.assertEqual(_tipos(tokens), ["LPAREN", "INT", "INT", "OP_LT", "RPAREN"])

    def test_maior(self):
        arq = _criar_temp("(5 3 >)")
        tokens = lerTokens(arq)
        os.unlink(arq)
        self.assertEqual(_tipos(tokens), ["LPAREN", "INT", "INT", "OP_GT", "RPAREN"])

    def test_menor_igual(self):
        arq = _criar_temp("(3 5 <=)")
        tokens = lerTokens(arq)
        os.unlink(arq)
        self.assertEqual(_tipos(tokens), ["LPAREN", "INT", "INT", "OP_LE", "RPAREN"])

    def test_maior_igual(self):
        arq = _criar_temp("(5 3 >=)")
        tokens = lerTokens(arq)
        os.unlink(arq)
        self.assertEqual(_tipos(tokens), ["LPAREN", "INT", "INT", "OP_GE", "RPAREN"])

    def test_igual(self):
        arq = _criar_temp("(5 5 ==)")
        tokens = lerTokens(arq)
        os.unlink(arq)
        self.assertEqual(_tipos(tokens), ["LPAREN", "INT", "INT", "OP_EQ", "RPAREN"])

    def test_diferente(self):
        arq = _criar_temp("(3 5 !=)")
        tokens = lerTokens(arq)
        os.unlink(arq)
        self.assertEqual(_tipos(tokens), ["LPAREN", "INT", "INT", "OP_NE", "RPAREN"])

class TestTiposLiterais(unittest.TestCase):
    # Testa classificação correta de INT vs REAL
    def test_inteiro(self):
        arq = _criar_temp("(42)")
        tokens = lerTokens(arq)
        os.unlink(arq)
        self.assertEqual(tokens[1]["tipo"], "INT")
        self.assertEqual(tokens[1]["valor"], "42")

    def test_real(self):
        arq = _criar_temp("(3.14)")
        tokens = lerTokens(arq)
        os.unlink(arq)
        self.assertEqual(tokens[1]["tipo"], "REAL")
        self.assertEqual(tokens[1]["valor"], "3.14")

    def test_real_comeca_com_zero(self):
        arq = _criar_temp("(0.5)")
        tokens = lerTokens(arq)
        os.unlink(arq)
        self.assertEqual(tokens[1]["tipo"], "REAL")

class TestEOF(unittest.TestCase):
    # Testa que o token $ é sempre adicionado ao final
    def test_eof_presente(self):
        arq = _criar_temp("(1 2 +)")
        tokens = lerTokens(arq)
        os.unlink(arq)
        self.assertEqual(tokens[-1]["tipo"], "$")
        self.assertEqual(tokens[-1]["valor"], "$")

    def test_eof_unico(self):
        arq = _criar_temp("(1 2 +)")
        tokens = lerTokens(arq)
        os.unlink(arq)
        eofs = [t for t in tokens if t["tipo"] == "$"]
        self.assertEqual(len(eofs), 1)

class TestLinhas(unittest.TestCase):
    # Testa que o número da linha é registrado corretamente
    def test_linha_unica(self):
        arq = _criar_temp("(1 2 +)")
        tokens = lerTokens(arq)
        os.unlink(arq)
        for t in tokens:
            if t["tipo"] != "$":
                self.assertEqual(t["linha"], 1)

    def test_multiplas_linhas(self):
        arq = _criar_temp("(1 2 +)\n(3 4 *)")
        tokens = lerTokens(arq)
        os.unlink(arq)
        linhas = [t["linha"] for t in tokens if t["tipo"] != "$"]
        self.assertIn(1, linhas)
        self.assertIn(2, linhas)

    def test_linhas_vazias_ignoradas(self):
        arq = _criar_temp("(1 2 +)\n\n\n(3 4 *)")
        tokens = lerTokens(arq)
        os.unlink(arq)
        linhas = set(t["linha"] for t in tokens if t["tipo"] != "$")
        self.assertEqual(linhas, {1, 4})

class TestErrosLexicos(unittest.TestCase):
    # Testa detecção de erros - compatibilidade com Fase 1
    def test_caractere_invalido(self):
        arq = _criar_temp("(3.0 2.0 &)")
        with self.assertRaises(ValueError):
            lerTokens(arq)
        os.unlink(arq)

    def test_numero_dois_pontos(self):
        arq = _criar_temp("(3.14.5 2.0 +)")
        with self.assertRaises(ValueError):
            lerTokens(arq)
        os.unlink(arq)

    def test_identificador_minusculo(self):
        arq = _criar_temp("(valor)")
        with self.assertRaises(ValueError):
            lerTokens(arq)
        os.unlink(arq)

    def test_arquivo_inexistente(self):
        with self.assertRaises(FileNotFoundError):
            lerTokens("arquivo_fantasma_xyz.txt")

class TestProgramaCompleto(unittest.TestCase):
    # Testa tokenização de um programa completo da Fase 2
    def test_programa_minimo(self):
        arq = _criar_temp("(START)\n(3.0 4.0 +)\n(END)")
        tokens = lerTokens(arq)
        os.unlink(arq)
        tipos = _tipos(tokens)
        self.assertEqual(tipos[0:3], ["LPAREN", "KW_START", "RPAREN"])
        self.assertEqual(tipos[-3:], ["LPAREN", "KW_END", "RPAREN"])

    def test_programa_com_if(self):
        prog = "(START)\n(IF (3 5 <) (1.0 2.0 +) (3.0 4.0 *))\n(END)"
        arq = _criar_temp(prog)
        tokens = lerTokens(arq)
        os.unlink(arq)
        tipos = _tipos(tokens)
        self.assertIn("KW_START", tipos)
        self.assertIn("KW_IF", tipos)
        self.assertIn("OP_LT", tipos)
        self.assertIn("KW_END", tipos)

    def test_programa_com_todas_operacoes(self):
        # Simula o arquivo1.txt da Fase 1 adaptado para Fase 2
        prog = (
            "(START)\n"
            "(3.0 4.0 +)\n"
            "(10.0 2.0 -)\n"
            "(5.0 6.0 *)\n"
            "(8.0 2.0 |)\n"
            "(9 4 /)\n"
            "(9 4 %)\n"
            "(2.0 3 ^)\n"
            "(END)")
        
        arq = _criar_temp(prog)
        tokens = lerTokens(arq)
        os.unlink(arq)
        tipos = _tipos(tokens)
        self.assertIn("OP_SUM", tipos)
        self.assertIn("OP_SUB", tipos)
        self.assertIn("OP_MUL", tipos)
        self.assertIn("OP_DIVR", tipos)
        self.assertIn("OP_DIVI", tipos)
        self.assertIn("OP_MOD", tipos)
        self.assertIn("OP_POW", tipos)

if __name__ == "__main__":
    unittest.main(verbosity=2)