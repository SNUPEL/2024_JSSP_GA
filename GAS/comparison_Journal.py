"""
Main script for running the Genetic Algorithm (GA) with various configurations.

This script initializes and runs the GA with different crossover, mutation, selection,
and local search methods. It supports island parallel GA with different migration strategies.

Functions:
    run_ga_engine(args): Runs the GA engine for a given configuration.
    main(): Main function to setup and execute the GA engines.
"""

import os
import sys
import random
import copy
import csv
import time
import datetime
from multiprocessing import Pool, Value, Array, Manager, Lock

import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from GAS.GA import GAEngine
from GAS.Crossover.PMX import PMXCrossover
from GAS.Mutation.CompositeMutation import CompositeMutation
from GAS.Selection.RouletteSelection import RouletteSelection
from Config.Run_Config import Run_Config
from Data.Dataset.Dataset_jsplib import Dataset

MIGRATION_FREQUENCY = 10100  # Migration frequency 설정



def run_ga_engine(args):
    ga_engine, index, experiment_path, sync_generation, sync_lock, events, new_populations = args
    try:
        # evolve 함수 호출 시 new_populations 전달
        best, best_crossover, best_mutation, all_generations, execution_time, best_time = ga_engine.evolve(index, sync_generation, sync_lock, new_populations, events, dirname=experiment_path)
        if best is None:
            return None
        return best, best_crossover, best_mutation, all_generations, execution_time, best_time, index
    except Exception as e:
        import traceback
        traceback.print_exc()  # 트레이스백 출력
        print(f"Exception in GA {index+1}: {e}")
        return None

