"""
TabuSearch Class

This script defines the TabuSearch class, which implements the tabu search 
algorithm for local search optimization in genetic algorithms. The class 
iteratively explores neighboring solutions while maintaining a list of tabu 
moves to avoid cycling.

Classes:
    TabuSearch: A class to perform tabu search local search optimization.

Functions:
    optimize(individual, config): Optimizes the job sequence using tabu search.
    get_neighbors(individual, config): Generates neighboring solutions by swapping jobs.
    create_new_individual(individual, new_seq, config): Creates a new individual with the optimized sequence.
    ensure_valid_sequence(seq, config): Ensures that the job sequence is valid.
"""

import copy
from collections import deque
import random

class TabuSearch:
    """
    Implements the tabu search algorithm for local search optimization.
    
    Attributes:
        tabu_tenure (int): The number of iterations a move remains tabu.
        iterations (int): The number of iterations to perform.
        max_neighbors (int): The maximum number of neighbors to consider.
        stop_search (bool): Flag to indicate when to stop the search.
    """
    
    def __init__(self, tabu_tenure=5, iterations=10, max_neighbors=10):
        """
        Initializes the TabuSearch class with the specified parameters.
        
        Parameters:
            tabu_tenure (int): The number of iterations a move remains tabu (default is 5).
            iterations (int): The number of iterations to perform (default is 10).
            max_neighbors (int): The maximum number of neighbors to consider (default is 10).
        """
        self.tabu_tenure = tabu_tenure
        self.iterations = iterations
        self.max_neighbors = max_neighbors  # 최대 이웃 개수를 추가
        self.stop_search = False  # 종료 조건 플래그 추가

    def optimize(self, individual, config):
        """
        Optimizes the job sequence using tabu search.
        
        Parameters:
            individual (Individual): The individual to optimize.
            config: Configuration object with simulation settings.
        
        Returns:
            Individual: The optimized individual.
        """
        best_solution = copy.deepcopy(individual)
        best_makespan = individual.makespan
        tabu_list = []
        tabu_list.append(copy.deepcopy(individual.seq))

        for iteration in range(self.iterations):
            neighbors = self.get_neighbors(individual, config)
            neighbors = [n for n in neighbors if n.seq not in tabu_list]

            if not neighbors:
                break

            current_solution = min(neighbors, key=lambda ind: ind.makespan)
            current_makespan = current_solution.makespan

            if current_makespan < best_makespan:
                best_solution = copy.deepcopy(current_solution)
                best_makespan = current_makespan

            tabu_list.append(copy.deepcopy(current_solution.seq))
            if len(tabu_list) > self.tabu_tenure:
                tabu_list.pop(0)

            # 목표 Makespan에 도달하면 Local Search 종료
            if best_solution.fitness >= 1.0:
                print(f"Stopping early as fitness {best_solution.fitness} is 1.0 or higher.")
                self.stop_search = True
                return best_solution

        return best_solution

    def get_neighbors(self, individual, config):
        """
        Generates neighboring solutions by swapping jobs.
        
        Parameters:
            individual (Individual): The individual to generate neighbors for.
            config: Configuration object with simulation settings.
        
        Returns:
            list: A list of neighboring individuals.
        """
        neighbors = []
        seq = individual.seq
        for i in range(len(seq) - 1):
            for j in range(i + 1, len(seq)):
                if len(neighbors) >= self.max_neighbors:  # 최대 이웃 개수 조건 추가
                    return neighbors
                neighbor_seq = seq[:]
                neighbor_seq[i], neighbor_seq[j] = neighbor_seq[j], neighbor_seq[i]
                neighbor = self.create_new_individual(individual, neighbor_seq, config)
                neighbors.append(neighbor)
        return neighbors

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
        new_individual.calculate_fitness(config.target_makespan)
        return new_individual

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
