import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
# from itertools import permutations
# import numpy as np
# from statistics import *
# from Dataset.Dataset import Dataset
from Metrics import *
import random


def generate_JSSP_data(num_job, num_machine, prefix):
    filename = prefix + str(num_job) + str(num_machine) + '.txt'
    first_line = f"{num_job}\t{num_machine}"
    df = pd.DataFrame(np.random.randint(11, 41, size=(num_job, num_machine)))
    # 각 행의 숫자를 1부터 num_machine까지의 permutation으로 변경
    for i in range(num_job):
        permutation = np.random.permutation(np.arange(1, num_machine + 1)).astype(int)
        df.loc[df.shape[0]] = permutation

    # 파일 작성
    with open(filename, 'w') as f:
        # 첫번째 줄 작성
        f.write(first_line + '\n')
        # 데이터프레임을 파일에 작성
        df.to_csv(f, sep='\t', index=False, header=False, lineterminator='\n')  # Updated lineterminator


def generate_bottleneckshop_data(n_job, n_machine, probability, prefix, instance):
    first_line = f"{num_job}\t{num_machine}"
    df = pd.DataFrame(np.random.randint(11, 101, size=(num_job, num_machine)))
    machine_data = []

    for i in range(num_job):
        permutation = np.random.permutation(np.arange(0, num_machine)).astype(int)
        for j in range(num_machine - 1):
            if random.random() < probability:  # modifying event occurred!
                # print('modifying event occurred!')
                # print('Original permutation:', permutation)
                target = permutation[j].copy() # j번째 자리에 들어있는 것은? (j여야 함)
                j_position = np.where(permutation==j) # 실제로 j가 들어있는 곳은?
                if (j_position != j):
                    permutation[j] = j
                    permutation[j_position] = target
                # print('Modified permutation:', permutation)
                # print('-' * 30)
        pmt = permutation.tolist()
        machine_data.append([t + 1 for t in pmt])
        df.loc[df.shape[0]] = [t + 1 for t in pmt]

    # Bottleneck Index
    I_bik = np.zeros((n_machine, n_machine))
    for i in range(n_machine):  # machine i
        for k in range(n_machine):  # appears as k-th operation
            is_kth = [True if machine_data[n][k] - 1 == i else False for n in range(n_machine)]
            I_bik[i, k] += sum(is_kth)
    I_b = np.subtract(I_bik, 1)
    I_b = I_b.clip(min=0)
    I_b = np.divide(I_b, n_job - 1)
    I_b = I_b.sum() / n_machine

    # Flowshop index
    I_fik = np.zeros((n_machine, n_machine))
    for n in range(n_job):
        for i in range(n_machine - 1):
            first = machine_data[n][i] - 1
            second = machine_data[n][i + 1] - 1
            I_fik[first, second] += 1
            # print('first job {0}, second job {1} for job {2}'.format(first, second, n))
    I_f = np.subtract(I_fik, 1)
    I_f = I_f.clip(min=0)
    I_f = np.divide(I_f, n_job - 1)
    I_f = I_f.sum() / (n_machine - 1)

    # filename = (prefix + str(num_job) + str(num_machine) +
    #             '_' + str(round(I_b, 3)) + '_' + str(round(I_f, 3)) + '.txt')
    filename = (prefix + str(num_job) + str(num_machine) +
                '_' + str(instance).zfill(3) + '.txt')
    print(f'Bottleneck Index:{round(I_b, 4)}, Flowshop Index:{round(I_f, 4)}')
    # 파일 작성
    with open(filename, 'w') as f:
        # 첫번째 줄 작성
        f.write(first_line + '\n')
        # 데이터프레임을 파일에 작성
        df.to_csv(f, sep='\t', index=False, header=False, lineterminator='\n')  # Updated lineterminator


def generate_flowshoplike_data(n_job, n_machine, probability, prefix, instance):
    first_line = f"{num_job}\t{num_machine}"
    df = pd.DataFrame(np.random.randint(11, 101, size=(num_job, num_machine)))
    machine_data = []

    for i in range(num_job):
        permutation = np.random.permutation(np.arange(1, num_machine + 1)).astype(int)
        for j in range(num_machine - 1):
            if random.random() < probability:  # modifying event occurred!
                # print('modifying event occurred!')
                # print('Original permutation:', permutation)
                first = permutation[j].copy()
                second = permutation[j + 1].copy()
                if (second != (first + 1)) & (first != n_machine):
                    idx = np.where(permutation == (first + 1))
                    permutation[j + 1] = first + 1
                    permutation[idx] = second
                # print('Modified permutation:', permutation)
                # print('-' * 30)
        machine_data.append(permutation.tolist())
        df.loc[df.shape[0]] = permutation

    # Bottleneck Index
    I_bik = np.zeros((n_machine, n_machine))
    for i in range(n_machine):  # machine i
        for k in range(n_machine):  # appears as k-th operation
            is_kth = [True if machine_data[n][k]-1 == i else False for n in range(n_machine)]
            I_bik[i, k] += sum(is_kth)
    I_b = np.subtract(I_bik, 1)
    I_b = I_b.clip(min=0)
    I_b = np.divide(I_b, n_job - 1)
    I_b = I_b.sum() / n_machine

    # Flowshop index
    I_fik = np.zeros((n_machine, n_machine))
    for n in range(n_job):
        for i in range(n_machine - 1):
            first = machine_data[n][i]-1
            second = machine_data[n][i + 1]-1
            I_fik[first, second] += 1
            # print('first job {0}, second job {1} for job {2}'.format(first, second, n))
    I_f = np.subtract(I_fik, 1)
    I_f = I_f.clip(min=0)
    I_f = np.divide(I_f, n_job - 1)
    I_f = I_f.sum() / (n_machine - 1)

    # filename = (prefix + str(num_job) + str(num_machine) +
    #             '_' + str(round(I_b, 3)) + '_' + str(round(I_f, 3)) + '.txt')
    filename = (prefix + str(num_job) + str(num_machine) +
                '_' + str(instance).zfill(3) + '.txt')
    print(f'Bottleneck Index:{round(I_b,4)}, Flowshop Index:{round(I_f,4)}')
    # 파일 작성
    with open(filename, 'w') as f:
        # 첫번째 줄 작성
        f.write(first_line + '\n')
        # 데이터프레임을 파일에 작성
        df.to_csv(f, sep='\t', index=False, header=False, lineterminator='\n')  # Updated lineterminator


if __name__ == "__main__":
    num_job = 20
    num_machine = 20
    # generate_JSSP_data(num_job, num_machine, './Dataset/test_')
    for i in range(100):
        generate_flowshoplike_data(num_job, num_machine, 0.01*i,'./Dataset/APMS/FS_', i+1)
        generate_bottleneckshop_data(num_job, num_machine, 0.01*i,'./Dataset/APMS/BS_', i+1)
    print()

# Assuming show_machine_distribution and show_pt_distribution are defined elsewhere
# show_machine_distribution(dataset)
# show_pt_distribution(dataset)
