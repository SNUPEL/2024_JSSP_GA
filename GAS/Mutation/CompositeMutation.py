import sys
import os
import random
import copy

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GAS.Individual import Individual
from GAS.Mutation.ShiftMutation import ShiftMutation
from GAS.Mutation.InsertionMutation import InsertionMutation
from GAS.Mutation.SwapMutation import SwapMutation
# [InsertionMutation(pm), ShiftMutation(pm), SwapMutation(pm)]
class CompositeMutation:
    def __init__(self, pm):
        self.pm = pm  # mutation 확률
        self.mutations = [ShiftMutation(pm), SwapMutation(pm)]  # 사용할 mutation 객체들

    def mutate(self, individual):
        if random.random() < self.pm:
            mutation = random.choice(self.mutations)  # 무작위로 mutation 방식 선택
            mutation.mutate(individual)  # 선택된 mutation 실행
        return individual