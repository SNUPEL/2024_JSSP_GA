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
import datetime
from multiprocessing import Pool, Value, Array, Manager, Lock

import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from GAS.GA import GAEngine
# Crossover
from GAS.Crossover.PMX import PMXCrossover
from GAS.Crossover.CX import CXCrossover
from GAS.Crossover.LOX import LOXCrossover
from GAS.Crossover.OrderBasedCrossover import OBC
from GAS.Crossover.PositionBasedCrossover import PositionBasedCrossover
from GAS.Crossover.SXX import SXX
from GAS.Crossover.PSX import PSXCrossover
from GAS.Crossover.OrderCrossover import OrderCrossover
from GAS.Crossover.POXCrossover import POXCrossover
from GAS.Crossover.CompositeCrossover import CompositeCrossover

# Mutation
from GAS.Mutation.GeneralMutation import GeneralMutation
from GAS.Mutation.DisplacementMutation import DisplacementMutation
from GAS.Mutation.InsertionMutation import InsertionMutation
from GAS.Mutation.ReciprocalExchangeMutation import ReciprocalExchangeMutation
from GAS.Mutation.ShiftMutation import ShiftMutation
from GAS.Mutation.InversionMutation import InversionMutation
from GAS.Mutation.SwapMutation import SwapMutation
from GAS.Mutation.CompositeMutation import CompositeMutation

# Selection
from GAS.Selection.RouletteSelection import RouletteSelection
from GAS.Selection.SeedSelection import SeedSelection
from GAS.Selection.TournamentSelection import TournamentSelection

# Local Search
from Local_Search.HillClimbing import HillClimbing
from Local_Search.TabuSearch import TabuSearch
from Local_Search.SimulatedAnnealing import SimulatedAnnealing
from Local_Search.GifflerThompson_LS import GifflerThompson_LS
from Local_Search.TwoOptLocalSearch import TwoOptLocalSearch
from Local_Search.SimulatedAnnealing_insert import SimulatedAnnealing_insert
from Local_Search.TwoOptLocalSearch_insert import TwoOptLocalSearch_insert

# Meta Heuristic
from Meta.PSO import PSO  # pso를 추가합니다

# Selective Mutation
from GAS.Mutation.SelectiveMutation import SelectiveMutation

from Config.Run_Config import Run_Config
from Data.Dataset.Dataset import Dataset
from visualization.Gantt import Gantt
from postprocessing.PostProcessing import generate_machine_log  # 수정된 부분


'''
txt : TARGET_MAKESPAN, Jobs, Machines

la01: 666  10, 5/  la11: 1222  20, 5
la02: 655  10, 5/  la12: 1039  20, 5
la03: 597  10, 5/  la13: 1150  20, 5
la04: 590  10, 5/  la14: 1292  20, 5
la05: 593  10, 5/  la15: 1207  20, 5
la06: 926  15, 5/  la16: 945   10, 10
la07: 890  15, 5/  la17: 784   10, 10
la08: 863  15, 5/  la18: 848   10, 10
la09: 951  15, 5/  la19: 842   10, 10
la10: 958  15, 5/  la20: 902   10, 10

ta21: 1642 20 20/  ta51: 2760 50 15
ta22: 1561 1600 20 20/  ta52: 2756 50 15
ta31: 1764 30 15/  ta61: 2868 50 20
ta32: 1774 1784 30 15/  ta62: 2869 50 20
ta41: 1906 2005 30 20/  ta71: 5464 100 20
ta42: 1884 1937 30 20/  ta72: 5181 100 20

abz5 = 1234  10, 10
ft20 = 1165
'''

############################################################################################
# TARGET_MAKESPAN 문제에 맞게 수정바람
############################################################################################

