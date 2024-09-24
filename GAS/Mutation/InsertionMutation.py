import sys
import os
import random
import copy
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GAS.Mutation.base import Mutation
from GAS.Individual import Individual

class InsertionMutation:
    def __init__(self, pm, min_insert_ratio=0.02, max_insert_ratio=0.1):
        self.pm = pm
        self.min_insert_ratio = min_insert_ratio  # 최소 삽입 비율
        self.max_insert_ratio = max_insert_ratio  # 최대 삽입 비율

    def mutate(self, individual):
        if random.random() < self.pm:
            print(f'InsertionMutation')
            original_seq = copy.deepcopy(individual.seq)  # 원래 시퀀스를 깊은 복사하여 비교에 사용
            seq = copy.deepcopy(individual.seq)  # 깊은 복사로 시퀀스의 일관성 유지
            size = len(seq)

            # 삽입 횟수를 비율로 결정
            min_insertions = max(1, int(size * self.min_insert_ratio))
            max_insertions = min(size, int(size * self.max_insert_ratio))
            num_insertions = random.randint(2, 10)
            
            for _ in range(num_insertions):
                # 삽입 길이를 비율로 계산
                min_insert_length = max(1, int(size * self.min_insert_ratio))
                max_insert_length = min(size // 2, int(size * self.max_insert_ratio))
                insert_length = random.randint(min_insert_length, max_insert_length)

                start = random.randint(0, len(seq) - insert_length)  # seq 크기를 재조정
                end = start + insert_length

                # 삽입 위치를 결정 (start와 end 범위와 상관없는 곳에 삽입)
                insert_pos = random.randint(0, len(seq) - insert_length)
                if insert_pos >= start:  # insert_pos가 삭제 범위 이후로 밀리는 경우를 보정
                    insert_pos += insert_length

                # 삽입할 세그먼트를 추출
                genes_to_insert = copy.deepcopy(seq[start:end])  # 깊은 복사로 세그먼트 유지

                # 추출한 세그먼트를 제거
                del seq[start:end]

                # 새로운 위치에 세그먼트를 삽입
                for gene in reversed(genes_to_insert):
                    seq.insert(insert_pos, gene)

            # 최종적으로 수정된 시퀀스를 individual에 반영
            individual.seq = seq

            # 디버깅을 위한 원래와 수정된 시퀀스 출력
            # print(f"원래 시퀀스: {original_seq}")
            # print(f"수정된 시퀀스: {seq}")
        return individual
