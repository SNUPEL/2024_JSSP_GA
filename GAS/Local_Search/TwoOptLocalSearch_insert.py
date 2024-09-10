import random
import copy

class TwoOptLocalSearch_insert:
    def __init__(self, iterations=None, max_swaps=None):
        self.iterations = iterations
        self.max_swaps = max_swaps

    def optimize(self, individual, config):
        if self.iterations is None:
            self.iterations = config.two_iterations
        if self.max_swaps is None:
            self.max_swaps = len(individual.seq) * (len(individual.seq) - 1) / 10

        best_solution = copy.deepcopy(individual)
        best_makespan = best_solution.makespan
        no_improvement_count = 0  # 개선되지 않은 연속 횟수 추적 

        for iteration in range(self.iterations):
            improved = False
            swaps = 0

            while swaps < self.max_swaps:
                # i는 0부터 len(individual.seq) - 1 사이에서 랜덤 선택
                i = random.randint(0, len(individual.seq) - 1)

                # j는 i와 같지 않은 값으로 선택
                j = random.randint(0, len(individual.seq) - 1)
                while j == i:
                    j = random.randint(0, len(individual.seq) - 1)

                new_seq = self.insertion(best_solution.seq, i, j)
                # print(f"After insert between {i} and {j}: {new_seq}")
                # new_solution = self.create_new_individual(individual, new_seq)

                new_solution = self.create_new_individual(individual, copy.deepcopy(new_seq), config)
                new_makespan = new_solution.makespan
                # <=로 바꿈
                if new_makespan == best_makespan:
                    best_solution = copy.deepcopy(new_solution)
                    best_makespan = new_makespan
                    # print(f"Improvement found: Makespan {best_makespan}")
                
                if new_makespan < best_makespan:
                    best_solution = copy.deepcopy(new_solution)
                    best_makespan = new_makespan
                    improved = True
                    # print(f"Improvement found: Makespan {best_makespan}")                
                swaps += 1

            if improved:
                no_improvement_count = 0  # 개선이 있으면 카운트 리셋
            else:
                no_improvement_count += 1  # 개선이 없으면 카운트 증가

            # 3번 연속으로 개선이 없으면 중단
            if no_improvement_count >= 1:
                # print(f"No improvement in the last 1 iterations. Stopping early at iteration {iteration + 1}.")
                break

            # Debugging output
            print(f"Iteration {iteration+1}/{self.iterations} - Best Makespan: {best_makespan}")
            # print(f"Best sequence: {best_solution.seq}")
                    
        return best_solution


    def insertion(self, seq, i, j):
        """
        작업을 seq[i]에서 seq[j]로 삽입하는 함수.
        """
        new_seq = seq[:]
        job = new_seq.pop(i)
        new_seq.insert(j, job)
        return new_seq

    def create_new_individual(self, individual, new_seq, config):
        new_individual = copy.deepcopy(individual)
        new_individual.seq = new_seq
        new_individual.job_seq = new_individual.get_repeatable()
        new_individual.feasible_seq = new_individual.get_feasible()
        new_individual.machine_order = new_individual.get_machine_order()
        new_individual.makespan, new_individual.mio_score = new_individual.evaluate(new_individual.machine_order)
        return new_individual
