import pandas as pd

df1 = pd.read_csv('Belong_to_Tsukuba.csv', usecols=[
                  0, 1, 4])  # 名前と所属のcolumnを抽出

df1 = df1.dropna(subset=['所属 (現在)'])  # 現在の所属が不明(NaN)の場合,除外

# print(df1)

df1 = df1[df1['所属 (現在)'].str.contains('筑波大学')]  # 現在の所属が筑波大学の人を抽出

#print(df1['姓名'] == '橋本 康二')

print(df1['姓名'].values.tolist())
