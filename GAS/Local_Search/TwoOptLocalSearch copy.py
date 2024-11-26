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
        best_job_seq = individual.job_seq  # 추가
        best_feasible_seq = individual.feasible_seq  # 추가
        best_machine_order = individual.machine_order  # 추가
        no_improvement_count = 0

        size = len(individual.seq)
        num_jobs = individual.config.n_job  # Job 수 가져오기

        # 각 Operation이 어느 Job에 속하는지 계산 (index에 해당하는 Job 번호)
        job_indices = [i // individual.config.n_machine for i in range(size)]

        for iteration in range(self.iterations):
            improved = False
            used_i = set()
            swaps = 0
            print(f"\nIteration {iteration + 1}/{self.iterations} - Current Best Makespan: {best_makespan}")

            if no_improvement_count == 0:
                while swaps < self.max_swaps:
                    available_i = [x for x in range(size - 1) if x not in used_i]
                    if not available_i:
                        print(f" - No more available i, breaking.")
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

                        print(f"  > Swap {swaps + 1}/{self.max_swaps}: Trying swap between i={i} (Job {job_indices[i]}) and j={j} (Job {job_indices[j]})")

                        new_seq = self.swap(best_solution_seq, i, j)

                        # 기존 개체의 seq만 변경하고, 새로운 개체를 생성하지 않음
                        individual.seq = new_seq
                        individual.job_seq = individual.get_repeatable()
                        individual.feasible_seq = individual.get_feasible()
                        individual.machine_order = individual.get_machine_order()

                        # 새롭게 계산된 makespan 반영
                        new_makespan, _ = individual.evaluate(individual.machine_order)

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
                        if swaps >= self.max_swaps:
                            print(f" - Max swaps ({self.max_swaps}) reached. Exiting.")
                            break

                    if improved:
                        no_improvement_count = 0
                        print(f" - Improvement found, reset no_improvement_count.")
                        break
                    else:
                        no_improvement_count += 1

            elif no_improvement_count == 1:
                while swaps < self.max_swaps:
                    available_i = [x for x in range(size - 1) if x not in used_i]
                    if not available_i:
                        print(f" - No more available i, breaking.")
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

                        print(f"  > Swap {swaps + 1}/{self.max_swaps}: Trying swap between i={i} (Job {job_indices[i]}) and j={j} (Job {job_indices[j]})")

                        new_seq = self.insertion(best_solution_seq, i, j)

                        # 기존 개체의 seq만 변경하고, 새로운 개체를 생성하지 않음
                        individual.seq = new_seq
                        individual.job_seq = individual.get_repeatable()
                        individual.feasible_seq = individual.get_feasible()
                        individual.machine_order = individual.get_machine_order()

                        # 새롭게 계산된 makespan 반영
                        new_makespan, _ = individual.evaluate(individual.machine_order)

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
                        if swaps >= self.max_swaps:
                            print(f" - Max swaps ({self.max_swaps}) reached. Exiting.")
                            break

                    if improved:
                        no_improvement_count = 0
                        print(f" - Improvement found, reset no_improvement_count.")
                        break
                    else:
                        no_improvement_count += 1

            elif no_improvement_count == 2:
                while swaps < self.max_swaps:
                    available_i = [x for x in range(size - 1) if x not in used_i]
                    if not available_i:
                        print(f" - No more available i, breaking.")
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

                        print(f"  > Swap {swaps + 1}/{self.max_swaps}: Trying swap between i={i} (Job {job_indices[i]}) and j={j} (Job {job_indices[j]})")

                        new_seq = self.two_opt_swap(best_solution_seq, i, j)

                        # 기존 개체의 seq만 변경하고, 새로운 개체를 생성하지 않음
                        individual.seq = new_seq
                        individual.job_seq = individual.get_repeatable()
                        individual.feasible_seq = individual.get_feasible()
                        individual.machine_order = individual.get_machine_order()

                        # 새롭게 계산된 makespan 반영
                        new_makespan, _ = individual.evaluate(individual.machine_order)

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
                        if swaps >= self.max_swaps:
                            print(f" - Max swaps ({self.max_swaps}) reached. Exiting.")
                            break

                    if improved:
                        no_improvement_count = 0
                        print(f" - Improvement found, reset no_improvement_count.")
                        break
                    else:
                        no_improvement_count += 1
                        
            else:
                print(f'종료 no_improvement_count:{no_improvement_count}')
                break

            print(f"Iteration {iteration + 1} complete - Best Makespan: {best_makespan}")

        # 최종적으로 best_solution_seq로 individual 업데이트 (machine_order 포함)
        individual.seq = best_solution_seq
        individual.makespan = best_makespan
        individual.job_seq = best_job_seq  # job_seq 업데이트
        individual.feasible_seq = best_feasible_seq  # feasible_seq 업데이트
        individual.machine_order = best_machine_order  # machine_order 업데이트

        print(f"Final Best Makespan: {best_makespan}\n")
        return individual

    def insertion(self, seq, i, j):
        new_seq = seq[:]
        job = new_seq.pop(i)
        new_seq.insert(j, job)
        return new_seq
    
    def two_opt(self, seq, i, j):
        """
        인덱스 i와 j를 선택하고, i와 j 사이의 부분(seq[i+1]부터 seq[j-1]까지)을 역순으로 뒤집습니다.
        i와 j는 그대로 두고, 사이의 부분만 반전합니다.
        """
        if i > j:
            i, j = j, i  # i와 j가 잘못된 경우 교환

        # 인덱스 범위 확인 (i와 j가 유효한 인덱스인지 검사)
        if i < 0 or j >= len(seq) or j - i < 2:
            # i와 j 사이에 최소한 하나의 요소가 있어야 함
            return seq[:]  # 원본 시퀀스를 그대로 반환

        # i+1부터 j-1까지의 부분을 반전
        middle_section = seq[i+1:j]
        reversed_middle = middle_section[::-1]

        # 새로운 시퀀스 생성
        new_seq = seq[:i+1] + reversed_middle + seq[j:]
        return new_seq
    
    def swap(self, seq, i, j):
        """ 두 개의 인덱스 i와 j에서 작업을 교환합니다. """
        new_seq = seq[:]
        new_seq[i], new_seq[j] = new_seq[j], new_seq[i]
        return new_seq

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