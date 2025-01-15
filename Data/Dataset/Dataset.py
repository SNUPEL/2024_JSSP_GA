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
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from GAS.Individual import Individual  
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
        data = pd.read_csv(file_path, sep='\t', engine='python', encoding="cp949", skiprows=[0], header=None)

        # Parse the operation data from the file
        for i in range(self.n_job):
            self.op_data.append([])
            for j in range(self.n_machine):
                self.op_data[i].append((data.iloc[self.n_job + i, j] - 1, data.iloc[i, j]))

        self.n_solution = 0 # Initialize the number of solutions to 0

