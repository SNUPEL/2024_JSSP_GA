"""
SelectiveMutation Class

This script defines the SelectiveMutation class, which implements a selective 
mutation method for genetic algorithms. The selective mutation method applies 
different mutation probabilities to different segments of the population based 
on their fitness.

Classes:
    SelectiveMutation: A class to perform selective mutation on a population.

Functions:
    mutate(population, config): Performs the selective mutation operation on a population.
    apply_mutation(individual, config, lower_bits): Applies inversion mutation to a segment of the individual's sequence.
"""

import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GAS.Mutation.base import Mutation
from GAS.Individual import Individual

class SelectiveMutation(Mutation):
    """
    Implements a selective mutation method for genetic algorithms.
    
    Attributes:
        pm_high (float): The high probability of mutation.
        pm_low (float): The low probability of mutation.
        rank_divide (float): The proportion of the population considered "good."
    """
    
    def __init__(self, pm_high, pm_low, rank_divide):
        """
        Initializes the SelectiveMutation class with the specified parameters.
        
        Parameters:
            pm_high (float): The high probability of mutation.
            pm_low (float): The low probability of mutation.
            rank_divide (float): The proportion of the population considered "good."
        """
        self.pm_high = pm_high  # 높은 돌연변이 확률
        self.pm_low = pm_low    # 낮은 돌연변이 확률
        self.rank_divide = rank_divide

    def mutate(self, population, config):
        """
        Performs the selective mutation operation on a population.
        
        Parameters:
            population (list): The population to mutate.
            config: Configuration object with simulation settings.
        """
        # 적합도에 따라 개체군을 랭킹합니다.
        ranked_population = sorted(population, key=lambda ind: ind.fitness, reverse=True)
        divide_index = int(len(ranked_population) * self.rank_divide)
        
        # 랭크에 따라 좋은 그룹과 나쁜 그룹으로 나눕니다.
        good_group = ranked_population[:divide_index]
        bad_group = ranked_population[divide_index:]

        for ind in good_group:
            if random.random() < self.pm_low:
                self.apply_mutation(ind, config, lower_bits=True)
        
        for ind in bad_group:
            if random.random() < self.pm_high:
                self.apply_mutation(ind, config, lower_bits=False)

    def apply_mutation(self, individual, config, lower_bits):
        """
        Applies inversion mutation to a segment of the individual's sequence.
        
        Parameters:
            individual (Individual): The individual to mutate.
            config: Configuration object with simulation settings.
            lower_bits (bool): Whether to apply mutation to the lower half of the sequence.
        
        Returns:
            Individual: The mutated individual.
        """
        seq = individual.seq[:]
        if lower_bits:
            # 염색체의 하위 부분에 돌연변이를 적용합니다.
            start, end = sorted(random.sample(range(len(seq)//2), 2))
        else:
            # 염색체의 상위 부분에 돌연변이를 적용합니다.
            start, end = sorted(random.sample(range(len(seq)//2, len(seq)), 2))

        # 역위 돌연변이를 수행합니다.
        seq[start:end] = seq[start:end][::-1]
        individual.seq = seq
        individual.calculate_fitness(config.target_makespan)
        
        return individual
