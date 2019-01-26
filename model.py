# coding:utf-8

# 美赛D题线路规划

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
imax=5
k=0.6
# 初始化图，添加点与边
def Graph_init(G):
    floor=['A','B','C','D','E']
    colors=['r','y','g','c','m']
    
    for i in range(5):
        for j in range(imax):
            node_num=i*imax+j
            G.add_node(node_num,pos=(j,i),label=(floor[i]+str(j)),color=i,count=5)
            colorlist.append(colors[i])
            if (i>0):
                G.add_edge(node_num,node_num-imax,weight=1)
            for k in range(j,0,-1):
                G.add_edge(node_num,node_num-k,weight=1)
    #G.add_edges_from([(1,2),(1,3),(1,5),(4,5),(4,6),(5,6)])
    #nx.set_node_attributes(G, labels, 'labels')
    # G.add_edge(0,1,weight=80)
    
# 画出G的点、边及其属性
def Graph_show(G):
    e_labels = nx.get_edge_attributes(G,'weight')
    nx.draw(G,pos,with_labels=False,edge_labels=e_labels)
    nx.draw_networkx_edge_labels(G,pos,edge_labels=e_labels)
    nx.draw_networkx(G, pos, labels=node_labels,font_size=12,node_color=colorlist)
    G.edges(data=True)
    plt.ion()
    #plt.savefig("test.png")
    plt.show()
    plt.pause(0.03)
    #plt.close()
    #print("nodes:", G.nodes())      #输出全部的节点： [1, 2, 3]
    #print("edges:", G.edges())      #输出全部的边：[(2, 3)]
    #print("number of edges:", G.number_of_edges())   #输出边的数量：1

# 修改已经存在的边的权重
def change_weight(G,src,dst,change):
    G[src][dst]['weight']=G[src][dst]['weight']+change

# 返回为list，格式[1]为各个点路径，[2]为总代价
def get_shortest_path(G,src,dst):
    path = nx.dijkstra_path(G, src, dst, weight='weight')#求最短路径
    cost = nx.shortest_path_length(G,src,dst,weight='weight')
    # print(path)
    # print(cost)
    ret=[]
    ret.append(path)
    ret.append(cost)
    return(ret)

# 点的label->index
def l2n(label):
    ret = get_keys(node_labels,label)
    return ret

# 点的number->label
def n2l(num):
    return node_labels.get(num)

# 查找dictionary，返回key
def get_keys(dic,value):
    for k,v in dic.items():
        if v == value:
            return k
    
def letsgo(G,src,dst):
    rate=0.5
    #print(node_counts[1])
    #print(node_counts[l2n(src)])
    ret=get_shortest_path(G,l2n(src),l2n(dst))
    count=node_counts[l2n(src)]
    leave=l2n(src)
    f.write(str(count)+' w:'+str(ret[1])+' path:'+n2l(leave))
    
    for go in ret[0]:
        # 不会是第一个 A0->A0
        if (leave == go):
            continue
        #f.write(n2l(leave)+'->'+n2l(go))
        f.write('->'+n2l(go))
        #print(G[leave][go]['weight'])
        change_weight(G,leave,go,count)
        #print()
        leave=go
    #print(ret[1])
    f.write('\n')
    temp=int(float(node_counts[l2n(src)])*rate)
    #print(rate)
    node_counts[l2n(src)]=temp
    print(node_counts[l2n(src)])
    #print(node_counts[l2n(src)])
    Graph_show(G)



if __name__ == "__main__":
    G=nx.Graph()
    colorlist=[]
    Graph_init(G)
    f=open("out.txt","w")
    pos=nx.get_node_attributes(G,'pos')
    # 边的权重
    e_labels = nx.get_edge_attributes(G,'weight')
    # 点的标记
    node_labels=nx.get_node_attributes(G,'label')
    #node_label_list=
    # 点的颜色
    node_colors=nx.get_node_attributes(G,'color')
    node_counts=nx.get_node_attributes(G,'count')
    #print(node_counts[1])
    '''
    ret=get_shortest_path(G,l2n('A1'),l2n('C0'))
    leave=l2n('A1')
    #print(G[1][0]['weight']+1)
    Graph_show(G)
    for go in ret[0]:
        if (leave == go):
            continue
        print(n2l(leave)+'->'+n2l(go))
        #print(G[leave][go]['weight'])
        change_weight(G,leave,go,1)
        leave=go
    print(ret[1])
    '''
    floor=['A','B','C','D','E']
    Graph_show(G)
    for k in range(3):
        node_counts=nx.get_node_attributes(G,'count')
        print(node_counts)
        for i in range(5):
            for j in range(imax):
                p=floor[i]
                p+=str(j)
                #print(p)
                letsgo(G,p,'C0')
    #letsgo(G,'A1','C0',5)
    #plt.ioff()
    #print(G[1][5])

    
