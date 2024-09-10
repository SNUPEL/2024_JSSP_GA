import random
import copy

class SeedSelection:
    def __init__(self):
        pass

    def select(self, population):
        # population을 makespan을 기준으로 정렬 (makespan이 작을수록 좋음)
        sorted_population = sorted(population, key=lambda ind: ind.makespan)

        # 가장 좋은 개체를 best_individual로 선택
        best_individual = sorted_population[0]

        # 확률적으로 best_individual 또는 다른 개체 선택
        if random.random() < 0.5:  # 50% 확률로 best_individual 선택
            return copy.deepcopy(best_individual)
        else:
            # 나머지 50% 확률로 다른 개체 무작위 선택
            other_individuals = sorted_population[1:]
            if other_individuals:
                return copy.deepcopy(random.choice(other_individuals))
            else:
                return copy.deepcopy(best_individual)