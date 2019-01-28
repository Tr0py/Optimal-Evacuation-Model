# coding:utf-8

# 美赛D题线路规划


'''
Demo branch
'''

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
height=3
imax=7
elevator_rate=int(2)
node_in=open("test_node_in.txt","r")
hori_in=open("test_hori_in.txt","r")
exit_count_out=open("test_exit_count.csv","w")
cost_count_out=open("test_cost.csv","w")
Mnode=node_in.readlines()
Mhori=hori_in.readlines()
dstlist=['A4']
OUTPUT=0
NEEDOUT=1
roundCount=0
# 纵向需要显示权重的边
hori_edges=[]
# 初始化图，添加点与边
def Graph_init(G,count_in):
    floor=['A','B','C','D','E']
    colors=['r','y','g','c','m']

    for i in range(height):
        Mnode[i]=Mnode[i].strip().split(' ')
    print(Mnode)
    global hori_edges
    node_sum=0
    for i in range(height):
        for j in range(imax):
            print("i:{} j:{}".format(i,j))
            if (Mnode[i][j]=='1'):
                node_num=i*imax+j
                G.add_node(node_num,pos=(j,i),label=(floor[i]+str(j)),color=i,count=count_in,path=[],dst=0,nowdst='',cost=0,people=count_in)
                node_sum+=1
                
                print("add node:{}".format(node_num))
                colorlist.append(colors[i])
                if ((i>0) and (Mnode[i-1][j]=='1')):
                    G.add_edge(node_num,node_num-imax,weight=1)
                    hori_edges.append((node_num,node_num-imax))
                    #print("add edge:{}->{}".format(node_num,node_num-imax))
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
    G.remove_edge(4,11)
    print("{}".format(node_sum))

def add_horizontal_weights():
    j=0
    for i in Mhori:        
        Mhori[j]=Mhori[j].strip().split(' ')
        #print(Mhori[j])
        src=Mhori[j][0]
        dst=Mhori[j][1]
        w=int(int(Mhori[j][2]))
        #for src,dst,w in Mhori[j]:
        #print("change_weight:{}->{}:{}".format(src,dst,w-1))
        #change_weight(G,l2n(src),l2n(dst),w-1)
        #print("add_edge3:{}->{}:{}".format(src,dst,w))
        G.add_edge(l2n(src),l2n(dst),weight=w)
        j+=1
    #print(Mhori)
    #exit()
    
# 画出G的点、边及其属性
def Graph_show(G):
    e_labels = nx.get_edge_attributes(G,'weight')
    global roundCount
    #roundCount+=1
    #print("roundCount:{}".format(roundCount))
    #print("roundCount:{} roundCount%10:{}".format(roundCount,(roundCount%10)))
    plt.figure(1,figsize=(7,2))
    nx.draw(G,pos)
    print(e_labels)
    vertical_labels={}
    horizontal_labels={}
    for a in e_labels:
        #print(a)
        
        b=e_labels[a]
        #print(a[0],a[1],b)
        #Ax->Bx 纵向边
        if (n2l(a[0])[0]!=n2l(a[1])[0]):
            #print("1")
            #print("add dict:{}->{}".format(n2l(a[0]),n2l(a[1])))
            vertical_labels[a]=b
        else:
            horizontal_labels[a]=b
    #print(vertical_labels)

        #print("x:{}y:{}b:{}".format(a[0],a[1],b))
    
    '''
    nx.draw_networkx_edge_labels(G,pos,edge_labels=e_labels)
    nx.draw_networkx_edge_labels(G,pos,edge_labels=vertical_labels,font_color='r',edge_color='r')
    '''
    nx.draw_networkx_edge_labels(G,pos,edge_labels=horizontal_labels)


    #nx.draw_networkx_edges(G,pos,edgelist=hori_edges)
    nx.draw_networkx(G, pos, labels=node_labels,font_size=10,node_color=colorlist)
    G.edges(data=True)
    #plt.figure(figsize=(6, 6.5))
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
    
