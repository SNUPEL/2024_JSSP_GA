"""
Resource Classes for Simulation

This script defines the Machine, Worker, and Jig classes, which model different 
resources within a simulation environment using the SimPy library.

Classes:
    Machine: A class to represent a machine in the simulation.
    Worker: A class to represent a worker in the simulation.
    Jig: A class to represent a jig in the simulation.
"""

import simpy

class Machine(object):
    """
    Represents a machine in the simulation.
    
    Attributes:
        env: The simulation environment.
        id (int): The ID of the machine.
        capacity (int): The capacity of the machine (default is 1).
        availability: SimPy store to manage machine availability.
        workingtime_log (list): Log of working times.
        util_time (float): Total utilization time of the machine.
        op_where (list): List of operation IDs processed by the machine.
    """
    
    def __init__(self, env, id):
        """
        Initializes the Machine class with the specified parameters.
        
        Parameters:
            env: The simulation environment.
            id (int): The ID of the machine.
        """
        self.env = env
        self.id = id
        self.capacity = 1
        self.availability = simpy.Store(env, capacity=self.capacity)
        self.workingtime_log = []
        self.util_time = 0.0
        self.op_where = []

    def add_reference(self, op):
        """
        Adds a reference to the operation processed by the machine.
        
        Parameters:
            op: The operation being processed.
        """
        self.op_where.append(op.id)  # 기록한 op가 몇 번째였는지를 기록


class Worker(object):
    """
    Represents a worker in the simulation.
    
    Attributes:
        env: The simulation environment.
        id (int): The ID of the worker.
        capacity (int): The capacity of the worker (default is 1).
        availability: SimPy store to manage worker availability.
        workingtime_log (list): Log of working times.
        util_time (float): Total utilization time of the worker.
    """
    
    def __init__(self, env, id):
        """
        Initializes the Worker class with the specified parameters.
        
        Parameters:
            env: The simulation environment.
            id (int): The ID of the worker.
        """
        self.env = env
        self.id = id
        self.capacity = 1
        self.availability = simpy.Store(env, capacity=self.capacity)
        self.workingtime_log = []
        self.util_time = 0.0


class Jig(object):
    """
    Represents a jig in the simulation.
    
    Attributes:
        env: The simulation environment.
        id (int): The ID of the jig.
        capacity (int): The capacity of the jig (default is 1).
        availability: SimPy store to manage jig availability.
        workingtime_log (list): Log of working times.
        util_time (float): Total utilization time of the jig.
    """
    
    def __init__(self, env, id):
        """
        Initializes the Jig class with the specified parameters.
        
        Parameters:
            env: The simulation environment.
            id (int): The ID of the jig.
        """
        self.env = env
        self.id = id
        self.capacity = 1
        self.availability = simpy.Store(env, capacity=self.capacity)
        self.workingtime_log = []
        self.util_time = 0.0
