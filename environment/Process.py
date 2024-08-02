"""
Process Class for Simulation

This script defines the Process class, which models a manufacturing process 
within a simulation environment using the SimPy library. The Process class 
handles the working, dispatching, and routing of parts through different 
machines and processes.

Classes:
    Process: A class to represent a manufacturing process in a simulation.

Functions:
    work: Simulates the working process on a machine.
    dispatch: Handles the dispatching of parts to be processed.
    check_item: Checks if the next part in the queue is ready for processing.
    routing: Routes parts to the next process or sink.
"""

import simpy
from .Monitor import Monitor

class Process(object):
    """
    Represents a manufacturing process in a simulation.
    
    Attributes:
        config: Configuration object with simulation settings.
        env: The simulation environment.
        name (str): The name of the process.
        model: The simulation model containing machines and processes.
        monitor: Monitor object for recording events.
        machine_order: Order of machines for processing parts.
        parts_sent (int): Number of parts sent for processing.
        scheduled (int): Number of parts scheduled for processing.
        in_part: Store for parts entering the process.
        part_ready: Store for parts ready for processing.
        out_part: Store for parts exiting the process.
        input_event: Event signaling a new input part.
        ready_event: Event signaling a part is ready for processing.
        route_ready: Event signaling a part is ready for routing.
    """

    def __init__(self, _env, _name, _model, _monitor, _machine_order, config):
        """
        Initializes the Process class with the specified parameters.
        
        Parameters:
            _env: The simulation environment.
            _name (str): The name of the process.
            _model: The simulation model containing machines and processes.
            _monitor: Monitor object for recording events.
            _machine_order: Order of machines for processing parts.
            config: Configuration object with simulation settings.
        """
        self.config = config
        self.env = _env
        self.name = _name
        self.model = _model
        self.monitor = _monitor
        self.machine_order = _machine_order
        self.parts_sent = 0
        self.scheduled = 0

        self.in_part = simpy.FilterStore(_env)
        self.part_ready = simpy.FilterStore(_env)
        self.out_part = simpy.FilterStore(_env)
        self.input_event = simpy.Event(_env)
        self.ready_event = simpy.Event(_env)
        self.route_ready = simpy.Event(_env)

        _env.process(self.work())
        _env.process(self.routing())
        _env.process(self.dispatch())

    def work(self):
        """
        Simulates the working process on a machine.
        """
        while True:
            part = yield self.part_ready.get()
            operation = part.op[part.step]
            yield operation.requirements

            if isinstance(operation.machine, list):
                machine = operation.machine[0]
                process_time = operation.process_time[0]
            else:
                machine = self.model['M' + str(operation.machine)]
                process_time = operation.process_time

            yield machine.availability.put('using')
            machine.add_reference(operation)

            # Logging the 'Started' event
            try:
                self.monitor.record(self.env.now, self.name, machine='M' + str(operation.machine),
                                    part_name=part.name, event="Started")
            except Exception as e:
                print(f"Error logging 'Started' event: {e}")

            yield self.env.timeout(process_time)

            # Logging the 'Finished' event
            try:
                self.monitor.record(self.env.now, self.name, machine='M' + str(operation.machine),
                                    part_name=part.name, event="Finished")
            except Exception as e:
                print(f"Error logging 'Finished' event: {e}")

            machine.util_time += process_time
            self.input_event.succeed()

            yield self.out_part.put(part)
            yield machine.availability.get()

    def dispatch(self):
        """
        Handles the dispatching of parts to be processed.
        """
        while True:
            yield self.input_event
            self.input_event = simpy.Event(self.env)
            if self.config.dispatch_mode == 'FIFO':
                part_ready = yield self.in_part.get()
                yield self.part_ready.put(part_ready)
            elif self.config.dispatch_mode == 'Manual':
                num_scan = len(self.in_part.items)
                for i in range(num_scan):
                    if self.check_item():
                        part_ready = yield self.in_part.get(lambda x: x.part_type == self.machine_order[self.scheduled])
                        yield self.part_ready.put(part_ready)
                        self.scheduled += 1

    def check_item(self):
        """
        Checks if the next part in the queue is ready for processing.
        
        Returns:
            bool: True if the part is ready, False otherwise.
        """
        for i, item in enumerate(self.in_part.items):
            if item.part_type == self.machine_order[self.scheduled]:
                return True
        return False

    def routing(self):
        """
        Routes parts to the next process or sink.
        """
        while True:
            part = yield self.out_part.get()
            if part.step != (self.config.n_machine - 1):
                part.step += 1
                part.op[part.step].requirements.succeed()
                next_process = self.model['Process' + str(part.op[part.step].process_type)]
                yield next_process.in_part.put(part)
                next_process.input_event.succeed()
                next_process.input_event = simpy.Event(self.env)
                part.loc = next_process.name
            else:
                self.model['Sink'].put(part)
