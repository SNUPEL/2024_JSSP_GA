import random
import copy

class PMXCrossover:
    def __init__(self, pc, min_crossover_size=0.1, max_crossover_size=0.3):
        self.pc = pc
        self.min_crossover_size = min_crossover_size
        self.max_crossover_size = max_crossover_size

    def get_job_index(self, index, num_jobs):
        # 주어진 index의 operation이 어느 job에 속하는지 계산 (Job 수로 나눔)
        return index // num_jobs

    def cross(self, parent1, parent2):
        num_jobs = parent1.config.n_job  # Job 수 가져오기
        
        if random.random() > self.pc:
            return copy.deepcopy(parent1), copy.deepcopy(parent2)

        size = len(parent1.seq)

        # Determine crossover size
        crossover_size = random.uniform(self.min_crossover_size, self.max_crossover_size)
        segment_size = max(2, int(size * crossover_size))  # 최소 교차 길이를 2로 설정
        
        # Randomly select the start point of the segment
        point1 = random.randint(0, size - segment_size)
        point2 = point1 + segment_size

        def pmx_one_offspring(p1, p2):
            offspring = [None] * size
            
            # Copy the segment from parent1
            offspring[point1:point2] = p1[point1:point2]
            
            # Map the segment from parent2 to parent1
            for i in range(point1, point2):
                if p2[i] not in offspring:
                    pos = p2.index(p1[i])
                    while offspring[pos] is not None:
                        pos = p2.index(p1[pos])
                    offspring[pos] = p2[i]

            # Fill in the remaining positions
            for i in range(size):
                if offspring[i] is None:
                    # Ensure jobs do not swap operations from different jobs
                    if self.get_job_index(i, num_jobs) == self.get_job_index(p2.index(p2[i]), num_jobs):
                        offspring[i] = p2[i]
                    else:
                        offspring[i] = p1[i]

            return offspring

        child1_seq = pmx_one_offspring(parent1.seq, parent2.seq)
        child2_seq = pmx_one_offspring(parent2.seq, parent1.seq)

        child1 = copy.deepcopy(parent1)
        child2 = copy.deepcopy(parent2)
        child1.seq = child1_seq
        child2.seq = child2_seq

        # Validation and Debugging Output
        assert len(child1_seq) == size, f"Child1 sequence length mismatch: {len(child1_seq)} != {size}"
        assert len(child2_seq) == size, f"Child2 sequence length mismatch: {len(child2_seq)} != {size}"
        assert len(set(child1_seq)) == size, f"Child1 has duplicate genes: {child1_seq}"
        assert len(set(child2_seq)) == size, f"Child2 has duplicate genes: {child2_seq}"

        return child1, child2
