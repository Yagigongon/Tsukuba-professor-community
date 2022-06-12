import networkx as nx
G = nx.read_edgelist("Tsukuba_teacher.txt", delimiter='|', nodetype=str)
# print(G.number_of_nodes())
# print(G.number_of_edges())
num_of_neighbors_dict = {}
for node in G.nodes():
    num_of_neighbors_dict[node] = len(list(nx.all_neighbors(G, node)))

num_of_neighbors_dict = sorted(
    num_of_neighbors_dict.items(), key=lambda x: x[1], reverse=True)


print(num_of_neighbors_dict)
