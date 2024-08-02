"""
Partially Ordered Crossover (POX) Class

This script defines the POXCrossover class, which implements the partially 
ordered crossover method for genetic algorithms. The partially ordered crossover 
method selects a subsequence from one parent and inserts corresponding elements 
from the other parent, then fills the remaining positions.

Classes:
    POXCrossover: A class to perform partially ordered crossover on two parent individuals.

Functions:
    cross(parent1, parent2): Performs the partially ordered crossover operation on two parents.
"""

import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GAS.Crossover.base import Crossover
from GAS.Individual import Individual

class POXCrossover(Crossover):
    """
    Implements the partially ordered crossover (POX) method for genetic algorithms.
    
    Attributes:
        pc (float): The probability of crossover.
    """
    
    def __init__(self, pc):
        """
        Initializes the POXCrossover class with the specified crossover probability.
        
        Parameters:
            pc (float): The probability of crossover.
        """
        self.pc = pc

    def cross(self, parent1, parent2):
        """
        Performs the partially ordered crossover operation on two parents.
        
        Parameters:
            parent1 (Individual): The first parent individual.
            parent2 (Individual): The second parent individual.
        
        Returns:
            tuple: Two offspring individuals resulting from the crossover.
        """
        if random.random() > self.pc:
            return parent1, parent2

        seq_length = len(parent1.seq)
        child1_seq = [-1] * seq_length
        child2_seq = [-1] * seq_length

        # Step 1: Select a subsequence from each parent
        sub_jobs = random.sample(range(seq_length), 2)
        sub_jobs.sort()
        sj1, sj2 = sub_jobs[0], sub_jobs[1]

        # Step 2: Copy the subsequence from each parent to the corresponding child
        child1_seq[sj1:sj2+1] = parent1.seq[sj1:sj2+1]
        child2_seq[sj1:sj2+1] = parent2.seq[sj1:sj2+1]

        # Step 3: Remove the selected subsequence symbols from the other parent
        p2_remaining_genes = [gene for gene in parent2.seq if gene not in parent1.seq[sj1:sj2+1]]
        p1_remaining_genes = [gene for gene in parent1.seq if gene not in parent2.seq[sj1:sj2+1]]

        # Step 4: Fill the remaining positions in the children with the remaining genes
        child1_index, child2_index = 0, 0
        for i in range(seq_length):
            if child1_seq[i] == -1:
                child1_seq[i] = p2_remaining_genes[child1_index]
                child1_index += 1
            if child2_seq[i] == -1:
                child2_seq[i] = p1_remaining_genes[child2_index]
                child2_index += 1

        return Individual(config=parent1.config, seq=child1_seq, machine_assignment=parent1.machine_assignment, op_data=parent1.op_data), Individual(config=parent1.config, seq=child2_seq, machine_assignment=parent2.machine_assignment, op_data=parent1.op_data)
