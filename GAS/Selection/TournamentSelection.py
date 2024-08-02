"""
TournamentSelection Class

This script defines the TournamentSelection class, which implements the tournament 
selection method for genetic algorithms. The tournament selection method selects 
a subset of the population and chooses the most fit individual from that subset.

Classes:
    TournamentSelection: A class to perform tournament selection on a population.

Functions:
    select(population): Selects an individual from the population based on the tournament selection method.
"""

import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GAS.Individual import Individual

class TournamentSelection:
    """
    Implements the tournament selection method for genetic algorithms.
    
    Attributes:
        tournament_size (int): The number of individuals in the tournament.
    """
    
    def __init__(self, tournament_size=2):
        """
        Initializes the TournamentSelection class with the specified tournament size.
        
        Parameters:
            tournament_size (int): The number of individuals in the tournament (default is 2).
        """
        self.tournament_size = tournament_size

    def select(self, population):
        """
        Selects an individual from the population based on the tournament selection method.
        
        Parameters:
            population (list): The population to select from.
        
        Returns:
            Individual: The selected individual.
        """
        # 토너먼트에 참가할 염색체 무작위 선택
        tournament = random.sample(population, self.tournament_size)
        # 토너먼트에서 가장 적합한 염색체 선택
        winner = max(tournament, key=lambda ind: ind.fitness)
        return winner
