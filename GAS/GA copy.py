"""
GAEngine Class

This script defines the GAEngine class, which implements a genetic algorithm (GA) engine 
for job shop scheduling. The engine includes functionalities for crossover, mutation, 
selection, local search, and parallel execution.

Functions:
    migrate_top_10_percent(ga_engines, migration_order, island_mode): Migrates top 10 percent of individuals between GA engines.
    GAEngine.__init__(self, config, op_data, crossover, mutation, selection, ...): Initializes the GA engine with the given parameters.
    GAEngine.evolve(self, index, sync_generation, sync_lock, events=None): Evolves the population for a number of generations.
    GAEngine.apply_local_search(self, individual): Applies local search optimization to an individual.
    GAEngine.apply_pso(self, individual): Applies PSO optimization to an individual.
    GAEngine.save_csv(self, all_generations, execution_time, file_path): Saves the GA generations data to a CSV file.
"""

import sys
import os
import random
import time
import copy
import csv
from concurrent.futures import ProcessPoolExecutor

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GAS.Population import Population
from Local_Search.TabuSearch import TabuSearch
from Data.Dataset.Dataset import Dataset
from Meta.PSO import PSO
from GAS.Mutation.SelectiveMutation import SelectiveMutation
from Local_Search.HillClimbing import HillClimbing
from Local_Search.SimulatedAnnealing import SimulatedAnnealing
from Local_Search.GifflerThompson_LS import GifflerThompson_LS
from multiprocessing import Pool, Manager, Event, Value, Array, Event
import datetime
# from Meta.ORtools import ORToolsOptimizer

def migrate_top_10_percent(ga_engines, migration_order, island_mode):
    """
    Migrates top 10 percent of individuals between GA engines.
    
    Parameters:
        ga_engines (list): List of GA engines.
        migration_order (list): Order of migration between GA engines.
        island_mode (int): Mode of migration (e.g., sequential or random).
    """
    num_islands = len(ga_engines)
    for source_island_idx in range(num_islands):
        target_island_idx = migration_order[source_island_idx]

        source_island = ga_engines[source_island_idx]
        target_island = ga_engines[target_island_idx]

        for individual in source_island.new_populations:
            target_island.population.individuals[random.randint(0, len(target_island.population.individuals) - 1)] = copy.deepcopy(individual)
            print(f"Migrating from GA{source_island_idx + 1} to GA{target_island_idx + 1}")
def get_next_filename(base_name):
    index = 1
    while os.path.exists(f"{base_name}_{index}.csv"):
        index += 1
    return f"{base_name}_{index}.csv"

def save_population_to_csv(population, filename, generation):
    with open(filename, 'a', newline='') as csvfile:  # 'a' 모드를 사용하여 기존 파일에 데이터를 추가
        writer = csv.writer(csvfile)
        
        # 첫 번째 세대일 경우, 헤더를 작성합니다.
        if generation == 0 and csvfile.tell() == 0:
            writer.writerow(['Generation', 'Index', 'Sequence', 'Makespan'])
        
        start_index = generation * len(population.individuals) + 1  # 각 세대별 시작 인덱스를 계산합니다.
        
        for i, individual in enumerate(population.individuals):
            seq_str = ','.join(map(str, individual.seq))
            writer.writerow([generation + 1, start_index + i, seq_str, individual.makespan])
