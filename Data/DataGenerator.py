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


def generate_JSSP_data(num_job, num_machine, stats, prefix, seed=0):

    random.seed(seed)
    np.random.seed(seed)

    if stats['mode']=='Uniform':
        filename = prefix +'LB'+ str(stats['LB'])+'_UB'+str(stats['UB'])+'_' + str(num_job) + '_' + str(num_machine) + '_' + str(seed) + '.txt'

        df = pd.DataFrame(np.random.randint(stats['LB'], stats['UB'], size=(num_job, num_machine)))
    elif stats['mode'] == 'Normal':
        filename = prefix +'Mean'+ str(stats['mean'])+'_Std'+str(stats['std'])+'_' + str(num_job) + '_' + str(num_machine) + '_' + str(seed) + '.txt'
        # 평균과 표준편차를 따르는 정규분포에서 난수 생성 후 최소값 5로 제한, 정수로 변환
        # df = pd.DataFrame(
        #     np.maximum(
        #         5,
        #         np.random.normal(stats['mean'], stats['std'], size=(num_job, num_machine))
        #     ).astype(int)
        # )
        df = pd.DataFrame(
            np.maximum(
                5,
                np.random.normal(stats['mean'], stats['std'], size=(num_job, num_machine))
            ).astype(int)/10
        )
    else:
        raise Exception("Invalid mode")

    first_line = f"{num_job}\t{num_machine}"
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
    return filename

def generate_bottleneckshop_data(num_job, num_machine, stats, prefix, seed):
    first_line = f"{num_job}\t{num_machine}"
    if stats['mode']=='Uniform':
        df = pd.DataFrame(np.random.randint(stats['LB'], stats['UB'], size=(num_job, num_machine)))
    elif stats['mode'] == 'Normal':
        # 평균과 표준편차를 따르는 정규분포에서 난수 생성 후 최소값 5로 제한, 정수로 변환
        # df = pd.DataFrame(
        #     np.maximum(
        #         1,
        #         np.random.normal(stats['mean'], stats['std'], size=(num_job, num_machine))
        #     ).astype(int)
        # )
        df = pd.DataFrame(
            np.maximum(
                1,
                np.random.normal(stats['mean'], stats['std'], size=(num_job, num_machine))
            )
        )
    else:
        raise Exception("Invalid mode")
    machine_data = []

    for i in range(num_job):
        permutation = np.random.permutation(np.arange(1, num_machine + 1)).astype(int)
        for j in range(num_machine - 1):
            if random.random() < stats['prob']:  # modifying event occurred!
                # print('modifying event occurred!')
                # print('Original permutation:', permutation)
                target = permutation[j].copy() # j번째 자리에 들어있는 것은? (j+1 이어야 함)
                j_position = np.where(permutation==(j+1)) # 실제로 j가 들어있는 곳은?
                if (j_position != j):
                    permutation[j] = j+1
                    permutation[j_position] = target
                # print('Modified permutation:', permutation)
                # print('-' * 30)
        machine_data.append(permutation.tolist())
        df.loc[df.shape[0]] = permutation

    # Bottleneck Index
    I_bik = np.zeros((num_machine, num_machine))
    for i in range(num_machine):  # machine i
        for k in range(num_machine):  # appears as k-th operation
            is_kth = [True if machine_data[n][k] - 1 == i else False for n in range(num_machine)]
            I_bik[i, k] += sum(is_kth)
    I_b = np.subtract(I_bik, 1)
    I_b = I_b.clip(min=0)
    I_b = np.divide(I_b, num_job - 1)
    I_b = I_b.sum() / num_machine

    # Flowshop index
    I_fik = np.zeros((num_machine, num_machine))
    for n in range(num_job):
        for i in range(num_machine - 1):
            first = machine_data[n][i] - 1
            second = machine_data[n][i + 1] - 1
            I_fik[first, second] += 1
            # print('first job {0}, second job {1} for job {2}'.format(first, second, n))
    I_f = np.subtract(I_fik, 1)
    I_f = I_f.clip(min=0)
    I_f = np.divide(I_f, num_job - 1)
    I_f = I_f.sum() / (num_machine - 1)

    # filename = (prefix + str(num_job) + str(num_machine) +
    #             '_' + str(round(I_b, 3)) + '_' + str(round(I_f, 3)) + '.txt')
    filename = (prefix + '_'+str(num_job) + str(num_machine) +
                '_' + str(seed) + '.txt')
    print(f'Bottleneck Index:{round(I_b, 4)}, Flowshop Index:{round(I_f, 4)}')
    # 파일 작성
    with open(filename, 'w') as f:
        # 첫번째 줄 작성
        f.write(first_line + '\n')
        # 데이터프레임을 파일에 작성
        df.to_csv(f, sep='\t', index=False, header=False, lineterminator='\n')  # Updated lineterminator
    return filename

