import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from networkx.algorithms.community import greedy_modularity_communities
import random
import numpy as np


G = nx.read_edgelist('Tsukuba_teacher.txt', delimiter='|', nodetype=str)

check_list = ['高橋 智']  # 影響度を調べたいノード

personalization_dict = {}

for node in G.nodes():
    if node in check_list:  # 影響度を調べたいノードに1
        personalization_dict[node] = 1
    else:  # それ以外に0
        personalization_dict[node] = 0

for value in personalization_dict:  # 正規化
    personalization_dict[value] = personalization_dict[value]/len(check_list)

ppr_dict = nx.pagerank(G, alpha=0.9, personalization=personalization_dict)

ppr_list = sorted(  # 中心性の値が大きい順に並び替え
    ppr_dict.items(), key=lambda x: x[1], reverse=True)

df = pd.read_csv('Belong_to_Tsukuba.csv', usecols=[
    0, 1, 4], low_memory=False)  # 名前と所属のcolumnを抽出
"""
for value in pagerank_list:
    print(value[0], '(', df[df['姓名'] == value[0]]
          ['所属 (現在)'].values.tolist()[0], ')=', value[1])
"""
for value in ppr_list:
    if not value[0] in check_list:  # 調査対象は除外
        print(value[0], '(', df[df['姓名'] == value[0]]
              ['所属 (現在)'].values.tolist()[0], ')=', value[1])
