"""
HillClimbing Class

This script defines the HillClimbing class, which implements the hill climbing 
algorithm for local search optimization in genetic algorithms. The class iteratively 
improves the job sequence to minimize the makespan and improve the fitness of the individual.

Classes:
    HillClimbing: A class to perform hill climbing local search optimization.

Functions:
    optimize(individual, config): Optimizes the job sequence using hill climbing.
    get_neighbors(individual, config): Generates neighboring solutions by swapping jobs.
    create_new_individual(individual, new_seq, config): Creates a new individual with the optimized sequence.
    ensure_valid_sequence(seq, config): Ensures that the job sequence is valid.
"""

import copy

class HillClimbing:
    """
    Implements the hill climbing algorithm for local search optimization.
    
    Attributes:
        iterations (int): The number of iterations to perform.
        stop_search (bool): Flag to indicate when to stop the search.
    """
    
    def __init__(self, iterations=30):
        """
        Initializes the HillClimbing class with the specified number of iterations.
        
        Parameters:
            iterations (int): The number of iterations to perform (default is 30).
        """
        self.iterations = iterations
        self.stop_search = False

    def optimize(self, individual, config):
        """
        Optimizes the job sequence using hill climbing.
        
        Parameters:
            individual (Individual): The individual to optimize.
            config: Configuration object with simulation settings.
        
        Returns:
            Individual: The optimized individual.
        """
        print(f"HillClimbing 시작 - Initial Individual: {individual.seq}, Makespan: {individual.makespan}, Fitness: {individual.fitness}")        
        best_solution = copy.deepcopy(individual)
        best_makespan = individual.makespan
        iteration = 0

        while iteration < self.iterations:
            neighbors = self.get_neighbors(best_solution, config)
            current_solution = min(neighbors, key=lambda ind: ind.makespan)
            current_makespan = current_solution.makespan

            if current_makespan >= best_makespan:
                break

            best_solution = current_solution
            best_makespan = current_makespan
            iteration += 1
            print(f"Iteration {iteration} - Current Solution: {current_solution.seq}, Makespan: {current_makespan}, Fitness: {current_solution.fitness}")

            # 목표 Makespan에 도달하면 Local Search 종료
            if best_solution.fitness >= 1.0:
                print(f"Stopping early as fitness {best_solution.fitness} is 1.0 or higher.")
                self.stop_search = True
                return best_solution

        print(f"HillClimbing 완료 - Optimized Individual: {best_solution.seq}, Makespan: {best_solution.makespan}, Fitness: {best_solution.fitness}")
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
