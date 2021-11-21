from re import I
import re
import networkx as nx
from networkx.classes.function import degree
import xlrd
import numpy as np
import matplotlib.pyplot as plt
import random
import threading
import copy

def ReadWeightMatrix():
    data = xlrd.open_workbook(r'H:\LYC\中期\数据\L\weight_symmetric_matrix.xlsx')
    worksheet = data.sheets()[0]
    row = worksheet.nrows
    cols = worksheet.ncols
    matrix = np.zeros((row, row))
    for i in range(cols):
        col_data = worksheet.col_values(i)
        matrix[:, i] = col_data
    print(matrix.shape)
    return matrix

def BuildWeightGraph(matrix):
    graph = nx.from_numpy_matrix(matrix)
    return graph

def Cacl_Weight_Degree(graph):
    degree = nx.degree(graph, weight='weight')
    print(degree)
    degree_broken_4000 = list(range(200))
    for i in range(200):
        degree_broken_4000[i] = 0
    y = []
    sum = 0
    for i in range(len(degree)):
        val = int(degree[i])
        sum += val
        index = (int) (val / 10000)
        degree_broken_4000[index] += 1
    print(sum, sum/340)
    print(degree_broken_4000)

    degree_values = {}
    for i in range(len(degree)):
        v = degree[i] / 10000.0
        if degree_values.get(v) is None:
            degree_values[v] = 1
        else:
            value = degree_values[v]
            value += 1
            degree_values[v] = value
    return degree_values

# 加权平均路径长度
def Weight_Ave_Length(graph):
    length = list(nx.all_pairs_dijkstra_path_length(graph))
    length_map = {}
    max = 5740996.0
    for i in range(len(length)):
        for val in length[i][1].values():
            key = round(val/max*54)
            if length_map.get(key) == None:
                length_map[key] = 1
            else:
                value = length_map[key]
                value += 1
                length_map[key] = value
    # print(length_map)
    lengths = []
    for val in length_map.keys():
        lengths.append(val)
    count = []
    for val in length_map.values():
        count.append(val)
    print(lengths)
    print(count)    

