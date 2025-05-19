from GAS.Individual import Individual
from Config.Run_Config import Run_Config
from baseline import baseline
from Data.Dataset.Dataset import Dataset
from GAS.Population import JSSP
import random

def comparison_report(ins, opt):
    instance = ins
    dataset = Dataset(instance)
    jssp = JSSP(dataset)
    config = Run_Config(n_job=dataset.n_job, n_machine=dataset.n_machine, n_op=dataset.n_op, population_size=100,
                        generations=1,
                        print_console=False, save_log=True, save_machinelog=True,
                        show_gantt=False, save_gantt=True, show_gui=False,
                        trace_object='Process4', title='Gantt Chart for JSSP',
                        tabu_search_iterations=10, hill_climbing_iterations=30, simulated_annealing_iterations=50,
                        two_iterations=1000, target_makespan=opt)
    RUBI_individuals = [Individual(config, seq=jssp.get_seq(), op_data=dataset.op_data) for i in range(10)]
    RUBI_list = [s.makespan for s in RUBI_individuals]
    Random_individuals = [Individual(config, seq=random.sample(range(config.n_op), config.n_op), op_data=dataset.op_data) for i in range(10)]
    Random_list = [s.makespan for s in Random_individuals]
    SPT_list = [baseline(dataset, "min") for i in range(10)]
    LPT_list = [baseline(dataset, "max") for i in range(10)]
    print('-'*15 + ins, f'(Optimal:{opt})', '-'*15)
    print(RUBI_list)
    print(Random_list)
    print(SPT_list)
    print(LPT_list)

if __name__ == '__main__':
    directories = ['abz5.txt'
                   ]
    optimal = [None for i in range(len(directories))]
    # directories = ['la01.txt',
    #                'la02.txt',
    #                'la03.txt',
    #                'la04.txt',
    #                'la05.txt',
    #                'la06.txt',
    #                'la07.txt',
    #                'la08.txt',
    #                'la09.txt',
    #                'la10.txt',
    #                'la11.txt',
    #                'la12.txt',
    #                'la13.txt',
    #                'la14.txt',
    #                'la15.txt',
    #                'la16.txt',
    #                'la17.txt',
    #                'la18.txt',
    #                'la19.txt',
    #                'la20.txt']
    # optimal = [666, 655, 597, 590, 593, 926, 890, 863, 951, 958,
    #            1222, 1039, 1150, 1292, 1207, 945, 784, 848, 842, 902]
    for ins, opt in zip(directories, optimal):
        comparison_report(ins, opt)
