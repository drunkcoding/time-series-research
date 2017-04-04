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
files = os.listdir(lead_dir)
num_files = len(files)



for file in dists:
    dist = pd.read_excel(dist_dir + file)
    A = csr_matrix(dist.values.tolist())
    #A = csr_matrix([[1, 0.8, 0.9], [0.8, 1, 0.7], [0.9, 0.7, 1]])
    G = nx.from_scipy_sparse_matrix(A, create_using=nx.MultiGraph())

    T = nx.minimum_spanning_tree(G)
    labels = {}
    cnt = 0
    for node in T.nodes():
        labels[node] = files[cnt].split('.')[0]
        cnt += 1
    plt.figure()
    nx.draw_networkx(T, pos=nx.spring_layout(T), with_labels=False, node_size = 15)
    nx.draw_networkx_labels(T, nx.spring_layout(T), labels, font_size=6,font_color='r')
    #plt.show()
    plt.savefig('graph\\\mst\\' + file.split('.')[0] + '.jpg')