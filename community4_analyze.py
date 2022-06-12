import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from networkx.algorithms.community import greedy_modularity_communities
import random
import numpy as np


G = nx.read_edgelist('Tsukuba_teacher.txt', delimiter='|', nodetype=str)
# ライブラリを利用したコミュニティのリスト
community_list = list(greedy_modularity_communities(G))

labeldict = {}
count = 0
for community_num in range(len(community_list)):
    for value in community_list[community_num]:
        labeldict[value] = count
    count = count + 1

"""
for edge in G.edges():
    if labeldict[edge[0]] == 2 and labeldict[edge[1]] == 2:
        print(edge[0], '|', edge[1], sep='')
"""

for edge in G.edges():
    if labeldict[edge[0]] == 3 or labeldict[edge[1]] == 3:
        print(edge[0], '|', edge[1], sep='')
