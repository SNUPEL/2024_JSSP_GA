"""
Partially Shifted Crossover (PSX) Class

This script defines the PSXCrossover class, which implements the partially 
shifted crossover method for genetic algorithms. The partially shifted crossover 
method exchanges partial schedules between parents and adjusts the offspring 
to ensure valid sequences.

Classes:
    PSXCrossover: A class to perform partially shifted crossover on two parent individuals.

Functions:
    cross(parent1, parent2): Performs the partially shifted crossover operation on two parents.
"""

import sys
import os
import random
from copy import deepcopy
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GAS.Crossover.base import Crossover
from GAS.Individual import Individual

class PSXCrossover(Crossover):
    """
    Implements the partially shifted crossover (PSX) method for genetic algorithms.
    
    Attributes:
        pc (float): The probability of crossover.
    """
    
    def __init__(self, pc):
        """
        Initializes the PSXCrossover class with the specified crossover probability.
        
        Parameters:
            pc (float): The probability of crossover.
        """
        self.pc = pc

    def cross(self, parent1, parent2):
        """
        Performs the partially shifted crossover operation on two parents.
        
        Parameters:
            parent1 (Individual): The first parent individual.
            parent2 (Individual): The second parent individual.
        
        Returns:
            tuple: Two offspring individuals resulting from the crossover.
        """
        if random.random() > self.pc:
            return parent1, parent2

        size = len(parent1.seq)
        point1, point2 = sorted(random.sample(range(size), 2))

        # Step 1: Identify a partial schedule in one parent and identify the corresponding part in the other parent
        partial1 = parent1.seq[point1:point2]
        partial2 = []

        # Find the corresponding part in parent2 centered around the same jobs as in parent1
        start_index = None
        for i in range(size):
            if parent2.seq[i] in partial1:
                start_index = i
                break
        if start_index is not None:
            end_index = start_index + len(partial1)
            partial2 = parent2.seq[start_index:end_index]

        # Step 2: Exchange the partial schedules to create proto-offspring
        proto_offspring1 = deepcopy(parent1.seq)
        proto_offspring2 = deepcopy(parent2.seq)
        
        proto_offspring1[point1:point2] = partial2
        proto_offspring2[start_index:end_index] = partial1

        # Step 3: Legalize the proto-offspring by removing excess genes and adding missing genes
        def legalize(proto, original):
            """
            Adjusts the proto-offspring to ensure valid sequences by removing excess genes
            and adding missing genes.
            
            Parameters:
                proto (list): The proto-offspring sequence.
                original (list): The original parent sequence.
            
            Returns:
                list: The legalized offspring sequence.
            """
            original_set = set(original)
            proto_set = set(proto)
            
            missing_genes = list(original_set - proto_set)
            excess_genes = [gene for gene in proto if proto.count(gene) > 1]

            proto_gene_count = {gene: proto.count(gene) for gene in proto}

            for i in range(len(proto)):
                if proto_gene_count[proto[i]] > 1:
                    proto_gene_count[proto[i]] -= 1
                    if missing_genes:
                        proto[i] = missing_genes.pop(0)
                        proto_gene_count[proto[i]] = proto_gene_count.get(proto[i], 0) + 1

            return proto

        final_offspring1 = legalize(proto_offspring1, parent1.seq)
        final_offspring2 = legalize(proto_offspring2, parent2.seq)

        return Individual(config=parent1.config, seq=final_offspring1, op_data=parent1.op_data), Individual(config=parent2.config, seq=final_offspring2, op_data=parent2.op_data)

