import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from networkx.algorithms.community import greedy_modularity_communities
import random
import numpy as np

G = nx.read_edgelist('Tsukuba_teacher.txt', delimiter='|', nodetype=str)

print(G.number_of_nodes())
print(G.number_of_edges())