class GAEngine:
    """
    Implements a genetic algorithm (GA) engine for job shop scheduling.
    
    Attributes:
        config: Configuration object for the GA engine.
        op_data: Operation data for the job shop.
        crossover: Crossover operator for the GA.
        mutation: Mutation operator for the GA.
        selection: Selection operator for the GA.
        local_search: Local search methods for the GA.
        pso: PSO optimizer for the GA.
        selective_mutation: Selective mutation operator for the GA.
        elite_ratio (float): Proportion of elites in the population.
        best_time: Best execution time recorded.
        ga_engines: List of GA engines for island model.
        island_mode (int): Mode of migration between islands.
        migration_frequency (int): Frequency of migration between islands.
        dataset_filename (str): Filename of the dataset.
        local_search_frequency (int): Frequency of local search application.
        selective_mutation_frequency (int): Frequency of selective mutation application.
        random_seed (int): Seed for random number generation.
        local_search_top_percentage (float): Top percentage of individuals for local search.
        population (Population): Population of individuals in the GA.
    """
    
    def __init__(self, config, op_data, crossover, mutation, selection, local_search=None, pso=None, selective_mutation=None, elite_ratio=0.1, ga_engines=None, island_mode=1, migration_frequency=10, initialization_mode='1', dataset_filename=None, initial_population=None, local_search_frequency=2, selective_mutation_frequency=10, random_seed=None):
        """
        Initializes the GA engine with the given parameters.
        
        Parameters:
            config: Configuration object for the GA engine.
            op_data: Operation data for the job shop.
            crossover: Crossover operator for the GA.
            mutation: Mutation operator for the GA.
            selection: Selection operator for the GA.
            local_search (list): List of local search methods for the GA (default is None).
            pso (PSO): PSO optimizer for the GA (default is None).
            selective_mutation (SelectiveMutation): Selective mutation operator for the GA (default is None).
            elite_ratio (float): Proportion of elites in the population (default is 0.1).
            ga_engines (list): List of GA engines for island model (default is None).
            island_mode (int): Mode of migration between islands (default is 1).
            migration_frequency (int): Frequency of migration between islands (default is 10).
            initialization_mode (str): Mode of population initialization (default is '1').
            dataset_filename (str): Filename of the dataset (default is None).
            initial_population (Population): Initial population of individuals (default is None).
            local_search_frequency (int): Frequency of local search application (default is 2).
            selective_mutation_frequency (int): Frequency of selective mutation application (default is 10).
            random_seed (int): Seed for random number generation (default is None).
        """
        self.config = config
        self.op_data = op_data
        self.crossover = crossover
        self.mutation = mutation
        self.selection = selection
        self.local_search = local_search
        self.local_search_methods = local_search if local_search else []
        self.pso = pso
        self.selective_mutation = selective_mutation
        self.elite_ratio = elite_ratio
        self.best_time = None
        self.ga_engines = ga_engines
        self.island_mode = island_mode
        self.migration_frequency = migration_frequency
        self.dataset_filename = dataset_filename
        self.local_search_frequency = local_search_frequency
        self.selective_mutation_frequency = selective_mutation_frequency
        self.random_seed = random_seed
        self.local_search_top_percentage = 0.01  

        if initialization_mode == '2':
            self.population = Population.from_mio(config, op_data, dataset_filename, random_seed=random_seed)
        elif initialization_mode == '3':
            self.population = Population.from_giffler_thompson(config, op_data, dataset_filename, random_seed=random_seed)
        else:
            self.population = Population(config, op_data, random_seed=random_seed)

    def update_new_populations(self, index, new_populations):
        # 현재 population에서 상위 10% 개체를 추출하여 new_populations에 저장
        top_individuals = sorted(self.population.individuals, key=lambda ind: ind.makespan)[:max(1, len(self.population.individuals) // 10)]
        new_populations[index] = [copy.deepcopy(ind) for ind in top_individuals]

        # 로그 출력: 상위 10% 개체 확인
        # print(f"GA{index+1} 세대의 상위 10% 개체: {[ind.seq for ind in new_populations[index]]}")

    def evolve(self, index, sync_generation, sync_lock, new_populations, events=None):
        try:
            all_generations = []
            start_time = time.time()
            best_individual = None
            best_fitness = float('inf')
            
            base_filename = f"population_generations_{index+1}"
            filename = get_next_filename(base_filename)  # 다음 사용 가능한 파일 이름을 가져옵니다.

            while sync_generation[index] < self.config.generations:
                # print(f"GA{index+1}_Evaluating generation {sync_generation[index]}")


                self.population.evaluate(self.config.target_makespan)
                print(f"GA{index+1} Population: {self.population is not None}")
                print(f"GA{index+1} Best Individual: {best_individual is not None}")


                best_individual = min(self.population.individuals, key=lambda ind: ind.makespan)
                best_fitness = best_individual.makespan
                print(f"GA{index+1}_Best fitness at generation select crossover mutate 전 {sync_generation[index]}: {best_fitness}")

                # 엘리트 개체 선택
                num_elites = int(self.elite_ratio * len(self.population.individuals))
                elites = copy.deepcopy(sorted(self.population.individuals, key=lambda ind: ind.makespan)[:num_elites])

                self.population.select(self.selection)

                self.population.crossover(self.crossover)

                self.population.mutate(self.mutation)

                # 전체 population 출력
                population_size = len(self.population.individuals)  # population의 갯수 계산
                print(f"GA{index+1} - 전체 population After crossover (Total Population: {population_size}):")

                # 엘리트 개체를 population에 다시 삽입
                for elite in elites:
                    # 현재 population에서 가장 성능이 떨어지는 개체를 찾음
                    worst_index = max(range(len(self.population.individuals)), key=lambda idx: self.population.individuals[idx].makespan)
                    # 엘리트 개체의 깊은 복사본을 생성하여 삽입
                    self.population.individuals[worst_index] = copy.deepcopy(elite)
                    print(f"Inserted elite at index {worst_index} - Makespan: {elite.makespan}, Fitness: {elite.fitness}")

                self.population.evaluate(self.config.target_makespan)
                # best_individual = min(self.population.individuals, key=lambda ind: ind.makespan)
                # best_fitness = best_individual.makespan
                 
                best_individual = min(self.population.individuals, key=lambda ind: ind.makespan)
                best_fitness = best_individual.makespan
                print(f"GA{index+1}_Best fitness at generation select crossover mutate 후 {sync_generation[index]}: {best_fitness}")

                # 상위 10% 개체를 new_populations에 저장
                self.update_new_populations(index, new_populations)
                # print(new_populations)

                if sync_generation[index] >= 1 and sync_generation[index] % self.local_search_frequency == 0:
                    print(f"GA{index+1}_Applying local search")
                    
                    total_percentage = self.local_search_top_percentage  # 예를 들어, 0.5이면 50%
                    top_percentage = 1 * total_percentage  # 상위 10%는 top_percentage에 해당

                    # 상위 10% 개체 추출 (가장 우수한 개체들)
                    top_count = int(len(self.population.individuals) * top_percentage)
                    top_indices_and_individuals = sorted(
                        enumerate(self.population.individuals),
                        key=lambda ind: ind[1].makespan
                    )[:top_count]

                    # 나머지 개체들 중에서 무작위로 나머지 40% 선택
                    remaining_count = int(len(self.population.individuals) * (total_percentage - top_percentage))
                    
                    remaining_indices_and_individuals = sorted(
                        enumerate(self.population.individuals),
                        key=lambda ind: ind[1].makespan
                    )[top_count:]  # 상위 10% 이후의 개체들

                    random_remaining = random.sample(remaining_indices_and_individuals, remaining_count)

                    top_individuals = [copy.deepcopy(individual) for idx, individual in top_indices_and_individuals]
                    top_indices = [idx for idx, individual in top_indices_and_individuals]

                    for method in self.local_search_methods:
                        for i in range(len(top_individuals)):
                            individual = top_individuals[i]  # 원래 개체 사용
                            optimized_ind = method.optimize(copy.deepcopy(individual), self.config)
                            
                            # Local Search 후 개체의 모든 속성 업데이트
                            optimized_ind.seq = optimized_ind.seq[:]  # 최종 seq 반영
                            optimized_ind.job_seq = optimized_ind.get_repeatable()  # job_seq 업데이트
                            optimized_ind.feasible_seq = optimized_ind.get_feasible()  # feasible_seq 업데이트
                            optimized_ind.machine_order = optimized_ind.get_machine_order()  # machine_order 재계산
                            optimized_ind.makespan, _ = optimized_ind.evaluate(optimized_ind.machine_order)  # makespan 재계산

                            # 비교를 통해 기존 개체보다 더 나은 경우에만 대체
                            if optimized_ind.makespan <= individual.makespan:
                                self.population.individuals[top_indices[i]] = optimized_ind
                                top_individuals[i] = optimized_ind  # top_individuals에서도 대체
                            else:
                                # 기존 개체 유지, 아무 작업도 하지 않음
                                pass



                best_individual = min(self.population.individuals, key=lambda ind: ind.makespan)
                best_fitness = best_individual.makespan
                print(f"GA{index+1}_Best fitness at generation Local Search 후 {sync_generation[index]}: {best_fitness}")

                # 이주가 가능한 경우
                if self.island_mode != 1 and sync_generation[index] % self.migration_frequency == 0 and sync_generation[index] != 0 and self.ga_engines:
                    # 이주 방식에 따른 순서 설정
                    if self.island_mode == 2:
                        # print(f"GA{index+1}_Migration 중 (순차) at generation {sync_generation[index]}")
                        migration_order = [(i + 1) % len(self.ga_engines) for i in range(len(self.ga_engines))]
                        print(f"Migration order: {migration_order}")
                    elif self.island_mode == 3:
                        # print(f"GA{index+1}_Migration 중 (랜덤) at generation {sync_generation[index]}")
                        migration_order = list(range(len(self.ga_engines)))
                        random.shuffle(migration_order)
                        print(f'랜덤 migration_order: {migration_order}')
                    else:
                        migration_order = range(len(self.ga_engines))
                    # print(f'최종 migration_order: {migration_order}')

                    # 각 GA 엔진 간 이주 수행
                    # 각 GA 엔진 간 이주 수행
                    for i in range(len(self.ga_engines)):
                        target_index = migration_order[i]

                        if target_index != i and sync_generation[i] % self.migration_frequency == 0:
                            print(f"GA{i+1} is migrating, receiving individuals from GA{target_index+1}")

                            if new_populations[target_index]:
                                best_index = min(range(len(self.ga_engines[i].population.individuals)), key=lambda idx: self.ga_engines[i].population.individuals[idx].makespan)
                                other_indices = [idx for idx in range(len(self.ga_engines[i].population.individuals)) if idx != best_index]

                                for j in range(len(new_populations[target_index])):
                                    random_index = random.choice(other_indices)
                                    other_indices.remove(random_index)

                                    # 개체 복사 (seq만 복사)
                                    migrated_individual = copy.deepcopy(new_populations[target_index][j])

                                    # machine_order는 이주 후 재계산
                                    migrated_individual.machine_order = migrated_individual.get_machine_order()
                                    

                                    # 마이그레이션 완료 후 상태 확인
                                    self.ga_engines[i].population.individuals[random_index] = migrated_individual

                                print(f"Migrating from GA{target_index+1} to GA{i+1} 완료")
                                
                                # 이주 후 population 평가
                                self.ga_engines[i].population.evaluate(self.config.target_makespan)


                            else:
                                print(f"new_populations[{target_index}] is empty, skipping migration.")

                self.population.evaluate(self.config.target_makespan)
                best_individual = min(self.population.individuals, key=lambda ind: ind.makespan)
                best_fitness = best_individual.makespan                
                print(f"GA{index+1}_Best fitness at generation 이주 후 {sync_generation[index]}: {best_fitness}")
                # print(f"{sync_generation[index]}: {best_fitness}, Sequence: {best_individual.seq}")

                generation_data = [(ind.seq, ind.makespan) for ind in self.population.individuals]
                all_generations.append((sync_generation[index], generation_data))

                # 각 세대의 인구를 CSV 파일에 저장
                save_population_to_csv(self.population, filename, sync_generation[index])
                
                if best_individual is not None and best_individual.makespan <= self.config.target_makespan:
                    elapsed_time = time.time() - start_time  # 걸린 소요시간 계산
                    print(f"GA{index+1}_Stopping early as best makespan {best_individual.makespan} is below target {self.config.target_makespan}.")
                    print(f"GA{index+1}_Elapsed time: {elapsed_time:.2f} seconds.")  # 소요시간 출력

                    break

                with sync_lock:
                    sync_generation[index] += 1

            if self.pso:
                print(f"GA{index+1}_Applying PSO after all generations")
                for i in range(len(self.population.individuals)):
                    individual = self.population.individuals[i]
                    optimized_individual = self.apply_pso(individual)
                    self.population.individuals[i] = optimized_individual

            end_time = time.time()
            execution_time = end_time - start_time

            if best_individual is not None and hasattr(best_individual, 'monitor'):
                best_individual.monitor.save_event_tracer(self.config.filename['log'])
            else:
                print("No valid best individual or monitor to save the event tracer.")
            return best_individual, self.crossover, self.mutation, all_generations, execution_time, self.best_time

        except Exception as e:
            print(f"Error during GA{index+1} evolution at generation {sync_generation[index]}: {str(e)}")
            # for ind in self.population.individuals:
            #     print(f"Seq: {ind.seq}, Makespan: {ind.makespan}, Machine Order: {ind.machine_order}")

            return None, None, None, [], 0, None