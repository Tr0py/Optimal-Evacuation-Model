# coding:utf-8

# 美赛D题线路规划

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
height=5
imax=38
node_in=open("node_in.txt","r")
hori_in=open("hori_in.txt","r")
Mnode=node_in.readlines()
Mhori=hori_in.readlines()
OUTPUT=0
roundCount=0
# 初始化图，添加点与边
def Graph_init(G):
    floor=['A','B','C','D','E']
    colors=['r','y','g','c','m']

    for i in range(height):
        Mnode[i]=Mnode[i].strip().split('\t')
    print(Mnode)

    for i in range(height):
        for j in range(imax):
            print("i:{} j:{}".format(i,j))
            if (Mnode[i][j]=='1'):
                node_num=i*imax+j
                G.add_node(node_num,pos=(j,i),label=(floor[i]+str(j)),color=i,count=200,path=[])
                print("add node:{}".format(node_num))
                colorlist.append(colors[i])
                if ((i>0) and (Mnode[i-1][j]=='1')):
                    G.add_edge(node_num,node_num-imax,weight=1)
                    print("add edge:{}->{}".format(node_num,node_num-imax))
                '''
                for k in range(j,0,-1):
                    #k=k-1
                    if (Mnode[i][j-k]=='1'):
                        G.add_edge(node_num,node_num-k,weight=1)
                        print("add edge2:{}->{}".format(node_num,node_num-k))
                '''
    #G.add_edges_from([(1,2),(1,3),(1,5),(4,5),(4,6),(5,6)])
    #nx.set_node_attributes(G, labels, 'labels')
    # G.add_edge(0,1,weight=80)
def add_horizontal_weights():
    j=0
    for i in Mhori:        
        Mhori[j]=Mhori[j].strip().split(' ')
        print(Mhori[j])
        src=Mhori[j][0]
        dst=Mhori[j][1]
        w=int(int(Mhori[j][2])*22/1.5)
        #for src,dst,w in Mhori[j]:
        #print("change_weight:{}->{}:{}".format(src,dst,w-1))
        #change_weight(G,l2n(src),l2n(dst),w-1)
        print("add_edge3:{}->{}:{}".format(src,dst,w))
        G.add_edge(l2n(src),l2n(dst),weight=w)
        j+=1
    print(Mhori)
    #exit()
    
# 画出G的点、边及其属性
def Graph_show(G):
    e_labels = nx.get_edge_attributes(G,'weight')
    global roundCount
    #roundCount+=1
    #print("roundCount:{}".format(roundCount))
    #print("roundCount:{} roundCount%10:{}".format(roundCount,(roundCount%10)))
    nx.draw(G,pos,with_labels=False,edge_labels=e_labels)
    nx.draw_networkx_edge_labels(G,pos,edge_labels=e_labels)
    nx.draw_networkx(G, pos, labels=node_labels,font_size=6,node_color=colorlist)
    G.edges(data=True)
    plt.ion()
    plt.savefig("test.png")
    plt.show()
    plt.pause(0.3)
    #plt.close()


# 修改已经存在的边的权重
def change_weight(G,src,dst,change):
    if (n2l(src)[0]!=n2l(dst)[0]):
        G[src][dst]['weight']=G[src][dst]['weight']+change
    #else:
        #print("hori!!{}{}".format(n2l(src),n2l(dst)))    

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
    global node_counts
    #print("banjjjjjjjjjjjjjju:{}->{}".format(src,dst))
    # 清除上次的path
    if (G.nodes[l2n(src)]['path']!=[]):
        count=(G.nodes[l2n(src)]['count'])
        leave=(G.nodes[l2n(src)]['path'][0])

        for go in G.nodes[l2n(src)]['path']:
            if (leave == go):
                continue
            #print("MINUS {}->{} by {}".format(n2l(leave),n2l(go),count))
            change_weight(G,leave,go,-count)
            leave=go
            

    rate=0.8
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
    G.nodes[l2n(src)]['count']=temp
    G.nodes[l2n(src)]['path']=ret[0]
    #print(node_counts)
    #print(node_counts[l2n(src)])
    #e_labels = nx.get_edge_attributes(G,'weight')
    #if (OUTPUT and (roundCount%3==0)):
    #    Graph_show(G)



if __name__ == "__main__":
    G=nx.Graph()
    roundCount=0
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
    add_horizontal_weights()
    floor=['A','B','C','D','E']
    #Graph_show(G)
    for k in range(16):
        if (k%3==0):
            Graph_show(G)
            node_counts=nx.get_node_attributes(G,'count')
            node_path=nx.get_node_attributes(G,'path')
        print("loop:{}\nnode_counts:{}\n".format(k,node_counts))
        #print(node_path)
        for i in range(height):
            for j in range(imax):
                if (Mnode[i][j]=='1'):
                    p=floor[i]
                    p+=str(j)
                    #print(p)
                    letsgo(G,p,'C1')
    #letsgo(G,'A1','C0',5)
    #plt.ioff()
    #print(G[1][5])
    #Graph_show(G)

    
