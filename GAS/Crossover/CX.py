"""
Cycle Crossover (CX) Class

This script defines the CXCrossover class, which implements the cycle crossover
method for genetic algorithms. The cycle crossover method ensures that each
position in the offspring receives a value from one of the parents, forming cycles
to preserve the order.

Classes:
    CXCrossover: A class to perform cycle crossover on two parent individuals.

Functions:
    cross(parent1, parent2): Performs the cycle crossover operation on two parents.
"""

import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GAS.Crossover.base import Crossover
from GAS.Individual import Individual

# Cycle crossover 
class CXCrossover(Crossover):
    """
    Implements the cycle crossover (CX) method for genetic algorithms.
    
    Attributes:
        pc (float): The probability of crossover.
    """
    
    def __init__(self, pc):
        """
        Initializes the CXCrossover class with the specified crossover probability.
        
        Parameters:
            pc (float): The probability of crossover.
        """
        self.pc = pc

    def cross(self, parent1, parent2):
        """
        Performs the cycle crossover operation on two parents.
        
        Parameters:
            parent1 (Individual): The first parent individual.
            parent2 (Individual): The second parent individual.
        
        Returns:
            tuple: Two offspring individuals resulting from the crossover.
        """
        if random.random() > self.pc:
            return parent1, parent2

        size = len(parent1.seq)
        child1, child2 = [None] * size, [None] * size

        def create_cycle(parent1_seq, parent2_seq):
            """
            Creates a cycle from the sequences of the parents.
            
            Parameters:
                parent1_seq (list): The sequence of the first parent.
                parent2_seq (list): The sequence of the second parent.
            
            Returns:
                list: A list of indices forming a cycle.
            """
            cycle = []
            index = 0
            while index not in cycle:
                cycle.append(index)
                index = parent1_seq.index(parent2_seq[index])
            return cycle

        cycle_indices = create_cycle(parent1.seq, parent2.seq)

        for i in cycle_indices:
            child1[i], child2[i] = parent1.seq[i], parent2.seq[i]

        for i in range(size):
            if child1[i] is None:
                child1[i] = parent2.seq[i]
            if child2[i] is None:
                child2[i] = parent1.seq[i]

        return Individual(config=parent1.config, seq=child1, op_data=parent1.op_data), Individual(config=parent1.config, seq=child2, op_data=parent1.op_data)
