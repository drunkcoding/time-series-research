import pandas as pd
import numpy as np
import os
import networkx as nx
from scipy.sparse import csr_matrix
from scipy.stats import pearsonr
import matplotlib.pyplot as plt

dir_base = 'data\\Chinese_Stock\\'
data_dir = dir_base + 'data_code\\'
lead_dir = dir_base + 'lead\\'
corr_dir = dir_base + 'corr\\'
dist_dir = dir_base + 'dist\\'

"""
files = os.listdir(lead_dir)
num_files = len(files)
unit_list = [[1.0 for i in range(num_files)] for j in range(num_files)]

pear_m = [[1.0 for j in range(num_files)] for i in range(num_files)]

df_list = {}
pop_list = ['open', 'high', 'low', 'volume', 'code']
for file in files: 
    tmp = pd.read_excel(lead_dir + file)
    for item in pop_list: del tmp[item]
    df_list[file] = tmp

for i in range(num_files):
    for j in range(i+1, num_files):
        tmp = pd.merge(df_list[files[i]], df_list[files[j]], on='date')
        del tmp['date']
        tmp = tmp.dropna()
        tmp.columns = ['X', 'Y']
        r, prob = pearsonr(tmp.X.values, tmp.Y.values)
        pear_m[i][j] = pear_m[j][i] = r

df_corr = pd.DataFrame(pear_m, columns=files, index=files)
df_corr.to_excel(dir_base+'pear_corr.xlsx')
dist = np.sqrt(np.multiply(2, np.subtract(unit_list, pear_m)))
df_dist = pd.DataFrame(dist, columns=files, index=files)
df_dist.to_excel(dir_base+'pear_dist.xlsx')
"""

df_dist = pd.read_excel(dir_base+'pear_dist.xlsx')
A = csr_matrix(df_dist.values.tolist())
G = nx.from_scipy_sparse_matrix(A, create_using=nx.MultiGraph())
T = nx.minimum_spanning_tree(G)
pos_t = nx.fruchterman_reingold_layout(T)
plt.figure()
nx.draw_networkx(T, pos=pos_t, with_labels=True, node_size = 18, alpha=0.6)
plt.savefig('graph\\pear.jpg')