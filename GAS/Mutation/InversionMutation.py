"""
InversionMutation Class

This script defines the InversionMutation class, which implements the inversion 
mutation method for genetic algorithms. The inversion mutation method reverses 
a subsequence within the individual's sequence.

Classes:
    InversionMutation: A class to perform inversion mutation on an individual.

Functions:
    mutate(individual): Performs the inversion mutation operation on an individual.
"""

import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GAS.Mutation.base import Mutation
from GAS.Individual import Individual

class InversionMutation(Mutation):
    """
    Implements the inversion mutation method for genetic algorithms.
    
    Attributes:
        pm (float): The probability of mutation.
    """
    
    def __init__(self, pm):
        """
        Initializes the InversionMutation class with the specified mutation probability.
        
        Parameters:
            pm (float): The probability of mutation.
        """
        self.pm = pm

    def mutate(self, individual):
        """
        Performs the inversion mutation operation on an individual.
        
        Parameters:
            individual (Individual): The individual to mutate.
        
        Returns:
            Individual: The mutated individual.
        """
        if random.random() < self.pm:
            seq = individual.seq[:]
            start, end = sorted(random.sample(range(len(seq)), 2))
            original_seq = seq[:]
            seq[start:end] = seq[start:end][::-1]
            return Individual(config=individual.config, seq=seq, op_data=individual.op_data)
        return individual
