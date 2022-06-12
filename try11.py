import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from networkx.algorithms.community import greedy_modularity_communities
import random
import numpy as np

# クラスタリングしたとき,(クラスタのノード数/全ノード数) > percentage を満たすクラスタを大きなクラスタとする
percentage = 0.01

G = nx.read_edgelist('Tsukuba_teacher.txt', delimiter='|', nodetype=str)

pos = nx.spring_layout(G, dim=2, k=500000, iterations=5, scale=0.2)


# ライブラリを利用したコミュニティのリスト
community_list = list(greedy_modularity_communities(G))

print(community_list)
