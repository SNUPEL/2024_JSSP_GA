"""
Distance and Correlation Functions

This script defines several functions to calculate distances and correlations 
between two sequences. These include Kendall's tau distance, Spearman's rank 
correlation, Spearman's footrule distance, bubble sort distance, positional 
distance, and mean squared error (MSE).

Functions:
    kendall_tau_distance(x, y): Calculates Kendall's tau distance between two sequences.
    spearman_rank_correlation(x, y): Calculates Spearman's rank correlation between two sequences.
    spearman_footrule_distance(x, y): Calculates Spearman's footrule distance between two sequences.
    bubble_sort_distance(x): Calculates the bubble sort distance for a sequence.
    positional_distance(x, y): Calculates the positional distance between two sequences.
    MSE(x, y): Calculates the mean squared error (MSE) between two sequences.
"""

import numpy as np
from scipy.stats import kendalltau, spearmanr

def kendall_tau_distance(x, y):
    """
    Calculates Kendall's tau distance between two sequences.
    
    Parameters:
        x (list or array): The first sequence.
        y (list or array): The second sequence.
    
    Returns:
        float: Kendall's tau distance.
    """
    tau, _ = kendalltau(x, y)
    return tau

def spearman_rank_correlation(x, y):
    """
    Calculates Spearman's rank correlation between two sequences.
    
    Parameters:
        x (list or array): The first sequence.
        y (list or array): The second sequence.
    
    Returns:
        float: Spearman's rank correlation coefficient.
    """
    rho, _ = spearmanr(x, y)
    return rho

def spearman_footrule_distance(x, y):
    """
    Calculates Spearman's footrule distance between two sequences.
    
    Parameters:
        x (list or array): The first sequence.
        y (list or array): The second sequence.
    
    Returns:
        float: Spearman's footrule distance.
    """
    distance = np.sum(np.abs(np.argsort(x) - np.argsort(y)))
    return distance

def bubble_sort_distance(x):
    """
    Calculates the bubble sort distance for a sequence.
    
    Parameters:
        x (list or array): The sequence to be sorted.
    
    Returns:
        int: The bubble sort distance.
    """
    n = len(x)
    sorted_x = np.sort(x)
    distance = np.sum(np.where(x != sorted_x)[0])
    return distance

def positional_distance(x, y):
    """
    Calculates the positional distance between two sequences.
    
    Parameters:
        x (list or array): The first sequence.
        y (list or array): The second sequence.
    
    Returns:
        int: The positional distance.
    """
    distance = np.sum(np.abs(np.where(x != y)[0] - np.where(x != y)[0]))
    return distance

def MSE(x, y):
    """
    Calculates the mean squared error (MSE) between two sequences.
    
    Parameters:
        x (list or array): The first sequence.
        y (list or array): The second sequence.
    
    Returns:
        float: The mean squared error.
    """
    # 2차원 리스트를 NumPy 배열로 변환
    x = np.array(x)
    y = np.array(y)

    # 각 원소 간의 평균 제곱 오차 계산
    mse = np.square(np.subtract(x, y)).mean()

    return mse
