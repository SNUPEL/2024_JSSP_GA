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
        selected = []
        for _ in range(len(population)):
            total_fitness = sum(ind.fitness for ind in population)
            pick = random.uniform(0, total_fitness)
            current = 0
            for individual in population:
                current += individual.fitness
                if current > pick:
                    selected.append(copy.deepcopy(individual))
                    break
            if not selected:  # 만약 선택되지 않았다면 마지막 개체 추가
                selected.append(copy.deepcopy(population[-1]))
        return selected
