import sys
import os
import random
import copy
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GAS.Mutation.base import Mutation
from GAS.Individual import Individual

class SwapMutation:
    def __init__(self, pm, min_swap_ratio=0.02, max_swap_ratio=0.2):
        self.pm = pm
        self.min_swap_ratio = min_swap_ratio
        self.max_swap_ratio = max_swap_ratio

    def mutate(self, individual):
        if random.random() < self.pm:
            # original_seq = copy.deepcopy(individual.seq)  # 원래 시퀀스를 깊은 복사하여 비교에 사용
            seq = individual.seq
            size = len(seq)
            num_jobs = individual.config.n_job  # Job 수 가져오기
            
            # 각 Operation이 어느 Job에 속하는지 계산 (index에 해당하는 Job 번호)
            job_indices = [i // individual.config.n_machine for i in range(size)]

            # 염색체 길이에 대한 상대적 비율로 교환 횟수 결정
            min_swaps = max(1, int(size * self.min_swap_ratio))
            max_swaps = min(size, int(size * self.max_swap_ratio))
            num_swaps = random.randint(min_swaps, max_swaps)

            for _ in range(num_swaps):
                i = random.randint(0, size - 1)
                
                # i와 다른 Job에 속하는 j를 찾을 때까지 반복
                different_job_indices = [j for j in range(size) if job_indices[j] != job_indices[i]]
                
                # 무조건 다른 Job에 속하는 Operation을 선택
                if different_job_indices:
                    j = random.choice(different_job_indices)
                    seq[i], seq[j] = seq[j], seq[i]
            
            # 디버깅을 위한 원래와 수정된 시퀀스 출력
            # print(f"Original sequence: {original_seq}")
            # print(f"Modified sequence: {seq}")
        return individual
