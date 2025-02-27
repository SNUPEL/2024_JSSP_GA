"""
Job-Based Crossover (JBX) Class

This script defines the JBX class, which implements the job-based crossover 
method for genetic algorithms. The job-based crossover method segments the 
sequence of jobs and swaps segments between parents to create offspring.

Classes:
    JBX: A class to perform job-based crossover on two parent individuals.

Functions:
    cross(parent1, parent2): Performs the job-based crossover operation on two parents.
"""

import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GAS.Crossover.base import Crossover
from GAS.Individual import Individual

class JBX(Crossover):
    """
    Implements the job-based crossover (JBX) method for genetic algorithms.
    
    Attributes:
        pc (float): The probability of crossover.
    """
    
    def __init__(self, pc):
        """
        Initializes the JBX class with the specified crossover probability.
        
        Parameters:
            pc (float): The probability of crossover.
        """
        self.pc = pc

    def cross(self, parent1, parent2):
        """
        Performs the job-based crossover operation on two parents.
        
        Parameters:
            parent1 (Individual): The first parent individual.
            parent2 (Individual): The second parent individual.
        
        Returns:
            tuple: Two offspring individuals resulting from the crossover.
        """
        if random.random() > self.pc:
            return parent1, parent2

        # Job-based crossover points
        jobs = list(set(parent1.seq))
        num_jobs = len(jobs)
        job_point1, job_point2 = sorted(random.sample(range(num_jobs), 2))

        # Create empty child sequences
        child1, child2 = [-1] * len(parent1.seq), [-1] * len(parent2.seq)

        # Keep the job segments
        job_segment1 = jobs[job_point1:job_point2]
        job_segment2 = jobs[job_point1:job_point2]

        # Copy the job segments to children
        for i in range(len(parent1.seq)):
            if parent1.seq[i] in job_segment1:
                child1[i] = parent1.seq[i]
            if parent2.seq[i] in job_segment2:
                child2[i] = parent2.seq[i]

        # Fill the remaining positions with the jobs from the other parent
        current_pos1, current_pos2 = 0, 0
        for i in range(len(parent1.seq)):
            if child1[i] == -1:
                while parent2.seq[current_pos1] in job_segment1:
                    current_pos1 += 1
                child1[i] = parent2.seq[current_pos1]
                current_pos1 += 1

            if child2[i] == -1:
                while parent1.seq[current_pos2] in job_segment2:
                    current_pos2 += 1
                child2[i] = parent1.seq[current_pos2]
                current_pos2 += 1

        return Individual(config=parent1.config, seq=child1, op_data=parent1.op_data), Individual(config=parent2.config, seq=child2, op_data=parent2.op_data)
