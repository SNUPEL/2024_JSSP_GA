"""
RouletteSelection Class

This script defines the RouletteSelection class, which implements the roulette 
wheel selection method for genetic algorithms. The roulette wheel selection method 
selects individuals from the population based on their fitness proportion.

Classes:
    RouletteSelection: A class to perform roulette wheel selection on a population.

Functions:
    select(population): Selects an individual from the population based on roulette wheel selection.
"""

import sys
import os
import random
import copy
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GAS.Individual import Individual

# class RouletteSelection:
#     """
#     Implements the roulette wheel selection method for genetic algorithms.
#     """
    
#     def __init__(self):
#         """
#         Initializes the RouletteSelection class.
#         """
#         pass

#     def select(self, population):
#         """
#         Selects an individual from the population based on roulette wheel selection.
        
#         Parameters:
#             population (list): The population to select from.
        
#         Returns:
#             Individual: The selected individual.
#         """
#         max_fitness = sum(ind.fitness for ind in population)
#         pick = random.uniform(0, max_fitness)
#         current = 0
#         for individual in population:
#             current += individual.fitness
#             if current > pick:
#                 return individual
class RouletteSelection:
    def __init__(self):
        pass

    def select(self, population):
        # 1) population 유효성 체크
        if not population:
            raise ValueError("Population is empty or None.")

        # 2) 전체 적합도 합 계산
        total_fitness = sum(ind.fitness for ind in population)

        # 3) 적합도가 0이면 선택 불가능하므로 예외 처리
        if total_fitness == 0:
            raise ValueError("Total fitness of the population is zero.")

        # 4) 랜덤 포인트 pick 설정
        pick = random.uniform(0, total_fitness)
        
        # 5) 누적 적합도를 증가시키며 pick을 넘은 개체 선택
        current = 0
        for individual in population:
            current += individual.fitness
            if current >= pick:
                # 다른 곳에서 `seq` 같은 속성을 사용할 수 있도록
                # `copy.deepcopy`로 개체 반환
                return copy.deepcopy(individual)
        
        # 6) 혹시 누락이 있다면 마지막 개체 반환 (fallback)
        return copy.deepcopy(population[-1])
