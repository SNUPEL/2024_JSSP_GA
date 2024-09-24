import sys
import os
import random
import copy

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GAS.Individual import Individual
from GAS.Crossover.CX import CXCrossover  # 예시로 CXCrossover 사용
from GAS.Crossover.SXX import SXX
from GAS.Crossover.PMX import PMXCrossover

#         self.crossovers = [CXCrossover(pc=pc), CXCrossover_origin(pc=pc)]
class CompositeCrossover:
    def __init__(self, pc):
        # 내부에서 사용할 Crossover 방식을 선언
        self.crossovers = [PMXCrossover(pc=pc)]
        self.pc = pc  # crossover 확률

    def cross(self, parent1, parent2):
        if random.random() < self.pc:
            crossover = random.choice(self.crossovers)  # 무작위로 crossover 방식 선택
            return crossover.cross(parent1, parent2)  # 선택된 crossover 실행
        else:
            return copy.deepcopy(parent1), copy.deepcopy(parent2)
