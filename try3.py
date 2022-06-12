import pandas as pd

df = pd.read_csv('Belong_to_Tsukuba.csv', usecols=[
    0, 1, 4])  # 名前と所属のcolumnを抽出

df = df.dropna(subset=['所属 (現在)'])  # 現在の所属が不明(NaN)の場合,除外

df1 = df[df['所属 (現在)'].str.contains('筑波大学')]  # 現在の所属が筑波大学の人を抽出

# 90775248

#print(df[df['研究者番号'] == 90775248]['姓名'].values.tolist()[0])

df2 = pd.read_csv('Tsukuba_thesis.csv', usecols=[
                  0, 4, 5, 6, 7, 8, 9, 10], low_memory=False)

df2 = df2.fillna('-')

column_list = [1, 2, 3, 4, 5, 6, 7]
index_list = []
name_list = []
s = '草野 都'

index_list += df2[df2['研究代表者'].str.contains(s)].index.values.tolist()
index_list += df2[df2['研究分担者'].str.contains(s)].index.values.tolist()
index_list += df2[df2['連携研究者'].str.contains(s)].index.values.tolist()
index_list += df2[df2['研究協力者'].str.contains(s)].index.values.tolist()
index_list += df2[df2['特別研究員'].str.contains(s)].index.values.tolist()
index_list += df2[df2['外国人特別研究員'].str.contains(s)].index.values.tolist()
index_list += df2[df2['受入研究者'].str.contains(s)].index.values.tolist()

# print(index_list)

for index in index_list:
    for column in column_list:
        names = df2.iat[index, column]
        names = names.splitlines()
        name_list += names

# print(name_list)

# print('')

name_list = [name for name in name_list if name != '-']  # NaNを除く
name_list = [name for name in name_list if not s in name]  # 本人を除く
name_list = [name for name in name_list if '筑波大学' in name]  # 筑波大学の教員
# name_list = [name[name.rfind('(')+1:name.rfind(')')]
# for name in name_list]  # 研究者番号を残す

name_list = [name[name.rfind('(')+1:name.rfind(')')]
             for name in name_list if name.rfind('(') != -1 and name.rfind(')') != -1]
name_list = [int(name) for name in name_list]

# num_list = [int(name[1:len(name)-1]) for name in name_list]  # 両端の()を除く,数値化
#name_list = [name.rstrip(')') for name in name_list]

name_list = list(set(name_list))
print(name_list)
for num in name_list:
    print(df[df['研究者番号'] == num]['姓名'].values.tolist()[0])
