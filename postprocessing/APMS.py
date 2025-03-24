import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
file = "C:\\SNU EnSite\\2024_JSSP_GA\\result\\250318_initialization_100.csv"
# file = "C:\\SNU EnSite\\2024_JSSP_GA\\result\\250307_BSFS.csv"
result = pd.read_csv(file)


# 'Problem' 컬럼에서 unique한 값 추출
unique_problems = result['Problem'].unique()

# 'BS'로 시작하는 값 필터링
bs_problems = [p for p in unique_problems if p.startswith('BS')]
fs_problems = [p for p in unique_problems if p.startswith('FS')]

def process_problem_group(df, problem_list):
    # 필터링
    filtered_df = df[df['Problem'].isin(problem_list)].copy()
    filtered_df['Problem'] = filtered_df['Problem']  # 마지막 3자리 유지
    # filtered_df['Problem'] = filtered_df['Problem'].str[-2:]  # 마지막 3자리 유지

    # 'Problem' 별로 그룹화
    grouped = filtered_df.groupby('Problem')

    processed_rows = []
    for name, group in grouped:
        seeds = group['Seed'].unique()
        for seed in seeds:
            rows = group.loc[group.Seed == seed]
            # ratio = - rows.loc[rows['RUBI Ratio']==40]['Best Makespan'].values[0] +  rows.loc[rows['RUBI Ratio']==0]['Best Makespan'].values[0]
            # ratio = rows.loc[rows['RUBI Ratio']==40]['Best Makespan'].values[0] /  rows.loc[rows['RUBI Ratio']==0]['Best Makespan'].values[0]
            # base = optimal[name]
            best = rows.loc[rows['RUBI Ratio']==0]['Best Makespan'].values[0] - rows.loc[rows['RUBI Ratio']==100]['Best Makespan'].values[0]
            mean = rows.loc[rows['RUBI Ratio']==0]['Mean Makespan'].values[0] - rows.loc[rows['RUBI Ratio']==100]['Mean Makespan'].values[0]
            # processed_rows.append([name, rows['I_b'].values[0], rows['I_f'].values[0], seed, ratio])
            # processed_rows.append([name, n[name],m[name],problem_size[name], rows['I_b'].values[0], rows['I_f'].values[0], seed, ratio_basic - ratio_rubi])
            processed_rows.append([name, rows['I_b'].values[0], rows['I_f'].values[0], seed, best, mean])

    # return pd.DataFrame(processed_rows, columns=['Problem', 'n','m','size', 'I_b', 'I_f', 'seed', 'ratio'])
    return pd.DataFrame(processed_rows, columns=['Problem', 'I_b', 'I_f', 'seed', 'best', 'mean'])



# BS 및 FS 데이터프레임 생성
# ta_data = process_problem_group(result, ta_problems)
bs_data = process_problem_group(result, bs_problems)
fs_data = process_problem_group(result, fs_problems)

# 결과 확인
# print(bs_data.head())
# print(fs_data.head())


# 분석할 관계 설정
relations = [
    ('I_b', 'I_f'),
    ('I_b', 'best'),
    ('I_f', 'best'),
    ('I_b', 'mean'),
    ('I_f', 'mean'),
    (['I_b', 'I_f'], 'best'),
    (['I_b', 'I_f'], 'mean')
]

# 결과 저장할 딕셔너리
results = []
df = fs_data.copy()
# 개별 분석 수행
for x_col, y_col in relations:
    if isinstance(x_col, list):  # 다변수 분석
        X = df[x_col]
    else:  # 단변수 분석
        X = df[[x_col]]

    y = df[y_col]

    # 다항 특징 변환 (2차 다항 회귀)
    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(X)

    # 모델 학습
    model = LinearRegression()
    model.fit(X_poly, y)
    y_pred = model.predict(X_poly)

    # 신뢰도 평가 (R²)
    r2 = r2_score(y, y_pred)

    # 결과 저장
    results.append([str(x_col), y_col, round(r2, 4)])

    # 그래프 출력
    plt.scatter(df[x_col] if isinstance(x_col, str) else df[x_col[0]], y, label="Actual Data")
    plt.scatter(df[x_col] if isinstance(x_col, str) else df[x_col[0]], y_pred, color='red', label="Predicted Data")
    plt.xlabel(str(x_col))
    plt.ylabel(y_col)
    plt.title(f"FS data Polynomial Regression: {x_col} vs {y_col}")
    plt.legend()
    plt.show()

# 결과 테이블 출력
results_df = pd.DataFrame(results, columns=['X', 'Y', 'R²'])
print(results_df)

# 그래프 그리기
# plt.figure(figsize=(8, 5))

# fig = plt.figure()
# ax =  fig.add_subplot(111, projection='3d')
#
# # ax.scatter(bs_data['I_b'],bs_data['I_f'], bs_data['best'], color='r', alpha=0.7, label='BS Data')
# ax.scatter(fs_data['I_b'],fs_data['I_f'], fs_data['best'], color='b', alpha=0.7, label='FS Data')
#
# # 그래프 꾸미기
# plt.xlabel('I_b')
# plt.ylabel('I_f')
# # plt.zlabel('Best Diff.')
# plt.title('I_b vs Ratio')
# plt.legend()
# plt.grid(True)
#
# # 그래프 표시
# plt.show()


# #%%
# plt.scatter(fs_data['I_b'], fs_data['best'], color='r', alpha=0.7, label='Best Diff.')
# plt.scatter(fs_data['I_b'], fs_data['mean'], color='b', alpha=0.7, label='Mean Diff.')
plt.scatter(fs_data['I_f'], fs_data['I_b'], color='r', alpha=0.7, label='Best Diff.')
# plt.scatter(bs_data['I_f'], bs_data['best'], color='r', alpha=0.7, label='Best Diff.')
# plt.scatter(bs_data['I_f'], bs_data['mean'], color='b', alpha=0.7, label='Mean Diff.')
# # plt.scatter(bs_data['I_f'], bs_data['ratio'], color='r', alpha=0.7, label='BS Data')
# # plt.scatter(fs_data['I_f'], fs_data['ratio'], color='b', alpha=0.7, label='FS Data')
# # plt.scatter(bs_data['I_b'], bs_data['ratio'], color='r', alpha=0.7, label='BS Data')
# # plt.scatter(fs_data['I_b'], fs_data['ratio'], color='b', alpha=0.7, label='FS Data')
# # plt.scatter(ta_data['m'], ta_data['ratio'], color='r', alpha=0.7, label='Taillard Data')
# # plt.scatter(ta_data['I_f'], ta_data['ratio'], color='r', alpha=0.7, label='Taillard Data')
# # plt.scatter(ta_data['I_b'], ta_data['ratio'], color='r', alpha=0.7, label='Taillard Data')
#
# 그래프 꾸미기
plt.xlabel('I_f')
plt.title('I_f vs I_b')
# plt.title('I_f vs Difference')
# plt.title('I_f vs Ratio')
# plt.xlabel('I_b')
# plt.title('I_b vs Ratio')
plt.ylabel('Ratio')
plt.legend()
plt.grid(True)

# 그래프 표시
plt.show()