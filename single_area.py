from method.InitMethod import stock_base_data, combine_excels, select_data
from method.DCCA import MF_DCCA
from method.DFA import MF_DFA
import pandas as pd
import numpy as np
import os
dir_base = 'data\\Chinese_Stock\\'
data_dir = dir_base + 'data_code\\'
lead_dir = dir_base + 'lead\\'
corr_dir = dir_base + 'corr\\'
dist_dir = dir_base + 'dist\\'

files = os.listdir(lead_dir)
num_files = len(files)
step_list = [5, 10, 20, 40, 60, 120, 245, 500, 750, 1250, 1750]
unit_list = [[1.0 for i in range(num_files)] for j in range(num_files)]

s_len = len(step_list)
dcca_m = [[[1.0 for j in range(num_files)]
           for i in range(num_files)] for k in range(s_len)]
           for i in range(num_files)] for k in range(s_len)]

df_list = {}
for file in files:
for file in files:
    for item in pop_list:
        del tmp[item]
    for item in pop_list:
        del tmp[item]
    for j in range(i + 1, num_files):
for i in range(num_files):
    for j in range(i + 1, num_files):
        tmp = pd.merge(df_list[files[i]], df_list[files[j]], on='date')
        del tmp['date']
        func_dcca = MF_DCCA(-5, 5, 1, tmp)
        tmp.columns = ['X', 'Y']
        func_dcca = MF_DCCA(-5, 5, 1, tmp)
        func_dcca.corr_coef()
        cov_dcca = func_dcca.cov_list
        for k in range(s_len):
        print(files[i] + files[j], end=' ')
            dcca_m[k][j][i] = cov_dcca[k]
        print(files[i] + files[j], end=' ')
        print(cov_dcca, flush=True)

for i in range(s_len):
    df_corr = pd.DataFrame(dcca_m[i], columns=files, index=files)
    df_corr.to_excel(corr_dir + 'corr_' + str(step_list[i]) + '.xlsx')
    dist = np.sqrt(np.multiply(2, np.subtract(unit_list, dcca_m[i])))
    df_dist = pd.DataFrame(dist, columns=files, index=files)
    df_dist.to_excel(dist_dir + 'dist_' + str(step_list[i]) + '.xlsx')
