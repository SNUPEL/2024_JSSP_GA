import sys
import os
import random
import copy
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GAS.Mutation.base import Mutation
from GAS.Individual import Individual

class InversionMutation:
    def __init__(self, pm, min_inverse_ratio=0.02, max_inverse_ratio=0.1):
        self.pm = pm
        self.min_inverse_ratio = min_inverse_ratio  # 최소 역위 길이 비율
        self.max_inverse_ratio = max_inverse_ratio  # 최대 역위 길이 비율

    def mutate(self, individual):
        if random.random() < self.pm:
            original_seq = copy.deepcopy(individual.seq)  # 깊은 복사로 원래 시퀀스를 보존
            size = len(original_seq)

            # 역위 횟수를 비율로 결정
            min_inversions = max(1, int(size * self.min_inverse_ratio))
            max_inversions = min(size, int(size * self.max_inverse_ratio))
            num_inversions = random.randint(min_inversions, max_inversions)

            for _ in range(num_inversions):
                # 역위 길이를 비율로 계산
                min_inverse_length = max(2, int(size * self.min_inverse_ratio))
                max_inverse_length = min(size - 1, int(size * self.max_inverse_ratio))
                inverse_length = random.randint(min_inverse_length, max_inverse_length)

                start = random.randint(0, size - inverse_length)
                end = start + inverse_length
                original_seq[start:end] = reversed(original_seq[start:end])

            # 깊은 복사로 새로운 시퀀스로 개체 생성
            new_individual = copy.deepcopy(individual)
            new_individual.seq = original_seq

            return new_individual

        return individual
