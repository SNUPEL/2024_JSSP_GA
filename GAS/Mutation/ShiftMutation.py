import sys
import os
import random
import copy
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GAS.Mutation.base import Mutation
from GAS.Individual import Individual
#  기존  min_shift_range=0.02, max_shift_range=0.3
# min_shifts=1, max_shifts=10, min_shift_range=0.02, max_shift_range=0.3
# 2개 10개
class ShiftMutation:
    def __init__(self, pm, min_shifts=1, max_shifts=5, min_shift_range=0.02, max_shift_range=0.2):
        self.pm = pm
        self.min_shifts = min_shifts
        self.max_shifts = max_shifts
        self.min_shift_range = min_shift_range
        self.max_shift_range = max_shift_range

    def mutate(self, individual):        
        if random.random() < self.pm:
            # print(f'ShiftMutation')
            original_seq = copy.deepcopy(individual.seq)  # 원래 시퀀스를 깊은 복사하여 비교에 사용
            seq = individual.seq
            size = len(seq)
            
            # 수행할 이동 횟수 결정
            num_shifts = random.randint(self.min_shifts, min(self.max_shifts, size // 2))
            
            for _ in range(num_shifts):
                pos = random.randint(0, size - 1)
                
                # 이동 범위 결정
                max_shift = int(size * random.uniform(self.min_shift_range, self.max_shift_range))
                shift = random.randint(-max_shift, max_shift)
                
                # 이동 수행
                gene = seq.pop(pos)
                new_pos = (pos + shift) % size
                seq.insert(new_pos, gene)
            
            # 디버깅을 위한 원래와 수정된 시퀀스 출력
            # print(f"원래 시퀀스: {original_seq}")
            # print(f"수정된 시퀀스: {seq}")
        return individual
