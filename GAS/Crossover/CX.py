import sys
import os
import random
import copy
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GAS.Crossover.base import Crossover
from GAS.Individual import Individual
import random
import copy

class CXCrossover:
    def __init__(self, pc):
        self.pc = pc

    def cross(self, parent1, parent2):
        # print(f'CXCrossover')
        # print(f"Starting crossover between:\nParent1: {parent1.seq}\nParent2: {parent2.seq}")
        if random.random() > self.pc:
            return copy.deepcopy(parent1), copy.deepcopy(parent2)

        size = len(parent1.seq)
        child1_seq = [None] * size
        child2_seq = [None] * size

        def create_cycle(parent1_seq, parent2_seq, max_attempts=10):
            cycle = []
            visited = [False] * size
            attempts = 0

            while attempts < max_attempts:
                cycle.clear()  # 이전에 생성된 사이클을 초기화
                start_index = random.randint(0, size - 1)  # 랜덤한 시작 인덱스 선택
                index = start_index
                while not visited[index]:
                    cycle.append(index)
                    visited[index] = True
                    index = parent1_seq.index(parent2_seq[index])

                if len(cycle) > 1:
                    break  # 사이클이 1개 이상일 때만 종료
                else:
                    attempts += 1
                    visited = [False] * size  # 방문 기록 초기화

            if attempts >= max_attempts:
                print("Max attempts reached, returning the current cycle.")
            
            return cycle

        cycle_indices = create_cycle(parent1.seq, parent2.seq)
        # print(f"Cycle indices: {cycle_indices}")

        for i in cycle_indices:
            child1_seq[i] = parent1.seq[i]
            child2_seq[i] = parent2.seq[i]

        for i in range(size):
            if child1_seq[i] is None:
                child1_seq[i] = parent2.seq[i]
            if child2_seq[i] is None:
                child2_seq[i] = parent1.seq[i]

        # print(f"Child1 sequence after crossover: {child1_seq}")
        # print(f"Child2 sequence after crossover: {child2_seq}")
        child1 = Individual(config=parent1.config, seq=child1_seq, op_data=parent1.op_data)
        child2 = Individual(config=parent2.config, seq=child2_seq, op_data=parent2.op_data)

        return child1, child2



