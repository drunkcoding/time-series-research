from method.DCCA import MF_DCCA
from method.DPXA import MF_DPXA
from method.DFA import MF_DFA
import tushare as ts
import pandas as pd
import numpy as np
import os
dir_base = 'data/Chinese_Stock/'
data_dir = dir_base + 'data_code/'
lead_dir = dir_base + 'lead/'
corr_dir = dir_base + 'corr_dcca/'
dist_dir = dir_base + 'dist_dcca/'
oil_list = dir_base + 'oil/'
dpxa_list = dir_base + 'lead-sh/'

files = os.listdir(oil_list)
files.sort()
num_files = len(files)
step_list = [5, 10, 20, 40, 60, 120, 245, 500, 750, 1250, 1750]
unit_list = [[1.0 for i in range(num_files)] for j in range(num_files)]

s_len = len(step_list)
dcca_m = [[[1.0 for j in range(num_files)]
           for i in range(num_files)] for k in range(s_len)]
for i in range(num_files):
    for j in range(i + 1, num_files):
        #tmp = pd.merge(df_list[files[i]], df_list[files[j]], on='date')
        #tmp = pd.merge(tmp, sh, on='date')
        #del tmp['date']
        #tmp = tmp.dropna()
        #tmp.columns = ['X', 'Y', 'Z']
        tmp = pd.read_excel(dir_base + 'oil-down/' +
                            files[i].split('.')[0] + '-' + files[j])
        func_dcca = MF_DCCA(-5, 5, 10, tmp)
        func_dcca.corr_coef()
        cov_dcca = func_dcca.coef_list
        for k in range(s_len):
            dcca_m[k][i][j] = cov_dcca[k]
            dcca_m[k][j][i] = cov_dcca[k]
        #print(files[i] + files[j])
        # print(cov_dcca)

for i in range(s_len):
    df_corr = pd.DataFrame(dcca_m[i], columns=files, index=files)
    df_corr.to_excel(corr_dir + 'dpxa_corr_down' + str(step_list[i]) + '.xlsx')
    print i, "corr"
    dist = np.sqrt(np.multiply(2, np.subtract(unit_list, dcca_m[i])))
    df_dist = pd.DataFrame(dist, columns=files, index=files)
    df_dist.to_excel(dist_dir + 'dpxa_dist_down' + str(step_list[i]) + '.xlsx')
    print i, "dist"
