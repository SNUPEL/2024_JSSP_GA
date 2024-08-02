"""
ReciprocalExchangeMutation Class

This script defines the ReciprocalExchangeMutation class, which implements the 
reciprocal exchange mutation method for genetic algorithms. The reciprocal exchange 
mutation method swaps two randomly chosen elements in the individual's sequence.

Classes:
    ReciprocalExchangeMutation: A class to perform reciprocal exchange mutation on an individual.

Functions:
    mutate(individual): Performs the reciprocal exchange mutation operation on an individual.
"""

import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GAS.Mutation.base import Mutation
from GAS.Individual import Individual

class ReciprocalExchangeMutation(Mutation):
    """
    Implements the reciprocal exchange mutation method for genetic algorithms.
    
    Attributes:
        pm (float): The probability of mutation.
    """
    
    def __init__(self, pm):
        """
        Initializes the ReciprocalExchangeMutation class with the specified mutation probability.
        
        Parameters:
            pm (float): The probability of mutation.
        """
        self.pm = pm

    def mutate(self, individual):
        """
        Performs the reciprocal exchange mutation operation on an individual.
        
        Parameters:
            individual (Individual): The individual to mutate.
        
        Returns:
            Individual: The mutated individual.
        """
        if random.random() < self.pm:
            seq = individual.seq[:]
            pos1, pos2 = random.sample(range(len(seq)), 2)
            seq[pos1], seq[pos2] = seq[pos2], seq[pos1]
            return Individual(config=individual.config, seq=seq, op_data=individual.op_data)
        return individual
