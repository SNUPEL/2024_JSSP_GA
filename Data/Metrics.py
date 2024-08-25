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
            print('first job {0}, second job {1} for job {2}'.format(first, second, n))

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
    from Dataset.Dataset import Dataset

    d = Dataset('ft06.txt')
    I_b = calculate_bottleneck_index(d)
    I_f = calculate_flowshop_index(d)
    print()
