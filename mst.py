import pandas as pd
import numpy as np
import networkx as nx
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt

dir_base = 'data\\Chinese_Stock\\'

#dist = pd.read_excel(dir_base + 'dist.xlsx')
#A = scipy.sparse.csr_matrix(dist.values.tolist())
A = csr_matrix([[1, 0.8, 0.9], [0.8, 1, 0.7], [0.9, 0.7, 1]])
G = nx.from_scipy_sparse_matrix(A, create_using=nx.MultiGraph())

T = nx.minimum_spanning_tree(G)
plt.figure()
nx.draw_networkx(T, pos=nx.spring_layout(T), with_labels=False, node_size = 15)
plt.show()