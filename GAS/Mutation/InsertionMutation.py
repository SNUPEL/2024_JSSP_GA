"""
InsertionMutation Class

This script defines the InsertionMutation class, which implements the insertion 
mutation method for genetic algorithms. The insertion mutation method removes 
an element from the individual's sequence and inserts it at a random position.

Classes:
    InsertionMutation: A class to perform insertion mutation on an individual.

Functions:
    mutate(individual): Performs the insertion mutation operation on an individual.
"""

import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GAS.Mutation.base import Mutation
from GAS.Individual import Individual

class InsertionMutation(Mutation):
    """
    Implements the insertion mutation method for genetic algorithms.
    
    Attributes:
        pm (float): The probability of mutation.
    """
    
    def __init__(self, pm):
        """
        Initializes the InsertionMutation class with the specified mutation probability.
        
        Parameters:
            pm (float): The probability of mutation.
        """
        self.pm = pm

    def mutate(self, individual):
        """
        Performs the insertion mutation operation on an individual.
        
        Parameters:
            individual (Individual): The individual to mutate.
        
        Returns:
            Individual: The mutated individual.
        """
        if random.random() < self.pm:
            seq = individual.seq[:]
            pos1 = random.randint(0, len(seq) - 1)
            pos2 = random.randint(0, len(seq) - 1)
            gene = seq.pop(pos1)
            seq.insert(pos2, gene)
            return Individual(config=individual.config, seq=seq, op_data=individual.op_data)
        return individual