def generate_flowshoplike_data(num_job, num_machine, stats, prefix, seed=0):
    first_line = f"{num_job}\t{num_machine}"
    if stats['mode']=='Uniform':
        df = pd.DataFrame(np.random.randint(stats['LB'], stats['UB'], size=(num_job, num_machine)))
    elif stats['mode'] == 'Normal':
        # 평균과 표준편차를 따르는 정규분포에서 난수 생성 후 최소값 5로 제한, 정수로 변환
        df = pd.DataFrame(
            np.maximum(
                5,
                np.random.normal(stats['mean'], stats['std'], size=(num_job, num_machine))
            ).astype(int)
        )
    else:
        raise Exception("Invalid mode")
    machine_data = []

    for i in range(num_job):
        permutation = np.random.permutation(np.arange(1, num_machine + 1)).astype(int)
        for j in range(num_machine - 1):
            if random.random() < stats['prob']:  # modifying event occurred!
                # print('modifying event occurred!')
                # print('Original permutation:', permutation)
                first = permutation[j].copy()
                second = permutation[j + 1].copy()
                if (second != (first + 1)) & (first != num_machine):
                    idx = np.where(permutation == (first + 1))
                    permutation[j + 1] = first + 1
                    permutation[idx] = second
                # print('Modified permutation:', permutation)
                # print('-' * 30)
        machine_data.append(permutation.tolist())
        df.loc[df.shape[0]] = permutation

    # Bottleneck Index
    I_bik = np.zeros((num_machine, num_machine))
    for i in range(num_machine):  # machine i
        for k in range(num_machine):  # appears as k-th operation
            is_kth = [True if machine_data[n][k]-1 == i else False for n in range(num_machine)]
            I_bik[i, k] += sum(is_kth)
    I_b = np.subtract(I_bik, 1)
    I_b = I_b.clip(min=0)
    I_b = np.divide(I_b, num_job - 1)
    I_b = I_b.sum() / num_machine

    # Flowshop index
    I_fik = np.zeros((num_machine, num_machine))
    for n in range(num_job):
        for i in range(num_machine - 1):
            first = machine_data[n][i]-1
            second = machine_data[n][i + 1]-1
            I_fik[first, second] += 1
            # print('first job {0}, second job {1} for job {2}'.format(first, second, n))
    I_f = np.subtract(I_fik, 1)
    I_f = I_f.clip(min=0)
    I_f = np.divide(I_f, num_job - 1)
    I_f = I_f.sum() / (num_machine - 1)

    # filename = (prefix + str(num_job) + str(num_machine) +
    #             '_' + str(round(I_b, 3)) + '_' + str(round(I_f, 3)) + '.txt')
    filename = (prefix + '_'+str(num_job) + str(num_machine) +
                '_' + str(seed) + '.txt')
    print(f'Bottleneck Index:{round(I_b,4)}, Flowshop Index:{round(I_f,4)}')
    # 파일 작성
    with open(filename, 'w') as f:
        # 첫번째 줄 작성
        f.write(first_line + '\n')
        # 데이터프레임을 파일에 작성
        df.to_csv(f, sep='\t', index=False, header=False, lineterminator='\n')  # Updated lineterminator
    return filename

if __name__ == "__main__":
    num_job = 10
    num_machine = 10
    for i in range(10):
        for j in [1,2,3,4,5,6,7,8,9,10]:
            # stats = {'mode':'Uniform',
            #          'LB':10,
            #          'UB':40
            #          }
            stats = {'mode':'Normal',
                     'mean':30,
                     'std':j
                     }
            generate_JSSP_data(num_job, num_machine, stats, './Dataset/Normal/',seed=i)
    # for i in range(20):
    #     generate_flowshoplike_data(num_job, num_machine, 0.05*i,'./Dataset/FS_', i+1)
    #     generate_bottleneckshop_data(num_job, num_machine, 0.05*i,'./Dataset/BS_', i+1)
    # print()

# Assuming show_machine_distribution and show_pt_distribution are defined elsewhere
# show_machine_distribution(dataset)
# show_pt_distribution(dataset)
