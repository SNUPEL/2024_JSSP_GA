from Data.Dataset.Dataset import Dataset
import random
from GAS.Population import JSSP

class Job:
    def __init__(self, idx, op_data):
        self.idx = idx
        self.current_idx = 0
        self.op_data = op_data

class Machine:
    def __init__(self, idx):
        self.idx = idx
        self.current_job = None
        self.earliest_finish = None
        self.ready_task = [] # (job, processing_time)
        self.working = False

    def finish(self, now):
        if now >= self.earliest_finish:
            # print(f"{now}M{self.idx}이 working을 끝냅니다.")
            self.working = False

    def schedule(self, now, mode, event_time_list):
        if self.working:
            # print(f"{now}\tM{self.idx}은 working 중이므로 별도의 schedule이 이루어지지 않습니다.")
            return None
        else:
            if len(self.ready_task) == 0:
                return None
            else:
                # 1. 최소값 찾기
                if mode == "min":
                    value = min(item[1] for item in self.ready_task)
                elif mode == "max":
                    value = max(item[1] for item in self.ready_task)
                else:
                    raise Exception("Invalid mode")
                # 2. 최소값을 갖는 인덱스 목록 추출
                indices = [i for i, item in enumerate(self.ready_task) if item[1] == value]

                # 3. 그 중 하나를 랜덤 선택
                chosen_index = random.choice(indices)

                # 4. pop
                job, pt = self.ready_task.pop(chosen_index)

                # 5. 지정
                self.current_job = job
                self.working = True
                self.earliest_finish = now + pt
                event_time_list.append((self.idx, self.earliest_finish))
                return job

def baseline(_dataset, mode = 'min'):
    _dataset : Dataset
    schedule = []
    machine_list = [Machine(i) for i in range(_dataset.n_machine)]
    job_list = [Job(i, _dataset.op_data[i]) for i in range(_dataset.n_job)]
    now = 0
    event_time_list = [] # (machine_idx, machine.earliest_finish)

    # Initialize
    for job_idx, job in enumerate(job_list):
        target_machine = job.op_data[job.current_idx][0]
        machine_list[target_machine].ready_task.append((job_idx, job.op_data[job.current_idx][1])) # (job, processing time)

    for machine_idx, machine in enumerate(machine_list):
        job = machine.schedule(now, mode, event_time_list)
        if job is not None:
            schedule.append(job * _dataset.n_machine + job_list[job].current_idx)
        # event_time_list.append((machine_idx, machine.earliest_finish))

    while len(event_time_list) > 0:
        # 1. 최소값 찾기
        min_value = min(item[1] for item in event_time_list)
        # 2. 최소값을 갖는 인덱스 목록 추출
        min_indices = [i for i, item in enumerate(event_time_list) if item[1] == min_value]
        # 3. 그 중 하나를 랜덤 선택
        chosen_index = random.choice(min_indices)
        # 4. pop
        machine_idx, now = event_time_list.pop(chosen_index)

        machine = machine_list[machine_idx]
        machine.finish(now) # working이 False로 바뀜

        # current task 의 다음 operation 시작
        job_idx = machine.current_job
        job = job_list[job_idx]
        job.current_idx += 1
        if job.current_idx == _dataset.n_machine:
            pass
        else:
            next_machine_idx = job.op_data[job.current_idx][0]
            next_machine = machine_list[next_machine_idx]
            next_machine.ready_task.append((job_idx, job.op_data[job.current_idx][1]))

        # 모든 machine에 대해 schedule 한바퀴 돌리기
        for m in machine_list:
            job = m.schedule(now, mode, event_time_list)
            if job is not None:
                schedule.append(job * _dataset.n_machine + job_list[job].current_idx)

        # print(f"현재 현황: {[j.current_idx for j in job_list]}")
    # print(f"{[j.current_idx for j in job_list]} / {now}")
    return now, schedule


if __name__ == '__main__':
    from GAS.Individual import Individual
    from Config.Run_Config import Run_Config
    instance = 'la03.txt'
    dataset = Dataset(instance)
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

    print()