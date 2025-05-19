"""
Dataset Loader

This script defines the Dataset class, which is used to load and parse a dataset
file for job and machine scheduling problems. The dataset is expected to be in a
specific format where the first line contains the number of jobs and machines, 
and the subsequent lines contain the operation data.

Attributes:
    filename (str): The name of the dataset file.
    name (str): The base name of the dataset file without the extension.
    path (str): The path to the dataset file.
    n_job (int): Number of jobs.
    n_machine (int): Number of machines.
    n_op (int): Number of operations (n_job * n_machine).
    op_data (list): List of operation data parsed from the file.
    n_solution (int): Number of solutions (initialized to 0).
"""
import os
import sys
import numpy as np
from Data.Metrics import calculate_bottleneck_index, calculate_flowshop_index

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from GAS.Individual import Individual
# from Data.Metrics import calculate_flowshop_index, calculate_bottleneck_index

# class Solution():

class Dataset:
    def __init__(self, filename):
        """
        Initializes the Dataset class with the specified filename and loads the dataset.

        Parameters:
            filename (str): The name of the dataset file.
        """
        self.name, _ = os.path.splitext(filename)
        self.path = 'Data\\Dataset\\'
        if __name__ == "__main__":
            file_path = os.path.join(os.getcwd(), filename)
        else:
            file_path = os.path.join(os.path.dirname(__file__), filename)

        # Read the first line of the file to get the number of jobs and machines
        with open(file_path, 'r') as file:
            first_line = file.readline()

        self.n_job, self.n_machine = map(int, first_line.strip().split('\t'))
        self.n_op = self.n_job * self.n_machine

        # Initialize operation data list
        self.op_data = []

        # division of machine data and processing time data
        self.machine_data = []
        self.pt_data = []
        data = pd.read_csv(file_path, sep="\t", engine='python', encoding="cp949", skiprows=[0], header=None)

        # Parse the operation data from the file
        for i in range(self.n_job):
            self.op_data.append([])
            self.machine_data.append([])
            self.pt_data.append([])
            for j in range(self.n_machine):
                self.op_data[i].append((data.iloc[self.n_job + i, j] - 1, data.iloc[i, j]))
                self.machine_data[i].append(data.iloc[self.n_job + i, j] - 1)
                self.pt_data[i].append(data.iloc[i, j])
        self.n_solution = 0  # Initialize the number of solutions to 0
        self.I_b = self.calculate_bottleneck_index()
        self.I_f = self.calculate_flowshop_index()

    def calculate_flowshop_index(self):
        I_ik = np.zeros((self.n_machine, self.n_machine))

        for n in range(self.n_job):
            for i in range(self.n_machine - 1):
                first = self.machine_data[n][i]
                second = self.machine_data[n][i + 1]
                I_ik[first, second] += 1
        I_f = np.subtract(I_ik, 1)
        I_f = I_f.clip(min=0)
        I_f = np.divide(I_f, self.n_job - 1)
        I_f = I_f.sum() / (self.n_machine - 1)
        return I_f

    def calculate_bottleneck_index(self):
        I_ik = np.zeros((self.n_machine, self.n_machine))
        for i in range(self.n_machine):  # machine i
            for k in range(self.n_machine):  # appears as k-th operation
                is_kth = [True if self.op_data[n][k][0] == i else False for n in range(self.n_machine)]
                I_ik[i, k] += sum(is_kth)

        I_b = np.subtract(I_ik, 1)
        I_b = I_b.clip(min=0)
        I_b = np.divide(I_b, self.n_job - 1)
        I_b = I_b.sum() / self.n_machine

        return I_b

if __name__ == "__main__":
    d = Dataset('abz5.txt')
    print()
