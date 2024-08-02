"""
Sink Class for Simulation

This script defines the Sink class, which models the final destination for parts
in a simulation environment using the SimPy library. The Sink class records the
completion of parts and monitors the simulation process.

Classes:
    Sink: A class to represent the final destination for parts in the simulation.

Functions:
    put: Records the arrival of parts at the sink and logs the completion event.
"""

import simpy
from .Monitor import monitor_by_console

# region Sink
class Sink(object):
    """
    Represents the final destination for parts in the simulation.
    
    Attributes:
        env: The simulation environment.
        name (str): The name of the sink.
        monitor: Monitor object for recording events.
        parts_rec (int): Number of parts received by the sink.
        last_arrival (float): Time when the last part arrived at the sink.
        config: Configuration object with simulation settings.
    """
    
    def __init__(self, env, monitor, config):
        """
        Initializes the Sink class with the specified parameters.
        
        Parameters:
            env: The simulation environment.
            monitor: Monitor object for recording events.
            config: Configuration object with simulation settings.
        """
        self.env = env
        self.name = 'Sink'
        self.monitor = monitor

        # Number of parts completed through the Sink
        self.parts_rec = 0
        # Time when the last part arrived
        self.last_arrival = 0.0
        self.config = config

    def put(self, part):
        """
        Records the arrival of parts at the sink and logs the completion event.
        
        Parameters:
            part: The part that has arrived at the sink.
        """
        self.parts_rec += 1
        self.last_arrival = self.env.now
        monitor_by_console(self.config.print_console, self.env, part, self.config.trace_object, "Completed on")
        self.monitor.record(self.env.now, self.name, machine=None,
                            part_name=part.name, event="Completed")

        if self.parts_rec == self.config.n_job:
            self.last_arrival = self.env.now
            # Optionally print or handle the event when all parts are finished
            # print(str(self.env.now))
            # print(str(self.env.now) + '\tAll Parts Finished')

# endregion