def main_GA(_kwargs):

    """
    Main function to setup and execute the GA engines.
    """
    _file=_kwargs['_file']
    _resultfile=_kwargs['_resultfile']
    _instance=_kwargs['_instance']
    _initialization=_kwargs['_initialization']
    _optimal = kwargs['_optimal']
    _seed=_kwargs['_seed']
    _record = _kwargs['_record']
    print(f'{_instance} | seed: {_seed} | optimal: {_optimal} | Initialization :{_initialization}')
    np.random.seed(_seed)
    random.seed(_seed)
    # print(np.random.rand())
    dataset = Dataset(_file)

    # Custom GA settings    
    base_config = Run_Config(n_job=dataset.n_job, n_machine=dataset.n_machine, n_op=dataset.n_op,
                             population_size=1000, generations=2,
                             print_console=False, save_log=True, save_machinelog=False,
                             show_gantt=False, save_gantt=False, show_gui=False,
                             trace_object='Process4', title='Gantt Chart for JSSP',
                             tabu_search_iterations=10, hill_climbing_iterations=30,
                             simulated_annealing_iterations=50, two_iterations=1000)
    # print("Base config created...")  # 디버그 출력 추가
    base_config.dataset_filename = _file  # dataset 파일명 설정
    base_config.target_makespan = _optimal
    base_config.island_mode = '1'  # Add this line to set island_mode
    keyword = _instance+"-"+_initialization
    result_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'result')
    experiment_path = os.path.join(result_path, keyword)

    # if not os.path.exists(result_path):
    #     os.makedirs(result_path)
    # if not os.path.exists(experiment_path):
    #     os.makedirs(experiment_path)
    custom_settings = [
        {'crossover': PMXCrossover, 'pc': 0.9, 'mutation': CompositeMutation, 'pm': 0.9, 'selection': RouletteSelection(), 'local_search': [], 'pso': None, 'selective_mutation': None},  # APMS Setting
        ]
    GA_start = time.time()

    ga_engines = []
    for i, setting in enumerate(custom_settings):
        crossover_class = setting['crossover']
        mutation_class = setting['mutation']
        selection_instance = setting['selection']
        local_search_methods = setting['local_search']
        pso_class = setting.get('pso')
        selective_mutation_instance = setting['selective_mutation']
        pc = setting['pc']
        pm = setting['pm']

        initialization_mode = _initialization
        print(f"Selected Initialization GA mode for GA{i+1}: {initialization_mode}")

        config = copy.deepcopy(base_config)
        config.ga_index = i + 1

        crossover = crossover_class(pc=pc)
        mutation = mutation_class(pm=pm)
        selection = selection_instance
        pso = pso_class if pso_class else None
        local_search = local_search_methods
        local_search_frequency = 100000
        selective_mutation_frequency = 100000
        selective_mutation = selective_mutation_instance

        ##############################################
        # elite_ratio 설정: 0.1이면 10%
        ##############################################

        ga_engine = GAEngine(config, dataset.op_data, crossover, mutation, selection, local_search,
                             pso, selective_mutation, elite_ratio=0.1, ga_engines=ga_engines, island_mode='1',
                             migration_frequency=MIGRATION_FREQUENCY,
                             initialization_mode=initialization_mode,
                             dataset_filename=_file,
                             local_search_frequency=local_search_frequency,
                             selective_mutation_frequency=selective_mutation_frequency,
                             random_seed=_seed,
                             record=_record)
        initial_best = copy.deepcopy(min([ind.makespan for ind in ga_engine.population.individuals]))
        ga_engines.append(ga_engine)

        # print(f"Initialized GAEngine {i+1}")  # 디버그 출력 추가
    GA_initialization_time = time.time()
    best_individuals = [None] * len(ga_engines)
    stop_evolution = Manager().Value('i', 0)
    elite_population = Manager().list([None] * len(ga_engines))

    manager = Manager()
    new_populations = manager.list([[] for _ in range(len(ga_engines))])  # Manager를 통한 공유 리스트

    sync_generation = manager.list([0] * len(ga_engines))
    sync_lock = manager.Lock()

    with Pool() as pool:
        while True:
            args = [(ga_engines[i], i, experiment_path, sync_generation, sync_lock, None, new_populations) for i in range(len(ga_engines))]

            results = pool.map(run_ga_engine, args)
            all_completed = True
            for result in results:
                if result is not None:
                    best, best_crossover, best_mutation, all_generations, execution_time, best_time, index = result
                    best_individuals[index] = (best, best_crossover, best_mutation, execution_time, best_time, all_generations)
                    elite_population[index] = best

                    # 세대가 끝날 때마다 상위 10% 개체를 new_populations에 저장
                    top_individuals = sorted(ga_engines[index].population.individuals, key=lambda ind: ind.makespan)[:max(1, len(ga_engines[index].population.individuals) // 10)]
                    new_populations[index] = [copy.deepcopy(ind) for ind in top_individuals]

                    crossover_name = best_crossover.__class__.__name__
                    mutation_name = best_mutation.__class__.__name__
                    selection_name = ga_engines[index].selection.__class__.__name__
                    local_search_names = [ls.__class__.__name__ for ls in ga_engines[index].local_search]
                    local_search_name = "_".join(local_search_names)
                    pso_name = ga_engines[index].pso.__class__.__name__ if ga_engines[index].pso else 'None'
                    pc = best_crossover.pc
                    pm = best_mutation.pm
                    log_path = os.path.join(experiment_path, f'log_GA{index+1}_{crossover_name}_{mutation_name}_{selection_name}_{local_search_name}_{pso_name}_pc{pc}_pm{pm}.csv')
                    machine_log_path = os.path.join(experiment_path, f'machine_log_GA{index+1}_{crossover_name}_{mutation_name}_{selection_name}_{local_search_name}_{pso_name}_pc{pc}_pm{pm}.csv')
                    generations_path = os.path.join(experiment_path, f'ga_generations_GA{index+1}_{crossover_name}_{mutation_name}_{selection_name}_{local_search_name}_{pso_name}_pc{pc}_pm{pm}.csv')

                    if base_config.target_makespan is not None:
                        if best.makespan <= base_config.target_makespan:
                            stop_evolution.value = 1
                            print(f"Stopping early as best makespan {best.makespan} is below target {base_config.target_makespan}.")
                            break

                    if os.path.exists(log_path) and os.path.exists(machine_log_path) and os.path.exists(generations_path):
                        stop_evolution.value = 1
                        print(f"Stopping as all files for GA{index+1} are generated.")
                        break
                else:
                    all_completed = False

            if stop_evolution.value or all_completed:
                break
    GA_finish = time.time()
    for i, result in enumerate(best_individuals):
        if result is not None:
            best, best_crossover, best_mutation, execution_time, best_time, all_generations = result
            with open(_resultfile, 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                initialization_time = GA_initialization_time - GA_start
                total_time = GA_finish - GA_start
                csvwriter.writerow([_instance.split('.')[0], dataset.n_job, dataset.n_machine, _instance.split('.')[0].split('_')[-1],
                                    dataset.I_b, dataset.I_f,
                                    _optimal,
                                    _initialization, _seed, initial_best, best.makespan, best_time, initialization_time, total_time])


if __name__ == "__main__":
    from itertools import product
    from datetime import datetime
    from tqdm import tqdm
    import json

    with open('Data/Dataset/JSPLIB/instances.json', 'r', encoding='utf-8') as f:
        instance_list = json.load(f)

    # 현재 시각을 YYMMDDhhmmss 형식으로 문자열 변환
    timestamp = datetime.now().strftime("%y%m%d%H%M%S")

    # result 파일 이름 구성
    result_filename = f"result/result_{timestamp}.csv"

    with open(result_filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Filename', 'n_job', 'n_machine', 'Instance', 'I_b', 'I_f', 'Optimal','Initialization', 'Seed',
                            'Initial Best', 'Best Makespan', 'Best Reached Time', 'Initialization Time', 'Execution Time'])

    root_dir = 'Data/Dataset/JSPLIB/instances'

    problems = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for file in filenames:
            problems.append(os.path.join(dirpath, file))

    # 반복 대상 정의
    seed_list = range(1)
    init_list = ['SPT','LPT']
    # init_list = ['RANDOM', 'RUBI', 'GT']

    # 전체 조합 수 계산
    total_iter = len(problems) * len(seed_list) * len(init_list)

    for i, (ins, seed, ini) in enumerate(
            tqdm(product(problems, seed_list, init_list), total=total_iter, desc="Running GA comparisons")
    ):
        if ins.split('.')[-1].split('\\')[-1][:2] in []:
        # if ins.split('.')[-1].split('\\')[-1][:2] in ['ab', 'la', 'or', 'ft', 'sw', 'ta']:
            pass
        else:
            problem_index = problems.index(ins)
            kwargs = {'_file': ins,
                      '_resultfile': result_filename,
                      '_instance': ins.split('.')[-1].split('\\')[-1],
                      '_initialization': ini,
                      '_seed': seed,
                      '_optimal': instance_list[problem_index]['optimum'],
                      '_record':False}
            main_GA(kwargs)

