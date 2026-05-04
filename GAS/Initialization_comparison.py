import os

import numpy as np

from GAS.Population import Population
from Config.Run_Config import Run_Config
import copy
from Data.DataGenerator import *
import time
from Data.Dataset.Dataset import Dataset
from itertools import product
from tqdm import tqdm
import datetime

def make_comparison(file):
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
    time_dict = {}
    mean_dict = {}
    best_dict = {}

    popul_dict['RANDOM'] = Population(config, dataset.op_data)
    time_random = time.time()
    time_dict['RANDOM'] = time_random - init_start

    popul_dict['RUBI'] = Population.from_mio(config, dataset.op_data, file)
    time_RUBI = time.time()
    time_dict['RUBI'] = time_RUBI - time_random

    # popul_dict['MoRUBI'] = Population.from_modified_rubi(config, dataset.op_data, file)
    # time_MoRUBI = time.time()
    # time_dict['MoRUBI'] = time_MoRUBI - time_RUBI
    #
    popul_dict['SPT'] = Population.from_SPT(config, dataset.op_data, file)
    time_SPT = time.time()
    time_dict['SPT'] = time_SPT - time_RUBI

    popul_dict['LPT'] = Population.from_LPT(config, dataset.op_data, file)
    time_LPT = time.time()
    time_dict['LPT'] = time_LPT - time_SPT

    popul_dict['GT'] = Population.from_GT(config, dataset.op_data, file)
    time_GT = time.time()
    time_dict['GT'] = time_GT - time_LPT
    # time_dict['GT'] = time_GT - time_LPT

    for init_mode in ['RANDOM', 'RUBI', 'SPT', 'LPT', 'GT']:
    # for init_mode in ['RANDOM', 'RUBI', 'MoRUBI', 'SPT', 'LPT', 'GT']:
        mean_dict[init_mode] = np.mean([ind.makespan for ind in popul_dict[init_mode].individuals])
        best_dict[init_mode] = np.min([ind.makespan for ind in popul_dict[init_mode].individuals])
    metrics = {}
    metrics['I_b'] = dataset.I_b
    metrics['I_f'] = dataset.I_f
    return metrics, time_dict, mean_dict, best_dict


if __name__ == '__main__':
    root_dir = '../Data/Dataset/Comparison'

    # problems = []
    # for dirpath, dirnames, filenames in os.walk(root_dir):
    #     for file in filenames:
    #         problems.append(os.path.join(dirpath, file))

    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    with open(f'Initialization_comparison_{current_time}.csv', 'w') as f:
        f.write('num_job,num_machine,mean,std,seed,'
                'I_b,I_f,baseline,'
                'RANDOM_best,RANDOM_time,'
                'RUBI_best,RUBI_time,'
                # 'MoRUBI_best,MoRUBI_time,'
                'SPT_best,SPT_time,'
                'LPT_best,LPT_time,'
                'GT_best,GT_time\n')

    pt_mean = 3
    # 만들고 싶은 문제모드 설정

    seed_list = list(range(20))
    num_job_list = [200]
    num_machine_list = [5]
    std_list = [0]
    level_list = [0]

    for seed, num_job, num_machine, std, level in tqdm(
            product(seed_list, num_job_list, num_machine_list, std_list, level_list),
            total=len(seed_list)*len(num_job_list)*len(num_machine_list)*len(std_list)*len(level_list),
            desc="Comparison"):

        # stats = {'mode': 'Normal',
        #          'mean': pt_mean,
        #          'std': std,
        #          'prob':0.05*level
        #          }
        stats = {'mode': 'Uniform',
                 'LB': 1,
                 'UB': 6,
                 'prob': 0.05 * level
                 }

        # 터미널에서 실행할 때
        file = generate_JSSP_data(num_job, num_machine, stats, 'Data/Dataset/Comparison/', seed=seed)

        # 파이참에서 실행할 때
        # file = generate_JSSP_data(num_job, num_machine, stats, '../Data/Dataset/Comparison/', seed=seed)

        # file = generate_flowshoplike_data(num_job, num_machine, stats, f'../Data/Dataset/Comparison/FS{str(level)}', seed=seed)
        # file = generate_bottleneckshop_data(num_job, num_machine, stats, f'Data/Dataset/Comparison/BS{str(level)}', seed=seed)
        # file = '../Data/Dataset/Comparison/BS18_1010_0.txt'
        metrics, time_dict, mean_dict, best_dict = make_comparison(file)

        with open(f'Initialization_comparison_{current_time}.csv', 'a') as f:
            f.write(f'{num_job},{num_machine},{pt_mean},{std},{seed},'
                    f'{metrics["I_b"]},{metrics["I_f"]},'
                    f'{mean_dict["RANDOM"]},'
                    f'{best_dict["RANDOM"]},{time_dict["RANDOM"]},'
                    f'{best_dict["RUBI"]},{time_dict["RUBI"]},'
                    # f'{best_dict["MoRUBI"]},{time_dict["MoRUBI"]},'
                    f'{best_dict["SPT"]},{time_dict["SPT"]},'
                    f'{best_dict["LPT"]},{time_dict["LPT"]},'
                    f'{best_dict["GT"]},{time_dict["GT"]}\n')