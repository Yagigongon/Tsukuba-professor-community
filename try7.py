import networkx as nx

G = nx.read_edgelist("Tsukuba_teacher.txt", delimiter='|', nodetype=str)
check_list = ['北川 博之']  # 影響度を調べたいノード

personalization_dict = {}

for node in G.nodes():
    if node in check_list:  # 影響度を調べたいノードに1
        personalization_dict[node] = 1
    else:  # それ以外に0
        personalization_dict[node] = 0

# print('OK')
for value in personalization_dict:  # 正規化
    personalization_dict[value] = personalization_dict[value]/len(check_list)

# print('OK')
#print(personalization_dict['北川 博之'])
# print(personalization_dict)


ppr_dict = nx.pagerank(G, alpha=0.7, personalization=personalization_dict)

# print('OK')

ppr_list = sorted(  # 中心性の値が大きい順に並び替え
    ppr_dict.items(), key=lambda x: x[1], reverse=True)

for value in ppr_list:
    if not value[0] in check_list:  # 調査対象は除外
        print(value[0], value[1])
