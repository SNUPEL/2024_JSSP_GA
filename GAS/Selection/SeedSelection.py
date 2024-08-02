"""
SeedSelection Class

This script defines the SeedSelection class, which implements a custom selection 
method for genetic algorithms. The selection method chooses the most fit individual 
(male) with a probability k and a random individual (female) otherwise.

Classes:
    SeedSelection: A class to perform seed selection on a population.

Functions:
    select(population): Selects an individual from the population based on the seed selection method.
"""

import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GAS.Individual import Individual

class SeedSelection:
    """
    Implements a custom seed selection method for genetic algorithms.
    
    Attributes:
        k (float): The probability of selecting the most fit individual.
    """
    
    def __init__(self, k=0.75):
        """
        Initializes the SeedSelection class with the specified probability.
        
        Parameters:
            k (float): The probability of selecting the most fit individual (default is 0.75).
        """
        self.k = k  # 확률값 k 설정

    def select(self, population):
        """
        Selects an individual from the population based on the seed selection method.
        
        Parameters:
            population (list): The population to select from.
        
        Returns:
            Individual: The selected individual.
        """
        # male: 가장 적합한 염색체
        male = max(population, key=lambda ind: ind.fitness)
        # female: 랜덤하게 선택
        female = random.choice(population)
        # 확률 k에 따라 male 또는 female 선택
        selected = male if random.random() < self.k else female
        return selected
