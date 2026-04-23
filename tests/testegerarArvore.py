import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.gerarArvore import No


n = No("+", [No("A"), No("B")])
print(n)
print(n.filhos[0], n.filhos[1])