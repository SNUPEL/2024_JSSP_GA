"""
Operation and Job Classes

This script defines the Operation and Job classes, which are used to model operations
and jobs in a job shop scheduling problem.

Classes:
    Operation: A class to represent an operation within a job.
    Job: A class to represent a job consisting of multiple operations.
"""

# region Operation
class Operation(object):
    """
    Represents an operation within a job.
    
    This class does not act as a process. Instead, it is a member variable of a job 
    that contains process info. This class is only used when generating a job sequence.
    
    Attributes:
        env: The simulation environment.
        id (int): The ID of the operation.
        part_name (str): The name of the part.
        process_type (int): The type of the process.
        machine (int): The machine type for the operation.
        process_time (float): The processing time for the operation.
        requirements: The preceding event requirements.
    """
    
    def __init__(self, env, id, part_name, process_type, machine, process_time, requirements=None):
        """
        Initializes the Operation class with the specified parameters.
        
        Parameters:
            env: The simulation environment.
            id (int): The ID of the operation.
            part_name (str): The name of the part.
            process_type (int): The type of the process.
            machine (int): The machine type for the operation.
            process_time (float): The processing time for the operation.
            requirements: The preceding event requirements (default is None).
        """
        self.id = id
        self.process_type = process_type
        self.process_time = process_time
        self.part_name = part_name
        self.name = part_name + '_Op' + str(id)

        # In the simplest Job Shop problem, process type often coincides with the machine type itself.
        self.machine = machine
        if requirements is None:
            self.requirements = env.event()  # preceding event
            if id == 0:
                self.requirements.succeed()
        else:
            # if there are more requirements, more env.event() can be added up
            # you can handle events using Simpy.AllOf() or Simpy.AnyOf()
            self.requirements = [env.event() for i in range(5)]  # This is an arbitrary value

# endregion

# region Job
class Job(object):
    """
    Represents a job consisting of multiple operations.
    
    A job is repeatedly generated in a source. For example:
    (Job1_1, Job1_2, Job1_3, ..., Job1_100,
    Job2_1, Job2_2, Job2_3, ..., Job2_100,
    ...                         Job10_100)
    
    Attributes:
        env: The simulation environment.
        part_type (int): The type of the part.
        id (int): The ID of the job.
        name (str): The name of the part.
        step (int): The current step in the job's operation sequence.
        loc: The current location of the job.
        op (list): The list of operations for the job.
    """
    
    def __init__(self, env, part_type, id, op_data):
        """
        Initializes the Job class with the specified parameters.
        
        Parameters:
            env: The simulation environment.
            part_type (int): The type of the part.
            id (int): The ID of the job.
            op_data (list): The operation data for the job.
        """
        self.part_type = part_type
        self.id = id
        self.name = 'Part' + str(part_type) + '_' + str(id)
        self.step = -1
        self.loc = None  # current location
        self.op = [Operation(env,
                             id=j, part_name=self.name,
                             process_type=op_data[part_type][j][0],
                             machine=op_data[part_type][j][0],
                             process_time=op_data[part_type][j][1],
                             requirements=None) for j in range(len(op_data[part_type]))]

# endregion Job
