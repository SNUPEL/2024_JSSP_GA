"""
SwapMutation Class

This script defines the SwapMutation class, which implements the swap 
mutation method for genetic algorithms. The swap mutation method exchanges 
two randomly chosen elements in the individual's sequence.

Classes:
    SwapMutation: A class to perform swap mutation on an individual.

Functions:
    mutate(individual): Performs the swap mutation operation on an individual.
"""

import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GAS.Mutation.base import Mutation
from GAS.Individual import Individual

class SwapMutation(Mutation):
    """
    Implements the swap mutation method for genetic algorithms.
    
    Attributes:
        pm (float): The probability of mutation.
    """
    
    def __init__(self, pm):
        """
        Initializes the SwapMutation class with the specified mutation probability.
        
        Parameters:
            pm (float): The probability of mutation.
        """
        self.pm = pm

    def mutate(self, individual):
        """
        Performs the swap mutation operation on an individual.
        
        Parameters:
            individual (Individual): The individual to mutate.
        
        Returns:
            Individual: The mutated individual.
        """
        if random.random() < self.pm:
            seq = individual.seq[:]
            i, j = random.sample(range(len(seq)), 2)
            seq[i], seq[j] = seq[j], seq[i]
            return Individual(config=individual.config, seq=seq, op_data=individual.op_data)
        return individual
