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
            self.max_swaps = 40

        best_solution_seq = individual.seq[:]
        best_makespan = individual.makespan
        no_improvement_count = 0
        
        # best_job_seq, best_feasible_seq, best_machine_order 초기화
        best_job_seq = individual.job_seq  # 초기값 설정
        best_feasible_seq = individual.feasible_seq  # 초기값 설정
        best_machine_order = individual.machine_order  # 초기값 설정
        
        size = len(individual.seq)
        num_jobs = individual.config.n_job  # Job 수 가져오기
        
        # 각 Operation이 어느 Job에 속하는지 계산 (index에 해당하는 Job 번호)
        job_indices = [i // individual.config.n_machine for i in range(size)]
        
        for iteration in range(self.iterations):
            improved = False
            used_i = set()
            swaps = 0
            if no_improvement_count == 0:
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

                        new_seq = self.swap(best_solution_seq, i, j)
                        # 기존 개체의 seq만 변경하고, 새로운 개체를 생성하지 않음
                        individual.seq = new_seq
                        individual.job_seq = individual.get_repeatable()
                        individual.feasible_seq = individual.get_feasible()
                        individual.machine_order = individual.get_machine_order()
                        new_makespan, _ = individual.evaluate(individual.machine_order)

                        if new_makespan == best_makespan:
                            best_solution_seq[:] = new_seq
                            best_makespan = new_makespan
                            best_job_seq = individual.job_seq  # job_seq도 업데이트
                            best_feasible_seq = individual.feasible_seq  # feasible_seq도 업데이트
                            best_machine_order = individual.machine_order  # machine_order도 업데이트

                        if new_makespan < best_makespan:
                            best_solution_seq[:] = new_seq
                            best_makespan = new_makespan
                            best_job_seq = individual.job_seq  # job_seq도 업데이트
                            best_feasible_seq = individual.feasible_seq  # feasible_seq도 업데이트
                            best_machine_order = individual.machine_order  # machine_order도 업데이트
                            improved = True
                            print(f"    >> Improvement found! New Best Makespan: {best_makespan}")
                            break
                    swaps += 1
                    
                if improved:
                    no_improvement_count = 0
                else:
                    no_improvement_count += 1

            elif no_improvement_count == 1:

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

                        new_seq = self.two_opt_swap(best_solution_seq, i, j)
                        # 기존 개체의 seq만 변경하고, 새로운 개체를 생성하지 않음
                        individual.seq = new_seq
                        individual.job_seq = individual.get_repeatable()
                        individual.feasible_seq = individual.get_feasible()
                        individual.machine_order = individual.get_machine_order()
                        new_makespan, _ = individual.evaluate(individual.machine_order)

                        if new_makespan == best_makespan:
                            best_solution_seq[:] = new_seq
                            best_makespan = new_makespan
                            best_job_seq = individual.job_seq  # job_seq도 업데이트
                            best_feasible_seq = individual.feasible_seq  # feasible_seq도 업데이트
                            best_machine_order = individual.machine_order  # machine_order도 업데이트

                        if new_makespan < best_makespan:
                            best_solution_seq[:] = new_seq
                            best_makespan = new_makespan
                            best_job_seq = individual.job_seq  # job_seq도 업데이트
                            best_feasible_seq = individual.feasible_seq  # feasible_seq도 업데이트
                            best_machine_order = individual.machine_order  # machine_order도 업데이트
                            improved = True
                            print(f"    >> Improvement found! New Best Makespan: {best_makespan}")
                            break  # 개선이 있으면 해당 Iteration 종료

                    swaps += 1                 

                if improved:
                    no_improvement_count = 0
                else:
                    no_improvement_count += 1
            else:
                print(f"Iteration {iteration+1}/{self.iterations} - Best Makespan: {best_makespan}")
                break
        
        # 최종적으로 best_solution_seq로 individual 업데이트 (machine_order 포함)
        individual.seq = best_solution_seq
        individual.makespan = best_makespan
        individual.job_seq = best_job_seq  # job_seq 업데이트
        individual.feasible_seq = best_feasible_seq  # feasible_seq 업데이트
        individual.machine_order = best_machine_order  # machine_order 업데이트
        
        return individual

    def two_opt_swap(self, seq, i, j):
        new_seq = seq[:]        
        # i와 j가 겹치지 않도록 조정
        if i < j:
            new_seq = seq[:i] + seq[i+2:j+1] + seq[i:i+2] + seq[j+1:]
        else:
            new_seq = seq[:j+1] + seq[i:i+2] + seq[j+1:i] + seq[i+2:]
        return new_seq

    def swap(self, seq, i, j):
        """ 두 개의 인덱스 i와 j에서 작업을 교환합니다. """
        new_seq = seq[:]
        new_seq[i], new_seq[j] = new_seq[j], new_seq[i]
        return new_seq