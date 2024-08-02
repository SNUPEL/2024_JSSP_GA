"""
GeneralMutation Class

This script defines the GeneralMutation class, which implements a general mutation 
method for genetic algorithms. The general mutation method swaps two random elements 
in the individual's sequence with a certain probability.

Classes:
    GeneralMutation: A class to perform general mutation on an individual.

Functions:
    mutate(individual): Performs the general mutation operation on an individual.
"""

import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GAS.Mutation.base import Mutation
from GAS.Individual import Individual

class GeneralMutation(Mutation):
    """
    Implements a general mutation method for genetic algorithms.
    
    Attributes:
        pm (float): The probability of mutation.
    """
    
    def __init__(self, pm):
        """
        Initializes the GeneralMutation class with the specified mutation probability.
        
        Parameters:
            pm (float): The probability of mutation.
        """
        self.pm = pm

    def mutate(self, individual):
        """
        Performs the general mutation operation on an individual.
        
        Parameters:
            individual (Individual): The individual to mutate.
        
        Returns:
            Individual: The mutated individual.
        """
        seq = individual.seq[:]
        for i in range(len(seq)):
            if random.random() < self.pm:
                j = random.randint(0, len(seq) - 1)
                seq[i], seq[j] = seq[j], seq[i]
        return Individual(config=individual.config, seq=seq, op_data=individual.op_data)
