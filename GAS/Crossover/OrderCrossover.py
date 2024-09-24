"""
Order Crossover (OX) Class

This script defines the OrderCrossover class, which implements the order 
crossover method for genetic algorithms. The order crossover method creates 
offspring by taking a subsequence from one parent and preserving the order of 
the remaining elements from the other parent.

Classes:
    OrderCrossover: A class to perform order crossover on two parent individuals.

Functions:
    cross(parent1, parent2): Performs the order crossover operation on two parents.
"""
##
import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GAS.Crossover.base import Crossover
from GAS.Individual import Individual

# Order Crossover
class OrderCrossover(Crossover):
    """
    Implements the order crossover (OX) method for genetic algorithms.
    
    Attributes:
        pc (float): The probability of crossover.
    """
    
    def __init__(self, pc):
        """
        Initializes the OrderCrossover class with the specified crossover probability.
        
        Parameters:
            pc (float): The probability of crossover.
        """
        self.pc = pc

    def cross(self, parent1, parent2):
        """
        Performs the order crossover operation on two parents.
        
        Parameters:
            parent1 (Individual): The first parent individual.
            parent2 (Individual): The second parent individual.
        
        Returns:
            tuple: Two offspring individuals resulting from the crossover.
        """
        if random.random() > self.pc:
            return parent1, parent2

        point1, point2 = sorted(random.sample(range(len(parent1.seq)), 2))
        child1, child2 = parent1.seq[:], parent2.seq[:]

        # Create proto-children by inserting the selected substring into the corresponding positions
        child1[point1:point2], child2[point1:point2] = parent1.seq[point1:point2], parent2.seq[point1:point2]

        # Remove the selected substring symbols from the other parent
        temp1 = [item for item in parent2.seq if item not in parent1.seq[point1:point2]]
        temp2 = [item for item in parent1.seq if item not in parent2.seq[point1:point2]]

        # Fill unfixed positions
        idx1, idx2 = 0, 0
        for i in range(len(child1)):
            if not (point1 <= i < point2):
                child1[i] = temp1[idx1]
                idx1 += 1
                child2[i] = temp2[idx2]
                idx2 += 1

        return Individual(config=parent1.config, seq=child1, op_data=parent1.op_data), Individual(config=parent1.config, seq=child2, op_data=parent1.op_data)
