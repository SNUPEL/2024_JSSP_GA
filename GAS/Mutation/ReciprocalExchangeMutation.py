import sys
import os
import random
import copy
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GAS.Mutation.base import Mutation
from GAS.Individual import Individual

class ReciprocalExchangeMutation:
    def __init__(self, pm, min_reciprocal_ratio=0.02, max_reciprocal_ratio=0.1):
        self.pm = pm
        self.min_reciprocal_ratio = min_reciprocal_ratio  # 최소 교환 비율
        self.max_reciprocal_ratio = max_reciprocal_ratio  # 최대 교환 비율

    def mutate(self, individual):
        if random.random() < self.pm:
            original_seq = copy.deepcopy(individual.seq)  # 원래 시퀀스를 깊은 복사하여 비교에 사용
            seq = individual.seq
            size = len(seq)
            
            # 교환 횟수를 비율로 결정
            min_reciprocal = max(1, int(size * self.min_reciprocal_ratio))
            max_reciprocal = min(size, int(size * self.max_reciprocal_ratio))
            
            num_reciprocal = random.randint(min_reciprocal, max_reciprocal)
            
            for _ in range(num_reciprocal):
                pos1, pos2 = random.sample(range(size), 2)
                seq[pos1], seq[pos2] = seq[pos2], seq[pos1]
            
            # 디버깅을 위한 원래와 수정된 시퀀스 출력
            # print(f"원래 시퀀스: {original_seq}")
            # print(f"수정된 시퀀스: {seq}")

        return individual

