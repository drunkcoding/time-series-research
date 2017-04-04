import pandas as pd
import numpy as np
import os
import networkx as nx
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt

dir_base = 'data\\Chinese_Stock\\'
lead_dir = dir_base + 'lead\\'
dist_dir = dir_base + 'dist\\'
dists = os.listdir(dist_dir)

reader = pd.read_excel(dir_base + 'lead.xlsx', converters={'code': lambda x: str(x)})
code_list = reader.code.values.tolist()
dist = pd.read_excel(dist_dir + 'dist_5.xlsx')
files = dist.columns.values.tolist()
drop_list = [files.index(item + '.xlsx') for item in code_list]
remove_name = [files[num] for num in drop_list]
print(code_list)
print(drop_list)
print(len(files))
for file in dists:
    dist = pd.read_excel(dist_dir + file)
    A = csr_matrix(dist.values.tolist())
    G = nx.from_scipy_sparse_matrix(A, create_using=nx.MultiGraph())
    tmp_files = files
    for num in drop_list:
        G.remove_node(num)
        print(num)
        tmp_files.remove(remove_name[num])
        T = nx.minimum_spanning_tree(G)
        pos_t = nx.spring_layout(T)
        labels = {}
        cnt = 0
        for node in T.nodes():
            labels[node] = tmp_files[cnt].split('.')[0]
            cnt += 1
        plt.figure()
        nx.draw_networkx(T, pos=pos_t, with_labels=False, node_size = 18, alpha=0.6)
        nx.draw_networkx_labels(T, pos_t, labels, font_size=7,font_color='b')
        #plt.show()
        plt.savefig('graph\\\mst_inc\\' + file.split('.')[0] + str(num) + '.jpg')

    """
    for item in code_list:
        print(item)
        G.remove_node(files.index(item + '.xlsx'))
        print(G.nodes())
        tmp_files.remove(item + '.xlsx')
        T = nx.minimum_spanning_tree(G)
        pos_t = nx.spring_layout(T)
        labels = {}
        cnt = 0
        for node in T.nodes():
            labels[node] = tmp_files[cnt].split('.')[0]
            cnt += 1
        plt.figure()
        nx.draw_networkx(T, pos=pos_t, with_labels=False, node_size = 18, alpha=0.6)
        nx.draw_networkx_labels(T, pos_t, labels, font_size=7,font_color='b')
        #plt.show()
        plt.savefig('graph\\\mst_inc\\' + file.split('.')[0] + item + '.jpg')
    """

