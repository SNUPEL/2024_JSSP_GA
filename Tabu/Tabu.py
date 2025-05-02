from Config.Run_Config import Run_Config
from GAS.Individual import Individual
from Data.Dataset.Dataset import Dataset
from GAS.Population import JSSP
import random
import copy
import pandas as pd
import os
import csv

def swap(individual):
    seq = copy.deepcopy(individual.seq)  # 원래 시퀀스를 깊은 복사
    size = len(seq)

    # 각 Operation이 어느 Job에 속하는지 계산 (index에 해당하는 Job 번호)
    job_indices = [i // individual.config.n_machine for i in range(size)]

    # 염색체 길이에 대한 상대적 비율로 교환 횟수 결정
    num_swaps = 1

    for _ in range(num_swaps):
        i = random.randint(0, size - 1)
        # i와 다른 Job에 속하는 j를 찾을 때까지 반복
        different_job_indices = [j for j in range(size) if job_indices[j] != job_indices[i]]

        # 무조건 다른 Job에 속하는 Operation을 선택
        if different_job_indices:
            j = random.choice(different_job_indices)
            seq[i], seq[j] = seq[j], seq[i]


    new_individual = Individual(individual.config, seq=seq, op_data=individual.op_data)
    return new_individual

def in_tabu(y, T):
    """
    Args:
        y: feasible solution
        T: Tabu Queue
    """
    if y.job_seq in T:
        return True
    else:
        return False

def tabu_search(config, jssp, dataset, seed = 0, use_RUBI = True):
    Y = [] # neighbors
    T = [] # Tabu queue
    max_tabu_size = 10000
    random.seed(seed)
    if use_RUBI:
        s = Individual(config, seq=jssp.get_seq(), op_data=dataset.op_data) # feasible solution
    else:
        s = Individual(config, seq=random.sample(range(config.n_op), config.n_op), op_data=dataset.op_data) # feasible solution
    c = s.makespan

    print("Initial makespan:", c)

    iteration = 0
    max_iterations = 1000
    while iteration < max_iterations:
        Y = []
        C = []
        for m in range(100):
            f = swap(s)
            Y.append(f)
            C.append(f.makespan)

        # 목적함수 기준으로 이웃 정렬
        sorted_neighbors = sorted(zip(Y, C), key=lambda x: x[1])

        found = False
        for idx, (y, cost) in enumerate(sorted_neighbors):
            if not in_tabu(y, T) or cost < c:  # Tabu가 아니거나 Aspiration
                s = y
                c = cost
                T.append(y.job_seq)
                print(idx,f"번째로 좋은 neighbor{y.job_seq}로 교체")
                if len(T) > max_tabu_size:
                    T.pop(0)
                found = True
                break

        if not found:
            print(f"Iteration {iteration}: No non-tabu or better neighbor found.")
            iteration += 1
            continue

        print(f"Iteration {iteration} \t Current makespan: {c}")
        if c == config.target_makespan:
            print(f"Success! Target makespan {c} reached at iteration {iteration}.")
            return s, c, iteration

        iteration += 1

    # 실패한 경우
    print("Fail: Target makespan not reached within max_iterations.")
    return s, c, 0

def run_experiment(instance, target):
    dataset = Dataset(instance)
    jssp = JSSP(dataset)
    config = Run_Config(n_job=dataset.n_job, n_machine=dataset.n_machine, n_op=dataset.n_op, population_size=100,
                        generations=4,
                        print_console=False, save_log=True, save_machinelog=True,
                        show_gantt=False, save_gantt=True, show_gui=False,
                        trace_object='Process4', title='Gantt Chart for JSSP',
                        tabu_search_iterations=10, hill_climbing_iterations=30, simulated_annealing_iterations=50,
                        two_iterations=1000, target_makespan=target)

    result = []

    csv_filename = "Tabu_result.csv"

    # 파일이 처음 생성될 경우, 헤더 추가
    if not os.path.exists(csv_filename):
        with open(csv_filename, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Instance', 'Seed', 'Termination', 'RUBI'])

    for i in range(10):
        solution, makespan, iteration = tabu_search(config, jssp, dataset, seed = i, use_RUBI=False)
        with open(csv_filename, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([ins.split('.')[0], i, iteration, False])
    for i in range(10):
        solution, makespan, iteration = tabu_search(config, jssp, dataset, seed = i, use_RUBI=True)
        with open(csv_filename, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([ins.split('.')[0], i, iteration, True])

if __name__ == '__main__':
    directories = ['la01.txt',
                   'la02.txt',
                   'la03.txt',
                   'la04.txt',
                   'la05.txt',
                   'la06.txt',
                   'la07.txt',
                   'la08.txt',
                   'la09.txt',
                   'la10.txt',
                   'la11.txt',
                   'la12.txt',
                   'la13.txt',
                   'la14.txt',
                   'la15.txt',
                   'la16.txt',
                   'la17.txt',
                   'la18.txt',
                   'la19.txt',
                   'la20.txt']
    optimal = [666, 655, 597, 590, 593, 926,890,863,951,958,
               1222,1039,1150,1292,1207,945,784,848,842,902]
    for ins, opt in zip(directories, optimal):
        run_experiment(ins, opt)

