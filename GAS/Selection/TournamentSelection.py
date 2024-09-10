import random
import copy
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GAS.Individual import Individual

class TournamentSelection:
    def __init__(self, tournament_size=2):
        self.tournament_size = tournament_size

    def select(self, population):
        # 토너먼트에 참가할 염색체 무작위 선택
        tournament = random.sample(population, self.tournament_size)
        
        # 토너먼트에서 가장 적합한 염색체 선택 (makespan이 작은 염색체를 선택)
        winner = min(tournament, key=lambda ind: ind.makespan)
        
        # 선택된 개체의 복사본을 반환
        return copy.deepcopy(winner)