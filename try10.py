import random
import numpy as np
import networkx as nx
import string

random.seed(42)  # 乱数シード固定

G = nx.barabasi_albert_graph(10, 1)
print(G.degree())
# [(0, 5), (1, 1), (2, 4), (3, 2), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1)]

# ノードの名前を変更する。
mapping = {k: v for k, v in zip(G.nodes, string.ascii_lowercase)}

print(mapping)

G = nx.relabel_nodes(G, mapping)
print(G.degree())
