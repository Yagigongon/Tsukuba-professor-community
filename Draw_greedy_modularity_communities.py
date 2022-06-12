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

# 全ノード数に対するコミュニティの大きさの割合
community_ratio = []

for x in community_list:
    community_ratio.append(len(x)/G.number_of_nodes())

# community_ratioに基づいてコミュニティ毎に位置を決める
angle = []
angle.append(0)

for x in range(1, len(community_list)):
    cmp = angle[x-1]
    angle.append(community_ratio[x-1]*2*np.pi + cmp)

 # (reposに各コミュニティの中心となる座標が格納されている)

repos = []
rad = 0.5

for ea in angle:
    repos.append(np.array([rad*np.cos(ea), rad*np.sin(ea)]))

# 要素数が多い順に並んでいるコミュニティのリストについて上から1番,2番...としたとき全ノードについてコミュニティ番号を割り当てる
labeldict = {}
count = 0
for community_num in range(len(community_list)):
    for value in community_list[community_num]:
        labeldict[value] = count
    count = count + 1

# 指定した数だけカラーセットをランダム生成


def rand_ints_nodup(a, b, k):
    ns = []
    while len(ns) < k:
        n = ((random.randint(a, b))/255, (random.randint(
            a, b))/255, (random.randint(a, b))/255)
        if not n in ns:
            ns.append(n)
    return ns


# コミュニティの数だけカラーセットを生成
color_random = (rand_ints_nodup(0, 255, len(community_list)))

node_community_color = []  # ノード毎に色を指定するための配列
my_node_size = []  # ノード毎に大きさを指定するための配列
node_weight = nx.degree(G)  # 各ノードについて接続されているエッジの数が格納されている

for node in G.nodes():  # 全てのノードについて見る
    my_node_size.append(node_weight[node]*10)
    node_community_color.append(color_random[labeldict[node]])
    pos[node] += repos[labeldict[node]]  # 自分が属するコミュニティの中心座標の近くにくるように移動

my_edge_width = []  # エッジの太さを指定するための配列

for edge in G.edges():
    # エッジに接続しているノードが大きなコミュニティに属している場合
    if (community_ratio[labeldict[edge[0]]] > percentage) and (community_ratio[labeldict[edge[1]]] > percentage):
        my_edge_width.append(1.0)
    else:
        my_edge_width.append(0.1)


for edge in G.edges():  # 見やすくするため同じコミュニティ間のエッジは削除
    if labeldict[edge[0]] == labeldict[edge[1]]:
        G.remove_edge(edge[0], edge[1])

df = pd.read_csv('Belong_to_Tsukuba.csv', usecols=[
    0, 1, 4], low_memory=False)  # 名前と所属のcolumnを抽出


for x in range(len(community_list)):
    #print(x+1, community_list[x])
    print('community', x+1, '=')
    for node in community_list[x]:
        print(node, ':', df[df['姓名'] == node]['所属 (現在)'].values.tolist()[0])
    print('')


plt.figure(figsize=(10, 8))  # ウィンドウの大きさを指定

nx.draw(G, pos=pos, node_size=my_node_size, node_color=node_community_color,
        edge_color=(0, 0, 0, 0.1), width=my_edge_width, with_labels=True,
        font_size=5, font_color=(0, 0, 0), font_family='Hiragino Mincho ProN')

plt.axis('off')
plt.show()  # 表示
