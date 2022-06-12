import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from networkx.algorithms.community import greedy_modularity_communities
import random
import numpy as np

G = nx.read_edgelist('Tsukuba_teacher.txt', delimiter='|', nodetype=str)

# ライブラリを利用したコミュニティのリスト
community_list = list(greedy_modularity_communities(G))

# print(community_list)
big_community = []
for x in range(len(community_list)):
    #print('community', x+1, '=')
    if x <= 7:
        big_community.append(community_list[x])
    else:
        break

labeldict = {}
count = 0
for community_num in range(len(community_list)):
    for value in community_list[community_num]:
        labeldict[value] = count
    count = count + 1


"""
for x in range(len(big_community)):
    count = 0
    for y in range(x+1,len(big_community)):
        set_y = big_community[y]
        for node in big_community[x]:
            set_node = set(nx.all_neighbors(G, node))
"""
next_num_list = [[0]*8 for _ in range(8)]
for edge in G.edges():
    less = labeldict[edge[0]]
    greater = labeldict[edge[1]]
    if (less <= 7) and (greater <= 7):
        if less > greater:
            tmp = less
            less = greater
            greater = tmp
        next_num_list[less][greater] += 1

"""
for y in range(len(next_num_list)):
    for x in range(y, len(next_num_list)):
        next_num_list[y][x] = next_num_list[y][x]/G.number_of_edges()
"""

for y in range(8):
    for x in range(8):
        if y < x:
            print('community', y+1, 'とcommunity',
                  x+1, 'の隣接係数は', next_num_list[y][x])

for x in range(len(community_list)):
    print(x+1, '=')
    for node in community_list[x]:
        print(node)
    print('')
