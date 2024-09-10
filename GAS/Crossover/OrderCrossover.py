import random
import copy

class OrderCrossover:
    def __init__(self, pc, min_crossover_size=0.1, max_crossover_size=0.3):
        self.pc = pc
        self.min_crossover_size = min_crossover_size
        self.max_crossover_size = max_crossover_size

    def cross(self, parent1, parent2):
        # print(f"Starting crossover between:\nParent1: {parent1.seq}\nParent2: {parent2.seq}")
        if random.random() > self.pc:
            print("Crossover did not occur, parents copied directly.")
            return copy.deepcopy(parent1), copy.deepcopy(parent2)

        size = len(parent1.seq)
        crossover_size = random.uniform(self.min_crossover_size, self.max_crossover_size)
        crossover_length = int(size * crossover_size)
        
        start = random.randint(0, size - crossover_length)
        end = start + crossover_length

        def create_child(p1, p2):
            child_seq = [None] * size
            child_seq[start:end] = p1.seq[start:end]
            
            remaining = [item for item in p2.seq if item not in child_seq[start:end]]
            for i in list(range(0, start)) + list(range(end, size)):
                child_seq[i] = remaining.pop(0)

            child = copy.deepcopy(p1)
            child.seq = child_seq
            return child

        child1 = create_child(parent1, parent2)
        child2 = create_child(parent2, parent1)

        # Validation and Debugging Output
        # print(f"Parent1: {parent1.seq}")
        # print(f"Parent2: {parent2.seq}")
        # print(f"Child1: {child1.seq}")
        # print(f"Child2: {child2.seq}")

        return child1, child2