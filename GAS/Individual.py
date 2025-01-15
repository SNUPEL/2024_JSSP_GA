"""
Individual Class

This script defines the Individual class, which represents a solution to the job shop scheduling problem. 
It includes functionalities for interpreting solutions, evaluating makespan and fitness, 
and generating machine order sequences.

Functions:
    calculate_score(x_array, y_array): Calculates various scores between two arrays.
    swap_digits(num): Swaps the digits of a two-digit number.
    Individual.__init__(self, config=None, seq=None, solution_seq=None, op_data=None): Initializes an individual with the given parameters.
    Individual.__str__(self): Returns a string representation of the individual.
    Individual.calculate_fitness(self, target_makespan): Calculates the fitness of the individual.
    Individual.interpret_solution(self, s): Interprets a solution sequence by swapping digits.
    Individual.get_repeatable(self): Generates a repeatable job sequence.
    Individual.get_feasible(self): Generates a feasible sequence.
    Individual.get_machine_order(self): Generates the machine order for the sequence.
    Individual.evaluate(self, machine_order): Evaluates the makespan and MIO score for the individual.
"""

import sys
import os
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import simpy
from environment.Source import Source
from environment.Sink import Sink
from environment.Part import Job, Operation
from environment.Process import Process
from environment.Resource import Machine
from environment.Monitor import Monitor
from postprocessing.PostProcessing import *
from visualization.Gantt import *
from visualization.GUI import GUI
from MachineInputOrder.utils import kendall_tau_distance, spearman_footrule_distance, spearman_rank_correlation, bubble_sort_distance, MSE

def calculate_score(x_array, y_array):
    score = [0.0 for i in range(6)]
    for i in range(len(x_array)):
        score[0] += kendall_tau_distance(x_array[i], y_array[i])
        score[1] += spearman_rank_correlation(x_array[i], y_array[i])
        score[2] += spearman_footrule_distance(x_array[i], y_array[i])
        score[3] += MSE(x_array[i], y_array[i])
        score[4] += bubble_sort_distance(x_array[i])
        correlation_matrix = np.corrcoef(x_array[i], y_array[i])
        score[5] += correlation_matrix[0, 1]
    return score

def swap_digits(num):
    if num < 10:
        return num * 10
    else:
        units = num % 10
        tens = num // 10
        return units * 10 + tens

class Individual:
    def __init__(self, config=None, seq=None, solution_seq=None, op_data=None):
        self.fitness = None
        self.monitor = None  # Add monitor attribute
        if solution_seq is not None:
            self.seq = self.interpret_solution(solution_seq)
        else:
            self.seq = seq

        self.config = config
        self.op_data = op_data
        self.MIO = []
        self.MIO_sorted = []
        self.job_seq = self.get_repeatable()
        self.feasible_seq = self.get_feasible()
        self.machine_order = self.get_machine_order()
        self.makespan, self.mio_score = self.evaluate(self.machine_order)
        self.score = calculate_score(self.MIO, self.MIO_sorted)
        self.calculate_fitness()  # Ensure target_makespan is passed

    def __str__(self):
        return f"Individual(makespan={self.makespan}, fitness={self.fitness})"

    def calculate_fitness(self, best=None, worst=None):
        if self.makespan == 0:
            raise ValueError("Makespan is zero, which will cause division by zero error.")
        if best is not None:
            self.fitness = 1 / (self.makespan/best)
            # gap = worst - best
            # if best == worst:
            #     self.fitness = 0.1
            # else:
            #     ratio = (self.makespan - best + 1) / gap
            #     # if denominator == 0:
            #     #     denominator = 1
            #     self.fitness = 1 - ratio
            #     # if self.fitness <=0.5:
            #     #     self.fitness = 0.1
            #     # self.fitness = 1 / (self.makespan - target_makespan + 1)
        else:
            self.fitness = 1 / self.makespan
        return self.fitness

    def interpret_solution(self, s):
        modified_list = [swap_digits(num) for num in s]
        return modified_list

    def get_repeatable(self):
        cumul = 0
        sequence_ = np.array(self.seq)
        for i in range(self.config.n_job):
            for j in range(self.config.n_machine):
                sequence_ = np.where((sequence_ >= cumul) & (sequence_ < cumul + self.config.n_machine), i, sequence_)
            cumul += self.config.n_machine
        return sequence_.tolist()

    def get_feasible(self):
        temp = 0
        cumul = 0
        sequence_ = np.array(self.seq)
        for i in range(self.config.n_job):
            idx = np.where((sequence_ >= cumul) & (sequence_ < cumul + self.config.n_machine))[0]
            for j in range(min(len(idx), self.config.n_machine)):
                sequence_[idx[j]] = temp
                temp += 1
            cumul += self.config.n_machine
        return sequence_

    def get_machine_order(self):
        m_list = []
        for num in self.feasible_seq:
            idx_j = num % self.config.n_machine
            idx_i = num // self.config.n_machine
            m_list.append(self.op_data[idx_i][idx_j][0])
        m_list = np.array(m_list)

        m_order = []
        for num in range(self.config.n_machine):
            idx = np.where((m_list == num))[0]
            job_order = [self.job_seq[o] for o in idx]
            m_order.append(job_order)
        return m_order

    def evaluate(self, machine_order):
        try:
            # Debug: machine_order 요약
            # print(f"Evaluating with machine_order: {machine_order[:2]} ...")  # 첫 두 개의 machine_order만 출력

            env = simpy.Environment()
            self.monitor = Monitor(self.config)
            model = dict()
            
            # 모델 초기화
            for i in range(self.config.n_job):
                model['Source' + str(i)] = Source(env, 'Source' + str(i), model, self.monitor, part_type=i, op_data=self.op_data, config=self.config)

            for j in range(self.config.n_machine):
                model['Process' + str(j)] = Process(env, 'Process' + str(j), model, self.monitor, machine_order[j], self.config)
                model['M' + str(j)] = Machine(env, j)

            model['Sink'] = Sink(env, self.monitor, self.config)

            # 시뮬레이션 실행
            env.run(self.config.simul_time)
            # print(f"Simulation completed.")

            # Machine input/output 추적
            self.MIO = []
            self.MIO_sorted = []
            
            # MIO 계산
            for i in range(self.config.n_machine):
                mio = model['M' + str(i)].op_where
                self.MIO.append(mio)
                self.MIO_sorted.append(np.sort(mio))

            # MIO Score 및 Makespan 계산
            mio_score = np.sum(np.abs(np.subtract(np.array(mio), np.array(sorted(mio)))))
            makespan = model['Sink'].last_arrival
            
            # 간결한 결과 출력
            # print(f"Evaluation complete: Makespan = {makespan}, MIO Score = {mio_score}")

            return makespan, mio_score

        except Exception as e:
            print(f"Error during evaluation: {e}")
            raise