# Configuration for target makespan and migration frequency
# TARGET_MAKESPAN = 666  # 목표 Makespan
MIGRATION_FREQUENCY = 10100  # Migration frequency 설정
# random_seed = None  # Population 초기화시 일정하게 만들기 위함. None을 넣으면 아예 랜덤 생성(GA들끼리 같지않음)
from GAS.Population import Population




def main(_kwargs):

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
    print(f'{_instance} | seed: {_seed} | optimal: {_optimal} | RUBI ratio:{_initialization}')


    np.random.seed(_seed)
    random.seed(_seed)
    # print(np.random.rand())
    dataset = Dataset(_file)

    # Custom GA settings    
    base_config = Run_Config(n_job=dataset.n_job, n_machine=dataset.n_machine, n_op=dataset.n_op,
                             population_size=100, generations=100,
                             print_console=False, save_log=True, save_machinelog=True,
                             show_gantt=False, save_gantt=True, show_gui=False,
                             trace_object='Process4', title='Gantt Chart for JSSP',
                             tabu_search_iterations=10, hill_climbing_iterations=30,
                             simulated_annealing_iterations=50, two_iterations=1000)

    pop = Population.from_mio(base_config, dataset.op_data, _file, random_seed=_seed, percentage=int(_initialization))
    makespans = [individual.makespan for individual in pop.individuals]
    min_makespan = min(makespans)
    avg_makespan = sum(makespans) / len(makespans) if makespans else 0
    with open(_resultfile, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([_instance.split('.')[0], dataset.I_b, dataset.I_f, _initialization, _seed, min_makespan, avg_makespan])

if __name__ == "__main__":
    # temp = [str(i+1) for i in range(8,20)]
    # instances = []
    # for ins in temp:
    #     if len(ins)==1:
    #         instances.append('0'+ins)
    #     else:
    #         instances.append(ins)

    with open('../result/250318_initialization_100.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Problem', 'I_b', 'I_f', 'RUBI Ratio', 'Seed', 'Best Makespan', 'Mean Makespan'])

    """
    la01: 666  10, 5/  la11: 1222  20, 5
    la02: 655  10, 5/  la12: 1039  20, 5
    la03: 597  10, 5/  la13: 1150  20, 5
    la04: 590  10, 5/  la14: 1292  20, 5
    la05: 593  10, 5/  la15: 1207  20, 5
    la06: 926  15, 5/  la16: 945   10, 10
    la07: 890  15, 5/  la17: 784   10, 10
    la08: 863  15, 5/  la18: 848   10, 10
    la09: 951  15, 5/  la19: 842   10, 10
    la10: 958  15, 5/  la20: 902   10, 10
    """
    root_dir = '../Data/Dataset/APMS'
    directories = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.txt'):
                directories.append(file)
    # optimal = [951,958,1222,1039,1150,1292,1207,945,784,848,842,902]
    # optimal = [666,655,597,590,593,926,890,863,951,958,1222,1039,1150,1292,1207,945,784,848,842,902]
    optimal={'abz5':1234,
             'abz6':943,
             'abz7':656,
             'abz8':645,
             'abz9':661,
             'ft06':55,
             'ft10':930,
             'ft20':1165,
             'ta21':1539,
             'ta22':1511,
             'ta31':1764,
             'ta32':1774,
             'ta41':1859,
             'ta42':1867,
             'ta51':2760,
             'ta52':2756,
             'ta61':2868,
             'ta62':2869,
             'ta71':None,
             'ta72':None}
    for i, ins in enumerate(directories):
        for seed in [2]:
            for ini in ['0', '100']:
            # for ini in ['0', '10', '20', '40']:
                kwargs = {'_file': 'APMS/'+ins,
                # kwargs = {'_file': 'APMS/'+ins,
                          '_resultfile': '../result/250318_initialization_100.csv',
                          '_instance': ins.split('.')[0],
                          '_initialization': ini,
                          '_seed': seed,

                          '_optimal': None,
                          '_record':False}
                          # '_optimal': optimal[ins.split('.')[0]]}
                main(kwargs)
