"""
SimulatedAnnealing Class

This script defines the SimulatedAnnealing class, which implements the simulated 
annealing algorithm for local search optimization in genetic algorithms. The class 
iteratively improves the job sequence by exploring neighboring solutions and 
accepting them based on a probabilistic criterion.

Classes:
    SimulatedAnnealing: A class to perform simulated annealing local search optimization.

Functions:
    optimize(individual, config): Optimizes the job sequence using simulated annealing.
    get_random_neighbor(individual, config): Generates a random neighboring solution.
    ensure_valid_sequence(seq, config): Ensures that the job sequence is valid.
    create_new_individual(individual, new_seq, config): Creates a new individual with the optimized sequence.
"""

import copy
import math
import random

class SimulatedAnnealing:
    """
    Implements the simulated annealing algorithm for local search optimization.
    
    Attributes:
        initial_temp (float): The initial temperature for the annealing process.
        cooling_rate (float): The rate at which the temperature decreases.
        min_temp (float): The minimum temperature for the annealing process.
        iterations (int): The number of iterations to perform.
        stop_search (bool): Flag to indicate when to stop the search.
    """
    
    def __init__(self, initial_temp=1000, cooling_rate=0.95, min_temp=1, iterations=10):
        """
        Initializes the SimulatedAnnealing class with the specified parameters.
        
        Parameters:
            initial_temp (float): The initial temperature (default is 1000).
            cooling_rate (float): The cooling rate (default is 0.95).
            min_temp (float): The minimum temperature (default is 1).
            iterations (int): The number of iterations (default is 10).
        """
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp
        self.iterations = iterations
        self.stop_search = False  # 종료 조건 플래그 추가

    def optimize(self, individual, config):
        """
        Optimizes the job sequence using simulated annealing.
        
        Parameters:
            individual (Individual): The individual to optimize.
            config: Configuration object with simulation settings.
        
        Returns:
            Individual: The optimized individual.
        """
        best_solution = copy.deepcopy(individual)
        current_solution = copy.deepcopy(individual)
        best_makespan = individual.makespan
        current_makespan = individual.makespan
        temp = self.initial_temp
        iteration = 0

        while temp > self.min_temp and iteration < self.iterations:
            neighbor = self.get_random_neighbor(current_solution, config)
            neighbor_makespan = neighbor.makespan

            if neighbor_makespan < best_makespan:
                best_solution = copy.deepcopy(neighbor)
                best_makespan = neighbor_makespan

            if neighbor_makespan < current_makespan or \
                    math.exp((current_makespan - neighbor_makespan) / temp) > random.random():
                current_solution = neighbor
                current_makespan = neighbor_makespan

            temp *= self.cooling_rate
            iteration += 1

            # 목표 Makespan에 도달하면 Local Search 종료
            if best_solution.fitness >= 1.0:
                print(f"Stopping early as fitness {best_solution.fitness} is 1.0 or higher.")
                self.stop_search = True
                break

        return best_solution

    def get_random_neighbor(self, individual, config):
        """
        Generates a random neighboring solution by swapping two jobs.
        
        Parameters:
            individual (Individual): The individual to generate a neighbor for.
            config: Configuration object with simulation settings.
        
        Returns:
            Individual: A neighboring individual.
        """
        new_seq = copy.deepcopy(individual.seq)
        i, j = random.sample(range(len(new_seq)), 2)
        new_seq[i], new_seq[j] = new_seq[j], new_seq[i]
        new_seq = self.ensure_valid_sequence(new_seq, config)
        
        # Create a new individual and recompute makespan and fitness
        neighbor = self.create_new_individual(individual, new_seq, config)
        neighbor.calculate_fitness(neighbor.config.target_makespan)
        return neighbor

    def ensure_valid_sequence(self, seq, config):
        """
        Ensures that the job sequence is valid.
        
        Parameters:
            seq (list): The job sequence.
            config: Configuration object with simulation settings.
        
        Returns:
            list: The valid job sequence.
        """
        num_jobs = config.n_job
        num_machines = config.n_machine
        job_counts = {job: 0 for job in range(num_jobs)}
        valid_seq = []

        for operation in seq:
            job = operation // num_machines
            if job_counts[job] < num_machines:
                valid_seq.append(job * num_machines + job_counts[job])
                job_counts[job] += 1

        for job in range(num_jobs):
            while job_counts[job] < num_machines:
                valid_seq.append(job * num_machines + job_counts[job])
                job_counts[job] += 1

        return valid_seq

    def create_new_individual(self, individual, new_seq, config):
        """
        Creates a new individual with the optimized sequence.
        
        Parameters:
            individual (Individual): The original individual.
            new_seq (list): The optimized job sequence.
            config: Configuration object with simulation settings.
        
        Returns:
            Individual: The new individual with the optimized sequence.
        """
        new_individual = copy.deepcopy(individual)
        new_individual.seq = new_seq
        new_individual.job_seq = new_individual.get_repeatable()
        new_individual.feasible_seq = new_individual.get_feasible()
        new_individual.machine_order = new_individual.get_machine_order()
        new_individual.makespan, new_individual.mio_score = new_individual.evaluate(new_individual.machine_order)
        return new_individual
