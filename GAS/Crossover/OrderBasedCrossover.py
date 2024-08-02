"""
Order-Based Crossover (OBC) Class

This script defines the OBC class, which implements the order-based crossover 
method for genetic algorithms. The order-based crossover method selects positions 
from one parent and fills the remaining positions in the order they appear in 
the other parent.

Classes:
    OBC: A class to perform order-based crossover on two parent individuals.

Functions:
    cross(parent1, parent2): Performs the order-based crossover operation on two parents.
"""

import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GAS.Crossover.base import Crossover
from GAS.Individual import Individual

# Order-Based Crossover
class OBC(Crossover):
    """
    Implements the order-based crossover (OBC) method for genetic algorithms.
    
    Attributes:
        pc (float): The probability of crossover.
    """
    
    def __init__(self, pc):
        """
        Initializes the OBC class with the specified crossover probability.
        
        Parameters:
            pc (float): The probability of crossover.
        """
        self.pc = pc

    def cross(self, parent1, parent2):
        """
        Performs the order-based crossover operation on two parents.
        
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

        # Step 1: Select positions from Parent 1
        positions = sorted(random.sample(range(size), random.randint(1, size - 1)))

        # Step 2: Produce Proto-child
        for pos in positions:
            child1[pos] = parent1.seq[pos]
            child2[pos] = parent2.seq[pos]

        # Step 3: Remove selected positions' symbols from the other parent
        parent2_filtered = [item for item in parent2.seq if item not in child1]
        parent1_filtered = [item for item in parent1.seq if item not in child2]

        # Step 4: Fill unfixed positions in the order of the other parent
        idx1, idx2 = 0, 0
        for i in range(size):
            if child1[i] is None:
                child1[i] = parent2_filtered[idx1]
                idx1 += 1
            if child2[i] is None:
                child2[i] = parent1_filtered[idx2]
                idx2 += 1

        return Individual(config=parent1.config, seq=child1, op_data=parent1.op_data), Individual(config=parent1.config, seq=child2, op_data=parent2.op_data)
