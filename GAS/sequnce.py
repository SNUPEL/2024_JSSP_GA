import os
import sys
import random
import time
import copy
import csv

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

# Mutation
from GAS.Mutation.GeneralMutation import GeneralMutation
from GAS.Mutation.DisplacementMutation import DisplacementMutation
from GAS.Mutation.InsertionMutation import InsertionMutation
from GAS.Mutation.ReciprocalExchangeMutation import ReciprocalExchangeMutation
from GAS.Mutation.ShiftMutation import ShiftMutation
from GAS.Mutation.InversionMutation import InversionMutation
from GAS.Mutation.SwapMutation import SwapMutation

# Selection
from GAS.Selection.RouletteSelection import RouletteSelection
from GAS.Selection.SeedSelection import SeedSelection
from GAS.Selection.TournamentSelection import TournamentSelection

# Local Search
from Local_Search.HillClimbing import HillClimbing
from Local_Search.TabuSearch import TabuSearch
from Local_Search.SimulatedAnnealing import SimulatedAnnealing
from Local_Search.GifflerThompson_LS import GifflerThompson_LS

# Meta Heuristic
from Meta.PSO import PSO  # pso를 추가합니다

# 선택 mutation 
from GAS.Mutation.SelectiveMutation import SelectiveMutation

from Config.Run_Config import Run_Config
from Data.Dataset.Dataset import Dataset
from visualization.Gantt import Gantt
from postprocessing.PostProcessing import generate_machine_log  # 수정된 부분

from concurrent.futures import ThreadPoolExecutor, as_completed

# Individual 클래스를 임포트합니다.
from GAS.Individual import Individual
import matplotlib.pyplot as plt

# Dataset을 로드합니다.
def load_dataset(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    n_jobs, n_machines = map(int, lines[0].strip().split())
    processing_times = [list(map(int, line.strip().split())) for line in lines[1:n_jobs+1]]
    machines = [list(map(int, line.strip().split())) for line in lines[n_jobs+1:]]
    
    return n_jobs, n_machines, processing_times, machines

# 주어진 시퀀스를 평가합니다.
def evaluate_sequence(n_jobs, n_machines, processing_times, machines, sequence):
    job_operation_counter = {i: 0 for i in range(1, n_jobs+1)}
    machine_end_times = {i: 0 for i in range(1, n_machines+1)}
    job_end_times = {i: 0 for i in range(1, n_jobs+1)}

    gantt_chart_data = []

    for job in sequence:
        job_id = job
        operation_idx = job_operation_counter[job_id]
        machine_id = machines[job_id-1][operation_idx]
        processing_time = processing_times[job_id-1][operation_idx]

        start_time = max(job_end_times[job_id], machine_end_times[machine_id])
        end_time = start_time + processing_time

        gantt_chart_data.append((job_id, machine_id, start_time, end_time))

        job_end_times[job_id] = end_time
        machine_end_times[machine_id] = end_time

        job_operation_counter[job_id] += 1

    makespan = max(job_end_times.values())
    return makespan, gantt_chart_data

# Gantt 차트를 생성합니다.
def plot_gantt_chart(gantt_chart_data):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for job_id, machine_id, start_time, end_time in gantt_chart_data:
        ax.barh(machine_id, end_time - start_time, left=start_time, edgecolor='black', height=0.5)
        ax.text(start_time + (end_time - start_time) / 2, machine_id, f'Job {job_id}', 
                va='center', ha='center', color='white', fontsize=8, fontweight='bold')

    ax.set_xlabel('Time')
    ax.set_ylabel('Machine')
    ax.set_title('Gantt Chart')
    plt.show()

# 메인 함수
def main():
    dataset_path = 'la01.txt'
    sequence = [8, 5, 6, 5, 6, 1, 8, 3, 9, 10, 6, 10, 9, 10, 7, 5, 9, 2, 9, 10, 6, 1, 3, 4, 4, 7, 3, 7, 3, 7, 1, 8, 5, 8, 4, 10, 2, 4, 7, 1, 1, 8, 3, 4, 2, 2, 2, 6, 5, 9]
    sequence = [job  for job in sequence]  # 시퀀스의 모든 요소에 1을 더합니다.
    
    n_jobs, n_machines, processing_times, machines = load_dataset(dataset_path)
    makespan, gantt_chart_data = evaluate_sequence(n_jobs, n_machines, processing_times, machines, sequence)
    print(f"Makespan: {makespan}")
    
    # Gantt 차트를 그립니다.
    plot_gantt_chart(gantt_chart_data)

if __name__ == "__main__":
    main()