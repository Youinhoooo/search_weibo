import networkx as nx

def add_attribute(G):
   for edge in G.edges:
      i = edge[0]
      j = edge[1]
      G[i][j]['isclassified'] = False
      G[i][j]['iscore'] = False
      G[i][j]['dirreach'] = []

def similar(edge1,edge2,G):
    l_1 = list(edge1)
    l_2 = list(edge2)
    l = l_1 + l_2
    for a in set(l_1)&set(l_2):
        while a in l:
            l.remove(a)
    if len(l)<2:
        return -1
    l_edge1 = list(i for i in nx.neighbors(G,l[0]))
    l_edge2 = list(j for j in nx.neighbors(G,l[1]))
    up = set(l_edge1)&set(l_edge2)
    down = set(l_edge1+l_edge2)
    return len(up)/len(down)

def is_core(edge,xigma,miu,G):
    a = edge[0]
    b = edge[1]
    conform_edge = []
    # 得到邻接节点
    neigh_a = nx.neighbors(G,a)
    neigh_b = nx.neighbors(G,b)
    # 得到邻接边
    neigh_a_edge = [(a,i) for i in neigh_a]
    neigh_b_edge = [(b,i) for i in neigh_b]
    neigh_a_edge.remove((a,b))
    neigh_b_edge.remove((b,a))
    # 计算相似度,合并相似度大于阈值的边
    for edge_1 in neigh_a_edge:
        sim = similar(edge,edge_1,G)
        if sim > xigma:
            conform_edge.append(edge_1)
    # 判断是否为核心边
    if len(conform_edge) > miu:
        G[a][b]['iscore'] = True
        G[a][b]['dirreach'] = conform_edge

def DirReach(x,G):
    a = x[0]
    b = x[1]
    if G[a][b]['iscore'] == True:
        return G[a][b]['dirreach']
    else:
        return []

def FindLinkComm(eage,G):
    LC = []
    Q = []
    Q.append(eage)
    G[eage[0]][eage[1]]['isclassified'] = True
    while len(Q) != 0:
        x = Q.pop(0)
        R = DirReach(x,G)
        for l in R:
            if G[l[0]][l[1]]['isclassified'] == False:
                G[l[0]][l[1]]['isclassified'] = True
            if G[l[0]][l[1]]['iscore'] == True:
                LC.append(l)
                Q.append(l)
            else:
                LC.append(l)
        #Q.pop(0)
    return LC

def find_edge(G):
    LCS = []
    for eage in G.edges:
        edge_dict = G[eage[0]][eage[1]]
        if edge_dict['isclassified'] == False:
            if edge_dict['iscore'] == True:
                G[eage[0]][eage[1]]['isclassified'] = True
                LCS = list(set(LCS + FindLinkComm(eage,G)))

    return LCS

if __name__ == '__main__':
    i = 0
    G_1 = nx.read_gml(r'D:\jupyter_file\w_q_bei\g1.gml')
    G_2 = nx.read_gml(r'D:\jupyter_file\w_q_bei\g2.gml')
    G_3 = nx.read_gml(r'D:\jupyter_file\w_q_bei\g3.gml')
    add_attribute(G_1)
    add_attribute(G_2)
    add_attribute(G_3)

    for edge in G_1.edges:
        a = edge[0]
        b = edge[1]
        is_core(edge,xigma=0.75,miu=1000,G=G_1)
        i = i + 1
        if i%500 == 0:
            print('-'*100)
            print(i)
    LCS_G1 = find_edge(G_1)
    with open('g_1.txt') as f:
        f.write(LCS_G1)