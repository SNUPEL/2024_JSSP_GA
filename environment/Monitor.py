"""
Monitor and Console Output

This script defines the Monitor class, which is used to record and save events during
a simulation, and functions to print events to the console based on different modes.

Classes:
    Monitor: A class to monitor and save events during the simulation.

Functions:
    monitor_by_console: Prints events to the console based on the mode.
    print_by_machine: Prints the current state of the machine to the console.
"""

import pandas as pd

# region Monitor
class Monitor(object):
    """
    A class to monitor and save events during the simulation.
    
    Attributes:
        config: Configuration object with simulation settings.
        time (list): List to store event times.
        event (list): List to store event types.
        part (list): List to store part names.
        process_name (list): List to store process names.
        machine_name (list): List to store machine names.
    """
    
    def __init__(self, config):
        """
        Initializes the Monitor class with the given configuration.
        
        Parameters:
            config: Configuration object with simulation settings.
        """
        self.config = config  # Event tracer 저장 경로
        self.time = []
        self.event = []
        self.part = []
        self.process_name = []
        self.machine_name = []

    def record(self, time, process, machine, part_name=None, event=None):
        """
        Records an event with the given parameters.
        
        Parameters:
            time: The time of the event.
            process: The name of the process.
            machine: The name of the machine.
            part_name: The name of the part (default is None).
            event: The type of event (default is None).
        """
        if time is not None and process is not None and machine is not None:
            self.time.append(time)
            self.event.append(event)
            self.part.append(part_name)  # string
            self.process_name.append(process)
            self.machine_name.append(machine)

    def save_event_tracer(self, file_path=None):
        """
        Saves the recorded events to a CSV file.
        
        Parameters:
            file_path: The path to save the CSV file (default is None).
        
        Returns:
            event_tracer: A DataFrame containing the recorded events.
        """
        event_tracer = pd.DataFrame({
            'Time': self.time,
            'Event': self.event,
            'Part': self.part,
            'Process': self.process_name,
            'Machine': self.machine_name
        })
        if self.config.save_log:
            if file_path:
                event_tracer.to_csv(file_path, index=False)
            else:
                event_tracer.to_csv(self.config.filename['log'], index=False)

        return event_tracer
# endregion

def monitor_by_console(console_mode, env, part, object='Single Part', command=''):
    """
    Prints events to the console based on the console mode.
    
    Parameters:
        console_mode (bool): Flag to print to the console.
        env: The simulation environment.
        part: The part being processed.
        object (str): The mode of monitoring (default is 'Single Part').
        command (str): Additional command to be printed (default is '').
    """
    if console_mode:
        operation = part.op[part.step]
        command = f" {command} "
        if object == 'Single Part' and operation.process_type == 0:
            pass
        elif object == 'Single Job' and operation.part_name == 'Part0_0':
            pass
        elif object == 'Entire Process':
            pass
        elif object == 'Machine':
            print_by_machine(env, part)

def print_by_machine(env, part):
    """
    Prints the current state of the machine to the console.
    
    Parameters:
        env: The simulation environment.
        part: The part being processed.
    """
    machine_idx = part.op[part.step].machine
    machine_positions = ["\t\t\t\t", "\t\t\t\t\t\t\t", "\t\t\t\t\t\t\t\t\t\t", "\t\t\t\t\t\t\t\t\t\t\t\t\t", "\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t"]
    if 0 <= machine_idx < len(machine_positions):
        print(f"{env.now}{machine_positions[machine_idx]}{part.op[part.step].name}")
    else:
        print()
