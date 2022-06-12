import pandas as pd


#df2 = pd.read_csv('Tsukuba_thesis.csv', usecols=[0, 4, 5, 6, 7, 8, 9, 10])
#df2 = pd.read_csv('Tsukuba_thesis.csv', usecols=[0, 4, 5, 6, 7, 8, 9, 10], converters={'研究代表者': str, '研究分担者': str, '連携研究者': str, '研究協力者': str, '特別研究員': str, '外国人特別研究員': str, '受入研究者': str})

# sys: 1: DtypeWarning: Columns(5, 6, 7, 8, 9, 10) have mixed types.Specify dtype option on import or set low_memory = False.
df2 = pd.read_csv('Tsukuba_thesis.csv', usecols=[
                  0, 4, 5, 6, 7, 8, 9, 10], low_memory=False)

df2 = df2.fillna('-')

column_list = [1, 2, 3, 4, 5, 6, 7]
index_list = []
name_list = []
s = '塩川 浩昭'
# print(df2[df2['研究代表者'].str.contains(s)].index)

#x = df2[df2['研究代表者'].str.contains(s)].index.values.tolist()

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
# name_list = [name[:name.find(' 筑波大学')] for name in name_list]  # 名前のみ残るようにする

# for name in name_list:


# print(name_list)

name_list = list(set(name_list))
print(name_list)

# for name in name_list:
#print(s, '', name)


#print(df2.iat[1209, 1])
#print(df2.iat[2620, 2])


#print(df2.iat[0, 2])

#df = df2.iat[0, 2]

#df = df.splitlines()

# print(df)
# print(df2.index[600])
