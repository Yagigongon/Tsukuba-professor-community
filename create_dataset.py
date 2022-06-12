import pandas as pd
import warnings
warnings.filterwarnings("ignore", 'This pattern has match groups')

df = pd.read_csv('Belong_to_Tsukuba.csv', usecols=[
    0, 1, 4], low_memory=False)  # 名前と所属のcolumnを抽出

df = df.dropna(subset=['所属 (現在)'])  # 現在の所属が不明(NaN)の場合,除外

df1 = df[df['所属 (現在)'].str.contains('筑波大学')]  # 現在の所属が筑波大学の人を抽出

node_list = df1['姓名'].values.tolist()  # 筑波大学の教員

# 筑波大学教員が関わっている論文
df2 = pd.read_csv('Tsukuba_thesis.csv', usecols=[
                  0, 4, 5, 6, 7, 8, 9, 10], low_memory=False)

# NaNを「-」で補完
df2 = df2.fillna('-')

# 1:研究代表者
# 2:研究分担者
# 3:連携研究者
# 4:研究協力者
# 5:特別研究員
# 6:外国人特別研究員
# 7:受入研究者
column_list = [1, 2, 3, 4, 5, 6, 7]

for node in node_list:
    index_list = []
    name_list = []

    index_list += df2[df2['研究代表者'].str.contains(node)].index.values.tolist()
    index_list += df2[df2['研究分担者'].str.contains(node)].index.values.tolist()
    index_list += df2[df2['連携研究者'].str.contains(node)].index.values.tolist()
    index_list += df2[df2['研究協力者'].str.contains(node)].index.values.tolist()
    index_list += df2[df2['特別研究員'].str.contains(node)].index.values.tolist()
    index_list += df2[df2['外国人特別研究員'].str.contains(node)].index.values.tolist()
    index_list += df2[df2['受入研究者'].str.contains(node)].index.values.tolist()

    for index in index_list:
        for column in column_list:
            names = df2.iat[index, column]
            names = names.splitlines()
            name_list += names

    name_list = [name for name in name_list if name != '-']  # NaNを除く
    name_list = [name for name in name_list if not node in name]  # 本人を除く
    name_list = [name for name in name_list if '筑波大学' in name]  # 筑波大学関係者

    name_list = [name[name.rfind('(')+1:name.rfind(')')]
                 for name in name_list if name.rfind('(') != -1 and name.rfind(')') != -1]  # 研究者番号を残す
    name_list = [int(name) for name in name_list if name.isdigit() == True]

    name_list = list(set(name_list))  # 重複を除く

    for num in name_list:
        next_list = df[df['研究者番号'] == num]['姓名'].values.tolist()
        if len(next_list) != 0:
            print(node, '|', next_list[0], sep='')
