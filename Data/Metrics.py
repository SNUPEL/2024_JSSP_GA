"""
calculate bottleneck indices and flowshop indices of the given problem instance
"""

import numpy as np


def calculate_flowshop_index(dataset):
    """

    Args:
        dataset: Dataset class instance

    Returns:
        I_f : float value between 0 and 1 (1 for a complete flowshop problem)
    """
    I_ik = np.zeros((dataset.n_machine, dataset.n_machine))

    for n in range(dataset.n_job):
        for i in range(dataset.n_machine - 1):
            first = dataset.machine_data[n][i]
            second = dataset.machine_data[n][i + 1]
            I_ik[first, second] += 1
            # print('first job {0}, second job {1} for job {2}'.format(first, second, n))

    I_f = np.subtract(I_ik, 1)
    I_f = I_f.clip(min=0)
    I_f = np.divide(I_f, dataset.n_job - 1)
    I_f = I_f.sum() / (dataset.n_machine - 1)
    return I_f


def calculate_bottleneck_index(dataset):
    """

    Args:
        dataset:

    Returns:

    """
    I_ik = np.zeros((dataset.n_machine, dataset.n_machine))
    for i in range(dataset.n_machine):  # machine i
        for k in range(dataset.n_machine):  # appears as k-th operation
            is_kth = [True if dataset.op_data[n][k][0] == i else False for n in range(dataset.n_machine)]
            I_ik[i, k] += sum(is_kth)

    I_b = np.subtract(I_ik, 1)
    I_b = I_b.clip(min=0)
    I_b = np.divide(I_b, dataset.n_job - 1)
    I_b = I_b.sum() / dataset.n_machine
    return I_b


if __name__ == "__main__":
    # from Dataset import Dataset
    from Dataset.Dataset import Dataset
    import os, csv
    # d = Dataset('la01.txt')
    # I_b = calculate_bottleneck_index(d)
    # I_f = calculate_flowshop_index(d)
    # print(I_b, I_f)

    output_dir = './Outputs'

    root_dir = './Dataset/APMS'
    directories=[]
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.txt'):
                directories.append('APMS/'+file)
                # directories.append(os.path.join(root, file))

    # CSV 파일 생성
    csv_filename = "Analysis.csv"
    with open(csv_filename, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Index", "Filename", "n_job","n_machine","Bottleneck_Index", "Flowshop_Index"])  # 헤더 작성

        for index, file in enumerate(directories):
            d = Dataset(file)  # 파일을 Dataset 객체로 변환
            I_b = calculate_bottleneck_index(d)
            I_f = calculate_flowshop_index(d)
            writer.writerow([index, file, d.n_job, d.n_machine, round(I_b,4), round(I_f,4)])

    print(f"CSV 파일이 생성되었습니다: {csv_filename}")

