import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from networkx.algorithms.community import greedy_modularity_communities
import random
import numpy as np

G = nx.read_edgelist('community4.txt', delimiter='|', nodetype=str)

pagerank_dict = nx.pagerank(G, alpha=0.9)  # 確率αで中心性を伝搬する

pagerank_list = sorted(  # 中心性の大きい順に並び替え
    pagerank_dict.items(), key=lambda x: x[1], reverse=True)

community_list = list(greedy_modularity_communities(G))

labeldict = {}
count = 0
for community_num in range(len(community_list)):
    for value in community_list[community_num]:
        labeldict[value] = count
    count = count + 1

df = pd.read_csv('Belong_to_Tsukuba.csv', usecols=[
    0, 1, 4], low_memory=False)  # 名前と所属のcolumnを抽出

for value in pagerank_list:
    print(value[0], '(', df[df['姓名'] == value[0]]
          ['所属 (現在)'].values.tolist()[0], ')=', value[1])