# 点介数,返回按点介数降序的节点索引
def static_between_centrality_point(graph):
    point = nx.betweenness_centrality(graph, weight='weight')
    sorted_point = sorted(point.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    points = []
    for i in range(len(sorted_point)):
        points.append(sorted_point[i][0])
    return points


# 边介数，返回按边介数降序的节点索引
def static_between_centrality_edge(graph):
    edge = nx.edge_betweenness_centrality(graph, weight='weight')
    sorted_edge = sorted(edge.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    points_map = {}
    points = []
    for i in range(len(sorted_edge)):
        for j in range(2):
            if points_map.get(sorted_edge[i][0][j]) is None:
                points_map[sorted_edge[i][0][j]] = True
                points.append(sorted_edge[i][0][j])
    return points

#点强度，按照点强度返回节点索引
def static_degree_intensity_point(graph):
    point_degree = nx.degree(graph, weight='weight')
    points_map = {}
    for i in range(len(point_degree)):
        points_map[i] = point_degree[i]
    sorted_point = sorted(points_map.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    points = []
    for i in range(len(sorted_point)):
        points.append(sorted_point[i][0])
    return points

#按照随机返回节点索引
def random_points():
    nodes = random.sample(list(range(340)), 340)
    return nodes


# 计算联通子图
def static_network_scale(graph, node_num):
    if len(list(nx.connected_components(graph))) == 0:
        return 0.0
    else:
        return len(list(nx.connected_components(graph))[0])*1.0/node_num


# 计算平均路径长度
def static_shortes_path_length(graph):
    total = 0.0
    lengths = list(nx.all_pairs_dijkstra_path_length(graph))
    for i in range(len(lengths)):
        total += sum(lengths[i][1].values())
    if graph.number_of_nodes() == 1 or graph.number_of_nodes() == 0:
        return 0.0 
    return total / (graph.number_of_nodes() * (graph.number_of_nodes() - 1))

# 计算全局效率
def static_graph_efficiency(graph):
    return nx.global_efficiency(graph)


def attack(graph, attack_type='图规模'):
    if attack_type == '图规模':
        pass
    elif attack_type== '最短路径长度':
        pass
    else: 
        pass

# 抗毁性指标，最短路径长度
def attack_graph_shortest_path_length(graph):
    graphs = [copy.deepcopy(graph), copy.deepcopy(graph), copy.deepcopy(graph), copy.deepcopy(graph)]
    rets = list(range(4))
    for i in range(4):
        rets[i] = []
    #随机攻击, 点介数, 边介数, 点强度
    nodes_list = [random_points(), static_between_centrality_point(graph), static_between_centrality_edge(graph), static_degree_intensity_point(graph)]
    for i in range(len(nodes_list)):
        for node in nodes_list[i]:
            ret = static_shortes_path_length(graphs[i])
            rets[i].append(ret)
            graphs[i].remove_node(node)    
    for ret in rets:
        val = ret[0]
        for i in range(len(ret)):
            ret[i] /= val
    return rets


# 抗毁性指标，网络规模
def attack_graph_sacle(graph):
    graphs = [copy.deepcopy(graph), copy.deepcopy(graph), copy.deepcopy(graph), copy.deepcopy(graph)]
    rets = list(range(4))
    for i in range(4):
        rets[i] = []
    #随机攻击, 点介数, 边介数, 点强度
    nodes_list = [random_points(), static_between_centrality_point(graph), static_between_centrality_edge(graph), static_degree_intensity_point(graph)]
    for i in range(len(nodes_list)):
        for node in nodes_list[i]:
            ret = static_network_scale(graphs[i], 340)
            rets[i].append(ret)
            graphs[i].remove_node(node)    
    for ret in rets:
        ret[0] = 1.0
    return rets

# 抗毁性指标，全局效率
def attack_efficiency(graph):
    graphs = [copy.deepcopy(graph), copy.deepcopy(graph), copy.deepcopy(graph), copy.deepcopy(graph)]
    rets = list(range(4))
    for i in range(4):
        rets[i] = []
    thread_list = []
     #随机攻击, 点介数, 边介数, 点强度
    nodes_list = [random_points(), static_between_centrality_point(graph), static_between_centrality_edge(graph), static_degree_intensity_point(graph)]
    for i in range(len(nodes_list)):
        thread_list.append(threading.Thread(target=attack_efficiency_thread, args=(graphs[i], nodes_list[i], i, rets)))
        # for node in nodes_list[i]:
        #     ret = static_graph_efficiency(graphs[i])
        #     rets[i].append(ret) 
        #     graphs[i].remove_node(node)   

    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()
    return rets

# 开启线程
def attack_efficiency_thread(graph, nodes, index, ret_all):
    rets = []
    for i in range(len(nodes)):
        ret = static_graph_efficiency(graph)
        rets.append(ret)
        graph.remove_node(nodes[i])
    ret_all[index] = rets


def draw(variales, ylabel):
    if len(variales) != 4:
        return
    plt.plot(range(len(variales[0])), variales[0], label='随机攻击')
    plt.plot(range(len(variales[1])), variales[1], label="基于点介数攻击")
    plt.plot(range(len(variales[2])), variales[2], label='基于边介数攻击')
    plt.plot(range(len(variales[3])), variales[3], label='基于点强度攻击')
    plt.xlabel("攻击站点个数")
    plt.ylabel(ylabel)
    plt.legend(loc='upper right')
    plt.show()

def main():
    matirx = ReadWeightMatrix()
    graph = BuildWeightGraph(matirx)
    # degree = Cacl_Weight_Degree(graph)
    # rets = attack_graph_sacle(graph)
    draw(attack_efficiency(graph), '全局效率')

if __name__ == "__main__":
    main()
    