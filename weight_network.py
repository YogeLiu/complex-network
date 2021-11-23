import xlrd
import numpy as np
import networkx as nx

Node_Number = 340

def Read_matrix():
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

def Build_Graph(matrix):
    return nx.from_numpy_matrix(matrix)


def network_efficiency(graph):
    max = 0.0 
    length_list = list(nx.all_pairs_shortest_path_length(graph))
    total = 0.0
    for i in range(len(length_list)):
        length_map = length_list[i][1]
        for path_length in length_map.values():
            if max < path_length:
                max = path_length
            if path_length != 0:
                total += 1/path_length
    print(max)
    return total / Node_Number / (Node_Number - 1)



def weight_network_efficiency(graph):
    max_shortest_length, max_weight_shortest_length = 54, 5740996
    length_list = list(nx.all_pairs_dijkstra_path_length(graph))
    total = 0.0
    for i in range(len(length_list)):
        length_map = length_list[i][1]
        for path_length in length_map.values():
            if path_length != 0:
                path_length_normalization = round(path_length / max_weight_shortest_length * max_shortest_length)
                if path_length_normalization != 0.0:
                    total += 1/path_length_normalization
    return total / Node_Number / (Node_Number - 1)



def main():
    matrix = Read_matrix()
    graph = Build_Graph(matrix)
    print(weight_network_efficiency(graph))

if __name__ == '__main__':
    main()
