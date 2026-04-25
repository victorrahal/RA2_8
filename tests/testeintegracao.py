# Aluno 4 - Lucas Balint Vilar
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from construirGramatica import construirGramatica
from lerTokens import lerTokens
from parsear import parsear
from gerarArvore import gerarArvore, simplificarArvore
from gerarAssembly import gerarAssembly


class TestIntegracao(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.info = construirGramatica()

    def _pipeline(self, caminho):
        tokens = lerTokens(caminho)
        derivacao, arvore_dict = parsear(tokens, self.info["tabela_ll1"], self.info["inicio"])
        arvore = gerarArvore(arvore_dict)
        arvore_simplificada = simplificarArvore(arvore)
        assembly = gerarAssembly(arvore_simplificada)
        return derivacao, arvore_simplificada, assembly

    def test_pipeline_teste1(self):
        derivacao, arvore, assembly = self._pipeline(
            os.path.join(ROOT, "testes", "teste1.txt")
        )
        self.assertGreater(len(derivacao), 0)
        self.assertIsNotNone(arvore)
        self.assertIsInstance(assembly, list)
        self.assertGreater(len(assembly), 0)

    def test_pipeline_teste2(self):
        derivacao, arvore, assembly = self._pipeline(
            os.path.join(ROOT, "testes", "teste2.txt")
        )
        self.assertGreater(len(derivacao), 0)
        self.assertIsNotNone(arvore)
        self.assertIsInstance(assembly, list)

    def test_pipeline_teste3(self):
        derivacao, arvore, assembly = self._pipeline(
            os.path.join(ROOT, "testes", "teste3.txt")
        )
        self.assertGreater(len(derivacao), 0)
        self.assertIsNotNone(arvore)
        self.assertIsInstance(assembly, list)

    def test_assembly_contem_start(self):
        _, _, assembly = self._pipeline(
            os.path.join(ROOT, "testes", "teste1.txt")
        )
        self.assertIn("_start:", assembly)

    def test_erro_lexico(self):
        with self.assertRaises((ValueError, Exception)):
            lerTokens(os.path.join(ROOT, "testes", "teste_erroLexico.txt"))

    def test_erro_sintatico(self):
        tokens = lerTokens(os.path.join(ROOT, "testes", "teste_erroSintatico.txt"))
        with self.assertRaises((Exception,)):
            parsear(tokens, self.info["tabela_ll1"], self.info["inicio"])


if __name__ == "__main__":
    unittest.main(verbosity=2)