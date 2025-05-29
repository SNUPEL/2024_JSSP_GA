from Data.Dataset.Dataset import Dataset
from baseline import GifflerandThompson, baseline

if __name__ == '__main__':
    from GAS.Individual import Individual
    from Config.Run_Config import Run_Config
    from GAS.Population import JSSP
    instance = 'la01.txt'
    dataset = Dataset(instance)
    seq = GifflerandThompson(dataset)
    print(seq)
    jssp = JSSP(dataset)
    config = Run_Config(n_job=dataset.n_job, n_machine=dataset.n_machine, n_op=dataset.n_op, population_size=100,
                        generations=1,
                        print_console=False, save_log=True, save_machinelog=True,
                        show_gantt=False, save_gantt=True, show_gui=False,
                        trace_object='Process4', title='Gantt Chart for JSSP',
                        tabu_search_iterations=10, hill_climbing_iterations=30, simulated_annealing_iterations=50,
                        two_iterations=1000, target_makespan=None)

    RUBI_individuals = [Individual(config, seq=jssp.get_seq(), op_data=dataset.op_data) for i in range(10)]
    RUBI_makespan = [s.makespan for s in RUBI_individuals]
    SPT = [baseline(dataset, "min") for i in range(10)]
    SPT_individuals = [Individual(config, seq=spt_seq[1], op_data=dataset.op_data) for spt_seq in SPT]
    SPT_makespan1 = [spt_seq[0] for spt_seq in SPT]
    SPT_makespan2 = [s.makespan for s in SPT_individuals]
    GT = [GifflerandThompson(dataset) for _ in range(10)]
    GT_individuals = [Individual(config, seq=gt_seq, op_data=dataset.op_data) for gt_seq in GT]


    print()