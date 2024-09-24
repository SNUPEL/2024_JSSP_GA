import sys
import os
import random
import copy
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GAS.Mutation.base import Mutation
from GAS.Individual import Individual

class DisplacementMutation:
    def __init__(self, pm, min_displacement_ratio=0.02, max_displacement_ratio=0.3):
        self.pm = pm
        self.min_displacement_ratio = min_displacement_ratio  # 최소 변위 비율
        self.max_displacement_ratio = max_displacement_ratio  # 최대 변위 비율

    def mutate(self, individual):
        if random.random() < self.pm:
            original_seq = copy.deepcopy(individual.seq)  # 원래 시퀀스를 깊은 복사하여 비교에 사용
            seq = individual.seq
            size = len(seq)

            # 염색체 길이에 대한 상대적 비율로 변위 횟수 결정
            min_displacements = max(1, int(size * self.min_displacement_ratio))
            max_displacements = min(size, int(size * self.max_displacement_ratio))
            num_displacements = random.randint(min_displacements, max_displacements)

            for _ in range(num_displacements):
                displacement_length = random.randint(min_displacements, max_displacements)
                start = random.randint(0, size - displacement_length)
                end = start + displacement_length

                # 변위할 부분 문자열 추출
                sub_seq = seq[start:end]

                # 추출한 부분 문자열 제거
                del seq[start:end]

                # 새로운 위치 선택 (원래 위치는 제외)
                remaining_positions = list(range(start)) + list(range(start, len(seq) + 1))
                insert_pos = random.choice(remaining_positions)

                # 새로운 위치에 삽입
                seq[insert_pos:insert_pos] = sub_seq

        return individual
