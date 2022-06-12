import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from networkx.algorithms.community import greedy_modularity_communities
import random
import numpy as np

G = nx.read_edgelist('Tsukuba_teacher.txt', delimiter='|', nodetype=str)

pagerank_dict = nx.pagerank(G, alpha=0.9)  # 確率αで中心性を伝搬する

pagerank_list = sorted(  # 中心性の大きい順に並び替え
    pagerank_dict.items(), key=lambda x: x[1], reverse=True)

df = pd.read_csv('Belong_to_Tsukuba.csv', usecols=[
    0, 1, 4], low_memory=False)  # 名前と所属のcolumnを抽出

for value in pagerank_list:
    print(value[0], '(', df[df['姓名'] == value[0]]
          ['所属 (現在)'].values.tolist()[0], ')=', value[1])
