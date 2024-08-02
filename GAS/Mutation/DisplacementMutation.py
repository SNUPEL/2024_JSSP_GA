"""
DisplacementMutation Class

This script defines the DisplacementMutation class, which implements the 
displacement mutation method for genetic algorithms. The displacement mutation 
method removes a subsequence from the individual and inserts it at a random position.

Classes:
    DisplacementMutation: A class to perform displacement mutation on an individual.

Functions:
    mutate(individual): Performs the displacement mutation operation on an individual.
"""

import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GAS.Mutation.base import Mutation
from GAS.Individual import Individual

class DisplacementMutation(Mutation):
    """
    Implements the displacement mutation method for genetic algorithms.
    
    Attributes:
        pm (float): The probability of mutation.
    """
    
    def __init__(self, pm):
        """
        Initializes the DisplacementMutation class with the specified mutation probability.
        
        Parameters:
            pm (float): The probability of mutation.
        """
        self.pm = pm

    def mutate(self, individual):
        """
        Performs the displacement mutation operation on an individual.
        
        Parameters:
            individual (Individual): The individual to mutate.
        
        Returns:
            Individual: The mutated individual.
        """
        if random.random() < self.pm:
            seq = individual.seq[:]
            start, end = sorted(random.sample(range(len(seq)), 2))
            sub_seq = seq[start:end]
            seq = seq[:start] + seq[end:]
            pos = random.randint(0, len(seq))
            seq = seq[:pos] + sub_seq + seq[pos:]
            return Individual(config=individual.config, seq=seq, op_data=individual.op_data)
        return individual
