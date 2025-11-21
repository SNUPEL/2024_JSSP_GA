from Data.Dataset.Dataset import Dataset
import random


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

def GifflerandThompson(_dataset):
    _dataset: Dataset
    # schedule = []
    # machine_list = [Machine(i) for i in range(_dataset.n_machine)]
    # job_list = [Job(i, _dataset.op_data[i]) for i in range(_dataset.n_job)]
    # now = 0
    # event_time_list = []  # (machine_idx, machine.earliest_finish)

    current_index = [0 for i in range(_dataset.n_job)]
    machine_ETT = [0 for i in range(_dataset.n_machine)] # Earliest Termination Time
    done = False
    # now = 0
    operation_ESD = [0 for i in range(_dataset.n_job)]
    job_seq = []
    while not done:
        pt_list = [0 for i in range(_dataset.n_job)]
        machine_list = [0 for i in range(_dataset.n_job)] # 현재 작업해야 하는 machine 들의 목록
        for i in range(_dataset.n_job):
            if current_index[i] != _dataset.n_machine:
                pt_list[i] = _dataset.op_data[i][current_index[i]][1]
            else:
                pt_list[i] = float('inf')

        for i in range(_dataset.n_job):
            if current_index[i] != _dataset.n_machine:
                machine_list[i] = _dataset.op_data[i][current_index[i]][0]
            else:
                machine_list[i] = float('inf')
        # print(f'현재 남아있는 operation들의 작업시간 : ', pt_list)
        # print(f'현재 남아있는 operation에 해당하는 machine : ', machine_list)
        operation_ETT = [0 for i in range(_dataset.n_job)]
        # print('현재 각 operation들이 작업을 시작할 수 있는 시간 :', operation_ESD)
        for i in range(_dataset.n_job):
            if current_index[i] != _dataset.n_machine:
                operation_ETT[i] = max(operation_ESD[i], machine_ETT[machine_list[i]]) + pt_list[i]
            else:
                operation_ETT[i] = float('inf')
            # print(f'Job{i}의 가장 빠른 operation 완료시간은 operation_ESD {operation_ESD[i]} 와 machine_ETT {machine_ETT[machine_list[i]]} 중에 더 큰 값에 pt를 더한 {operation_ETT[i]}입니다.')
            # if operation_ESD[i] >= machine_ETT[machine_list[i]]: # 23 > 10
            #     operation_ETT[i] = operation_ESD[i] + pt_list[i] # 23 + 5
            # else: # 23 , 30
            #     operation_ETT[i] = machine_ETT[machine_list[i]] + pt_list[i] # 30 + 5

        # print('현재 각 operation들이 끝날 수 있는 시간 :', operation_ETT)
        selected_job = operation_ETT.index(min(operation_ETT))
        selected_machine = machine_list[selected_job]
        # machine_ETT[selected_machine] = min(operation_ETT)

        # candidate set
        candidates = [i for i, v in enumerate(machine_list) if v == selected_machine]
        active_candidates = []
        for c in candidates:
            if operation_ESD[c]<min(operation_ETT):
                active_candidates.append(c)
        selected_job = random.choice(active_candidates)
        machine_ETT[selected_machine] = operation_ETT[selected_job]

        job_seq.append(selected_job * _dataset.n_machine + current_index[selected_job])

        current_index[selected_job] += 1
        # print(current_index)
        # print(f'Job{selected_job}를 machine{selected_machine}에서 작업합니다.')
        #       f'\n\t작업시간은 {pt_list[selected_job]}, 끝나는 시점은 {machine_ETT[selected_machine]}이 될 예정입니다.')
        # print('machine_ETT:',machine_ETT)
        operation_ESD[selected_job] = operation_ETT[selected_job]
        if sum(current_index) == _dataset.n_job * _dataset.n_machine:
            done = True
    # print(max(machine_ETT))
    return job_seq




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