def letsgo(G,src,dstlist):
    global node_counts
    #print("banjjjjjjjjjjjjjju:{}->{}".format(src,dst))
    # 清除上次的path

    #清除dstcount
    nowdst=G.nodes[l2n(src)]['nowdst']
    if (nowdst!=''):
        count=node_counts[l2n(src)]
        #print("nowdst:{} dstcount:{} count:{}".format(nowdst,G.nodes[l2n(nowdst)]['dst'],-count))
        G.nodes[l2n(nowdst)]['dst']-=count
        #print("nowdst:{} dstcount:{}".format(nowdst,G.nodes[l2n(nowdst)]['dst']))

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
    minw=99999
    minpath=[]
    mindst=''
    for dst in dstlist:
        ret=get_shortest_path(G,l2n(src),l2n(dst))
        if (ret[1]<minw):
            minw=ret[1]
            minpath=ret[0]
            mindst=dst
    ret[1]=minw
    ret[0]=minpath
    count=node_counts[l2n(src)]

    
    G.nodes[l2n(mindst)]['dst']+=count
    #print("dst{}+{}".format(mindst,count))
    G.nodes[l2n(src)]['nowdst']=n2l(minpath[-1])
    G.nodes[l2n(src)]['cost']+=ret[1]
    leave=l2n(src)
    #f.write(str(count)+' w:'+str(ret[1])+' path:'+n2l(leave)+' dstCount:'+str(G.nodes[l2n(mindst)]['dst']))
    f.write("moved:{},cost:{},dstCount:{},path:{}".format(count,ret[1],G.nodes[l2n(mindst)]['dst'],n2l(leave)))
    for go in ret[0]:
        # 不会是第一个 A0->A0
        if (leave == go):
            continue
        #f.write(n2l(leave)+'->'+n2l(go))
        f.write('->'+n2l(go))
        #print(G[leave][go]['weight'])
        change_weight(G,leave,go,count*elevator_rate)
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


    exit_count_out.write("EXIT")
    for dst in dstlist:
        exit_count_out.write(",{}".format(dst))
    exit_count_out.write("\n")
    first=1
    for ei in range(20,21,1):
        print("BIGLOOP:{}....".format(ei))
        #elevator_rate=int(15/6)
        node_in=open("test_node_in.txt","r")
        hori_in=open("test_hori_in.txt","r")
        #exit_count_out=open("exit_count.csv","w+")
        Mnode=node_in.readlines()
        Mhori=hori_in.readlines()
        roundCount=0
        # 纵向需要显示权重的边
        hori_edges=[]



        G=nx.Graph()
        roundCount=0
        colorlist=[]
        Graph_init(G,ei+1)

        '''
        cost表头输出
        '''
        if (first):
            floor=['A','B','C','D','E']
            cost_count_out.write("NODE")
            for i in range(height):
                for j in range(imax):
                    if (Mnode[i][j]=='1'):
                        p=floor[i]
                        p+=str(j)
                        cost_count_out.write(",{}".format(p))
            cost_count_out.write("\n")
            first=0

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
        for k in range(15):
            
            if (k%3==1 and NEEDOUT==1):
                Graph_show(G)
                node_counts=nx.get_node_attributes(G,'count')
                node_path=nx.get_node_attributes(G,'path')
            if (node_counts[0]<=1):
                break
            #print("loop:{}\nnode_counts:{}\n".format(k,node_counts[1]))
            
            #print(node_path)
            for i in range(height):
                for j in range(imax):
                    if (Mnode[i][j]=='1'):
                        p=floor[i]
                        p+=str(j)
                        #print(p)
                        letsgo(G,p,dstlist)

        '''
        cost统计输出
        '''

        cost_count_out.write("NUM={}".format((ei+1)*81))
        costlist=nx.get_node_attributes(G,'cost')
        peoplelist=nx.get_node_attributes(G,'people')
        # print(costlist)
        # for i in costlist:
        #     costlist[i]=int(costlist[i]/peoplelist[i])
        #     #print("cost{}:{}".format(n2l(i),costlist[i]))
        #     cost_count_out.write("{}:{}".format(n2l(i),costlist[i]))
        
        for i in range(height):
            for j in range(imax):
                if (Mnode[i][j]=='1'):
                    floor=['A','B','C','D','E']
                    p=floor[i]
                    p+=str(j)
                    num=l2n(p)
                    costlist[num]=int(costlist[num]/peoplelist[num])
                    cost_count_out.write(",{}".format(costlist[num]))
        cost_count_out.write("\n")
        

        '''
        exit负荷统计输出
        '''
        exit_count_out.write("{}".format((ei+1)*81))
        for dst in dstlist:
            exit_count_out.write(",{}".format(G.nodes[l2n(dst)]['dst']))


        exit_count_out.write("\n")
    #print("{},{}".format(l2n('A4'),l2n('B4')))
    #letsgo(G,'A1','C0',5)
    #plt.ioff()
    #print(G[1][5])
    #Graph_show(G)
