import pandas as pd
import numpy as np
import networkx as nx
from scipy.sparse import csr_matrix

dir_base = 'data\\Chinese_Stock\\'

dist = pd.read_excel(dir_base + 'dist.xlsx')
A = scipy.sparse.csr_matrix(dist.values.tolist())
G = nx.from_scipy_sparse_matrix(A, create_using=nx.MultiGraph())
