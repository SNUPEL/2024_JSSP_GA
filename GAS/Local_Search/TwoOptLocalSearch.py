import copy
import random

class TwoOptLocalSearch:
    def __init__(self, iterations=None, max_swaps=None):
        self.iterations = iterations
        self.max_swaps = max_swaps

    def optimize(self, individual, config):
        if self.iterations is None:
            self.iterations = config.two_iterations
        if self.max_swaps is None:
            self.max_swaps = (len(individual.seq) * (len(individual.seq) - 1) / 1)

        best_solution = copy.deepcopy(individual)
        best_makespan = best_solution.makespan
        no_improvement_count = 0
        
        size = len(individual.seq)
        num_jobs = individual.config.n_job  # Job 수 가져오기
        
        # 각 Operation이 어느 Job에 속하는지 계산 (index에 해당하는 Job 번호)
        job_indices = [i // individual.config.n_machine for i in range(size)]
        
        for iteration in range(self.iterations):
            improved = False
            used_i = set()
            swaps = 0

            while swaps < self.max_swaps:
                available_i = [x for x in range(size - 1) if x not in used_i]
                if not available_i:
                    break

                i = random.choice(available_i)
                used_i.add(i)

                used_j = set()
                while len(used_j) < (size - (i + 1)):
                    available_j = [x for x in range(i + 1, size) if x not in used_j and job_indices[x] != job_indices[i]]
                    if not available_j:
                        break
                    
                    j = random.choice(available_j)
                    used_j.add(j)

                    new_seq = self.two_opt_swap(best_solution.seq, i, j)
                    new_solution = self.create_new_individual(individual, copy.deepcopy(new_seq), config)
                    new_makespan = new_solution.makespan

                    if new_makespan == best_makespan:
                        best_solution = copy.deepcopy(new_solution)
                        best_makespan = new_makespan

                    if new_makespan < best_makespan:
                        best_solution = copy.deepcopy(new_solution)
                        best_makespan = new_makespan
                        improved = True
                        print(f"Improvement found: Makespan {best_makespan}")
                swaps += 1

            if improved:
                no_improvement_count = 0
            else:
                no_improvement_count += 1

            if no_improvement_count >= 2:
                break

            print(f"Iteration {iteration+1}/{self.iterations} - Best Makespan: {best_makespan}")
        
        return best_solution

    def two_opt_swap(self, seq, i, j):
        new_seq = copy.deepcopy(seq[:i] + seq[i:j+1][::-1] + seq[j+1:])
        return new_seq

    def create_new_individual(self, individual, new_seq, config):
        new_individual = copy.deepcopy(individual)
        new_individual.seq = new_seq
        new_individual.job_seq = new_individual.get_repeatable()
        new_individual.feasible_seq = new_individual.get_feasible()
        new_individual.machine_order = new_individual.get_machine_order()
        new_individual.makespan, new_individual.mio_score = new_individual.evaluate(new_individual.machine_order)
        return new_individual
