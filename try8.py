import networkx as nx
import matplotlib.pyplot as plt

G = nx.read_edgelist("Tsukuba_teacher.txt", delimiter='|', nodetype=str)

pos = nx.spring_layout(G, dim=2, k=0.5, iterations=5, scale=5.0)

node_weight_color = []  # ノード毎に色を指定する
node_weight_size = []  # ノード毎にサイズを指定する
node_weight = nx.degree(G)  # 各ノードについて接続されているエッジの数が格納されている

for node in G.nodes():
    if node_weight[node] >= 15:
        node_weight_color.append((1, 0, 0))
        node_weight_size.append(50)  # ノードのサイズは8.0
    else:
        node_weight_color.append((0, 0, 1))
        node_weight_size.append(15)  # ノードのサイズは0.5

plt.figure(figsize=(10, 8))  # ウィンドウの大きさを指定

# 以下細かい指定
#(0.196, 0.80, 0.196)
nx.draw(G, pos, node_size=node_weight_size, node_color=node_weight_color, edge_color=(0, 0, 0, 0.5), width=0.1, with_labels=True,
        font_size=5, font_color=(1, 1, 0), font_family='Hiragino Mincho ProN')
plt.axis('off')
plt.show()  # 表示
