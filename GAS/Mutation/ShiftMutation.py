"""
ShiftMutation Class

This script defines the ShiftMutation class, which implements the shift 
mutation method for genetic algorithms. The shift mutation method removes 
an element from the individual's sequence and inserts it at a shifted position.

Classes:
    ShiftMutation: A class to perform shift mutation on an individual.

Functions:
    mutate(individual): Performs the shift mutation operation on an individual.
"""

import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GAS.Mutation.base import Mutation
from GAS.Individual import Individual

class ShiftMutation(Mutation):
    """
    Implements the shift mutation method for genetic algorithms.
    
    Attributes:
        pm (float): The probability of mutation.
    """
    
    def __init__(self, pm):
        """
        Initializes the ShiftMutation class with the specified mutation probability.
        
        Parameters:
            pm (float): The probability of mutation.
        """
        self.pm = pm

    def mutate(self, individual):
        """
        Performs the shift mutation operation on an individual.
        
        Parameters:
            individual (Individual): The individual to mutate.
        
        Returns:
            Individual: The mutated individual.
        """
        if random.random() < self.pm:
            seq = individual.seq[:]
            pos = random.randint(0, len(seq) - 1)
            shift = random.randint(-len(seq) + 1, len(seq) - 1)
            gene = seq.pop(pos)
            seq.insert((pos + shift) % len(seq), gene)
            return Individual(config=individual.config, seq=seq, op_data=individual.op_data)
        return individual
