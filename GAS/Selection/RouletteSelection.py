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
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GAS.Individual import Individual

class RouletteSelection:
    """
    Implements the roulette wheel selection method for genetic algorithms.
    """
    
    def __init__(self):
        """
        Initializes the RouletteSelection class.
        """
        pass

    def select(self, population):
        """
        Selects an individual from the population based on roulette wheel selection.
        
        Parameters:
            population (list): The population to select from.
        
        Returns:
            Individual: The selected individual.
        """
        max_fitness = sum(ind.fitness for ind in population)
        pick = random.uniform(0, max_fitness)
        current = 0
        for individual in population:
            current += individual.fitness
            if current > pick:
                return individual
