"""
PSO Class

This script defines the PSO (Particle Swarm Optimization) class, which implements 
the particle swarm optimization algorithm for local search optimization in genetic 
algorithms. The class iteratively improves the job sequence by adjusting the 
positions and velocities of particles to minimize the makespan.

Classes:
    PSO: A class to perform particle swarm optimization.

Functions:
    optimize(individual, config): Optimizes the job sequence using PSO.
    create_new_individual(individual, new_seq, config): Creates a new individual with the optimized sequence.
    ensure_valid_sequence(seq, config): Ensures that the job sequence is valid.
"""

import copy
import random
import numpy as np

class PSO:
    """
    Implements the particle swarm optimization (PSO) algorithm for local search optimization.
    
    Attributes:
        num_particles (int): The number of particles in the swarm.
        num_iterations (int): The number of iterations to perform.
        w (float): The inertia coefficient.
        c1 (float): The cognitive coefficient (personal best).
        c2 (float): The social coefficient (global best).
    """
    
    def __init__(self, num_particles=30, num_iterations=100, w=0.7, c1=1.5, c2=1.5):
        """
        Initializes the PSO class with the specified parameters.
        
        Parameters:
            num_particles (int): The number of particles (default is 30).
            num_iterations (int): The number of iterations (default is 100).
            w (float): The inertia coefficient (default is 0.7).
            c1 (float): The cognitive coefficient (default is 1.5).
            c2 (float): The social coefficient (default is 1.5).
        """
        self.num_particles = num_particles
        self.num_iterations = num_iterations
        self.w = w  # 관성 계수
        self.c1 = c1  # 개인 최적 위치로 이동하는 계수
        self.c2 = c2  # 전체 최적 위치로 이동하는 계수

    def optimize(self, individual, config):
        """
        Optimizes the job sequence using particle swarm optimization.
        
        Parameters:
            individual (Individual): The individual to optimize.
            config: Configuration object with simulation settings.
        
        Returns:
            Individual: The optimized individual.
        """
        print("PSO 시작")
        particles = [self.create_new_individual(individual, individual.seq, config) for _ in range(self.num_particles)]
        velocities = [np.random.uniform(-1, 1, len(individual.seq)) for _ in range(self.num_particles)]
        personal_best_positions = [copy.deepcopy(p.seq) for p in particles]
        personal_best_fitness = [p.fitness for p in particles]
        
        global_best_particle = min(particles, key=lambda p: p.fitness)
        global_best_position = global_best_particle.seq[:]
        global_best_fitness = global_best_particle.fitness

        for iteration in range(self.num_iterations):
            for i in range(self.num_particles):
                r1 = random.random()
                r2 = random.random()
                
                velocities[i] = (self.w * velocities[i] +
                                 self.c1 * r1 * (np.array(personal_best_positions[i]) - np.array(particles[i].seq)) +
                                 self.c2 * r2 * (np.array(global_best_position) - np.array(particles[i].seq)))
                velocities[i] = np.clip(velocities[i], -1, 1)
                
                new_seq = (np.array(particles[i].seq) + velocities[i]).astype(int).tolist()
                new_seq = self.ensure_valid_sequence(new_seq, config)

                # 새로운 개체 생성 및 평가
                new_individual = self.create_new_individual(particles[i], new_seq, config)
                new_individual.calculate_fitness(config.target_makespan)

                # Personal best 업데이트
                if new_individual.fitness < personal_best_fitness[i]:
                    personal_best_positions[i] = new_individual.seq[:]
                    personal_best_fitness[i] = new_individual.fitness

                # Global best 업데이트
                if new_individual.fitness < global_best_fitness:
                    global_best_particle = copy.deepcopy(new_individual)
                    global_best_position = new_individual.seq[:]
                    global_best_fitness = new_individual.fitness

                # 파티클 업데이트
                particles[i] = new_individual

            current_best_particle = min(particles, key=lambda p: p.fitness)
            current_best_fitness = current_best_particle.fitness

            for i, p in enumerate(particles):
                print(f"Particle {i}: Sequence = {p.seq}, Makespan = {p.makespan}, Fitness = {p.fitness}")

        print("PSO 종료")
        return global_best_particle

    def create_new_individual(self, individual, new_seq, config):
        """
        Creates a new individual with the optimized sequence.
        
        Parameters:
            individual (Individual): The original individual.
            new_seq (list): The optimized job sequence.
            config: Configuration object with simulation settings.
        
        Returns:
            Individual: The new individual with the optimized sequence.
        """
        new_individual = copy.deepcopy(individual)
        new_individual.seq = new_seq
        new_individual.job_seq = new_individual.get_repeatable()
        new_individual.feasible_seq = new_individual.get_feasible()
        new_individual.machine_order = new_individual.get_machine_order()
        new_individual.makespan, new_individual.mio_score = new_individual.evaluate(new_individual.machine_order)
        new_individual.calculate_fitness(config.target_makespan)
        return new_individual

    def ensure_valid_sequence(self, seq, config):
        """
        Ensures that the job sequence is valid.
        
        Parameters:
            seq (list): The job sequence.
            config: Configuration object with simulation settings.
        
        Returns:
            list: The valid job sequence.
        """
        num_jobs = config.n_job
        num_machines = config.n_machine
        job_counts = {job: 0 for job in range(num_jobs)}
        valid_seq = []

        for operation in seq:
            job = operation // num_machines
            if job_counts[job] < num_machines:
                valid_seq.append(job * num_machines + job_counts[job])
                job_counts[job] += 1

        for job in range(num_jobs):
            while job_counts[job] < num_machines:
                valid_seq.append(job * num_machines + job_counts[job])
                job_counts[job] += 1

        return valid_seq
