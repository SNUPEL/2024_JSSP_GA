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

MIGRATION_FREQUENCY = 10100
from GAS.Population import Population
from Config.Run_Config import Run_Config
from Data.DataGenerator import *
import time

def make_heuristic_comparison(file):
    dataset = Dataset(file)
    init_start = time.time()
    random_seed = 0
    # Custom GA settings
    config = Run_Config(n_job=dataset.n_job, n_machine=dataset.n_machine, n_op=dataset.n_op,
                        population_size=100, generations=100,
                        print_console=False, save_log=True, save_machinelog=True,
                        show_gantt=False, save_gantt=True, show_gui=False,
                        trace_object='Process4', title='Gantt Chart for JSSP',
                        tabu_search_iterations=10, hill_climbing_iterations=30,
                        simulated_annealing_iterations=50, two_iterations=1000)
    config.dataset_filename = file  # dataset 파일명 설정
    config.target_makespan = None  # 목표 Makespan
    config.island_mode = '1'  # Add this line to set island_mode

    popul_dict = {}
    mean_dict = {}

    popul_dict['SPT'] = Population.from_SPT(config, dataset.op_data, file)
    popul_dict['LPT'] = Population.from_LPT(config, dataset.op_data, file)
    for init_mode in ['SPT', 'LPT']:
        mean_dict[init_mode] = np.mean([ind.makespan for ind in popul_dict[init_mode].individuals])

    return mean_dict


if __name__ == "__main__":
    from datetime import datetime
    import json
    from tqdm import tqdm

    with open('../Data/Dataset/JSPLIB/instances.json', 'r', encoding='utf-8') as f:
        instance_list = json.load(f)

    # 현재 시각을 YYMMDDhhmmss 형식으로 문자열 변환
    timestamp = datetime.now().strftime("%y%m%d%H%M%S")

    # result 파일 이름 구성
    result_filename = f"../result/result_{timestamp}.csv"

    with open(result_filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Filename', 'SPT', 'LPT'])

    root_dir = '../Data/Dataset/JSPLIB/instances'

    problems = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for file in filenames:
            problems.append(os.path.join(dirpath, file))

    for ins in tqdm(problems, desc="Heuristic comparison progress"):
        if ins.split('.')[-1].split('\\')[-1][:2] in ['ta']:
            pass
        else:
            problem_index = problems.index(ins)
            result_dict = make_heuristic_comparison(ins)

            # 한 줄씩 결과 추가
            with open(result_filename, 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([
                    ins,
                    result_dict['SPT'],
                    result_dict['LPT']
                ])


