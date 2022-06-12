import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


#G = nx.read_edgelist('community3.txt', delimiter='|', nodetype=str)
G = nx.read_edgelist('new_community3.txt', delimiter='|', nodetype=str)


def all_edge_sigma(G):
    for edge in G.edges():
        # edgeに接続しているノードの隣接ノードをsetとして返す
        set_u = set(nx.all_neighbors(G, edge[0]))
        set_v = set(nx.all_neighbors(G, edge[1]))
        # 自分自身も加える
        set_u.add(edge[0])
        set_v.add(edge[1])
        # set_uとset_vの積集合
        set_uv = set_u & set_v
        # 構造的類似度を計算
        sigma_uv = len(set_uv)/np.sqrt(len(set_u)*len(set_v))
        # エッジに計算した値を付与
        G.edges[edge[0], edge[1]]['key'] = sigma_uv


# 全てのノードについてcoreかどうか判定
def judge_core(G, eps, mu):
    # coreノードのリスト
    core_node_list = []
    # coreノードとクラスタを形成するノードの集合リスト(core_node_listと1対1対応)
    next_list = []

    # 全てのノードについて見る,coreかどうか
    for node in G.nodes():
        # あるノードについて,その隣接ノードとのエッジがeps以上だった場合,その隣接ノードを追加.
        # ただしそのノードが結果的にcoreじゃなかった場合は捨てられる
        core_next_node = set()
        count = 0
        # あるノードの隣接ノードの集合
        next_node_set = set(nx.all_neighbors(G, node))

        # ノードとその隣接ノードによるエッジの属性値がeps以上ならcountを増やす
        for next_node in next_node_set:
            if G.edges[node, next_node]['key'] >= eps:
                count += 1
                # eps以上なら追加
                core_next_node.add(next_node)

        # 隣接ノードについて見終わったとき,countの値がmu以上ならそのノードに1(=core)の属性値を付与
        if count >= mu:
            # coreだった場合リストに追加
            core_node_list.append(node)
            next_list = next_list + [core_next_node]

    return [core_node_list, next_list]


# 形成中のcommunityの中にまだ結合されていないcoreノードがあるか確認
# あればそのcoreノードがcore_node_listのどこにあるのか,indexを返す
# なければ-1を返す
def core_search(core_node_list, community):
    for node in community:
        if node in core_node_list:
            core_index = core_node_list.index(node)
            return core_index
    return -1

# 出来上がったcommunity_listをcommunityの大きさ順にソート


def sort_community_list(community_list):
    new_community_list = []
    # communityに番号をふるための変数
    community_num = 1
    while(len(community_list)) > 0:
        cmp = 0
        cmp_index = -1
        for x in range(len(community_list)):
            if len(community_list[x]) > cmp:
                cmp = len(community_list[x])
                cmp_index = x
        extract_community = community_list.pop(cmp_index)
        new_community_list.append(extract_community)
        for node in extract_community:
            G.nodes[node]['core'] = community_num
        community_num += 1
    return new_community_list

# どのクラスターにも属さないノードに対してハブか外れ値か判定


def check_hub(G, alone_list, belong_list):
    for alone_node in alone_list:
        check_set = set()
        next_node_set = set(nx.all_neighbors(G, alone_node))
        for next_node in next_node_set:
            if next_node in belong_list:
                # クラスターに属さないノードについて,その周辺ノードのうち
                # どこかのクラスターに属しているノードのノード番号(クラスター番号)を追加していく
                check_set.add(G.nodes[next_node]['core'])

        if len(check_set) >= 2:  # 2つ以上のクラスターに接続している
            G.nodes[alone_node]['core'] = -1  # ハブなら-1
        else:
            G.nodes[alone_node]['core'] = -2  # 外れ値なら-2


# クラスターを形成
def create_community(core_node_list, next_list):
    # 形成されたクラスターを格納していく
    community_list = []
    # どこかのクラスターに属しているノードのリスト
    belong_list = []

    # coreなノードがなくなるまで繰り返す
    while len(core_node_list) > 0:
        # coreなノードを1つ持ってくる
        one_core_node = core_node_list.pop()
        # そのcoreなノードとクラスターを形成する集合を持ってくる
        community = next_list.pop()

        while True:
            # 形成中のクラスターにまだ結合されていないcoreなノードがないか確認
            core_index = core_search(core_node_list, community)
            if core_index == -1:
                break
            else:
                # 形成中のクラスターの中に見つかったcoreなノードをcore_node_listから取り出す
                core_node_list.pop(core_index)
                # そのcoreなノードとクラスターを形成するノードの集合を取り出す
                next_community = next_list.pop(core_index)
                # 形成中のクラスターに結合
                community = community | next_community
        # 最後に自分自身を追加
        community.add(one_core_node)
        # 出来上がったクラスターをリストに追加
        community_list.append(community)
        # クラスターに属しているノードとしてリストに追加
        for node in community:
            belong_list.append(node)

    # community_listのソート
    new_community_list = sort_community_list(community_list)

    alone_list = []  # ハブ,外れ値の人のリスト
    # どこのクラスターにも属していないノードをハブ・外れ値として処理
    for node in G.nodes:
        if not node in belong_list:
            new_community_list.append({node})
            alone_list.append(node)

    check_hub(G, alone_list, belong_list)

    return new_community_list


def scan_communities(G, eps, mu):
    # 全てのedgeについて構造的類似度を計算
    all_edge_sigma(G)
    # 全てのノードについてcoreかどうか判定する
    core_result = judge_core(G, eps, mu)

    # 1つめの返り値にはcoreなノードのリスト
    core_node_list = core_result[0]
    # 2つめの返り値にはcoreノードとクラスタを形成するノードの集合リスト
    # (1つめの返り値であるcore_node_listに対応)
    next_list = core_result[1]

    # print(core_node_list)

    return create_community(core_node_list, next_list)


community_list = scan_communities(G, 0.6, 3)

df = pd.read_csv('Belong_to_Tsukuba.csv', usecols=[
    0, 1, 4], low_memory=False)  # 名前と所属のcolumnを抽出


for x in range(len(community_list)):
    #print(x+1, community_list[x])
    print('community', x+1, '=')
    for node in community_list[x]:
        print(node, ':', df[df['姓名'] == node]['所属 (現在)'].values.tolist()[0])
    print('')
