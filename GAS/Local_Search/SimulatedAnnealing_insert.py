import copy
import math
import random

class SimulatedAnnealing_insert:
    def __init__(self, initial_temp=1000, cooling_rate=0.95, min_temp=1, min_insert_ratio=0.05, max_insert_ratio=0.5):
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp
        self.min_insert_ratio = min_insert_ratio  # 최소 삽입 비율
        self.max_insert_ratio = max_insert_ratio  # 최대 삽입 비율
        self.stop_search = False

    def optimize(self, individual, config):
        best_solution = copy.deepcopy(individual)
        current_solution = copy.deepcopy(individual)
        best_makespan = best_solution.makespan
        current_makespan = current_solution.makespan
        temp = self.initial_temp
        iteration = 0

        # Run_Config의 simulated_annealing_iterations 사용
        iterations = config.simulated_annealing_iterations

        while temp > self.min_temp and iteration < iterations:
            neighbor = self.get_random_neighbor(current_solution, config)  # config 추가
            neighbor_makespan = neighbor.makespan

            if neighbor_makespan < best_makespan:
                best_solution = copy.deepcopy(neighbor)
                best_makespan = neighbor_makespan

            if neighbor_makespan < current_makespan or \
                    math.exp((current_makespan - neighbor_makespan) / temp) > random.random():
                current_solution = copy.deepcopy(neighbor)
                current_makespan = neighbor_makespan

            temp *= self.cooling_rate
            iteration += 1

            if best_solution.fitness >= 1.0:
                print(f"Stopping early as fitness {best_solution.fitness} is 1.0 or higher.")
                self.stop_search = True
                break

        return best_solution

    def get_random_neighbor(self, individual, config):  # config 매개변수 추가
        new_seq = copy.deepcopy(individual.seq)
        size = len(new_seq)

        # 염색체 길이에 대한 상대적 비율로 삽입 횟수 결정
        min_inserts = max(1, int(size * self.min_insert_ratio))
        max_inserts = min(size, int(size * self.max_insert_ratio))
        num_inserts = random.randint(min_inserts, max_inserts)

        for _ in range(num_inserts):
            i, j = random.sample(range(size), 2)
            job = new_seq.pop(i)
            new_seq.insert(j, job)
        
        neighbor = self.create_new_individual(individual, new_seq, config)  # config 전달
        return neighbor

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
