import pandas as pd

optimal = {'la01': 666, 'la11': 1222,
           'la02': 655, 'la12': 1039,
           'la03': 597, 'la13': 1150,
           'la04': 590, 'la14': 1292,
           'la05': 593, 'la15': 1207,
           'la06': 926, 'la16': 945,
           'la07': 890, 'la17': 784,
           'la08': 863, 'la18': 848,
           'la09': 951, 'la19': 842,
           'la10': 958, 'la20': 902,
           }
# CSV 파일 불러오기
df = pd.read_csv("result_250114.csv")  # 실제 파일 경로로 바꿔줘야 함

# Initialization 값들
init_values = ['SGA_BM','SGA_BRT','RUBI_BM', 'RUBI_BRT']
problem_values = [f"la{str(i).zfill(2)}" for i in range(1, 21)]

# 결과를 담을 DataFrame
result_matrix = pd.DataFrame(index=problem_values, columns=init_values)

# 각 Problem-Initialization 조합에 대해 seed 개수 확인
for problem in problem_values:
    for init in [0, 100]:
        subset = df[(df['Problem'] == problem) & (df['Initialization'] == init)]
        problem = subset['Problem'].unique()[0]
        optimal_set = subset[subset['Best Makespan'] == optimal[problem]]
        if optimal_set.shape[0] !=0:
            avg_optimal = round(optimal_set['Best Reached Time'].mean(),3)
        else:
            avg_optimal = None
        # seed_count = subset['Seed'].nunique()
        if init == 0:
            result_matrix.loc[problem, "SGA_BM"] = subset['Best Makespan'].min()
            result_matrix.loc[problem, "SGA_BRT"] = avg_optimal
        elif init == 100:
            result_matrix.loc[problem, "RUBI_BM"] = subset['Best Makespan'].min()
            result_matrix.loc[problem, "RUBI_BRT"] = avg_optimal

# 불리언 타입으로 변환 (선택 사항)
# result_matrix = result_matrix.astype(bool)

# 결과 출력
print(result_matrix)
