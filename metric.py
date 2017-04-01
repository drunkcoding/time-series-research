from method.InitMethod import stock_base_data, combine_excels, select_data
from method.DCCA import MF_DCCA
from method.DFA import MF_DFA
import pandas as pd
import numpy as np
import os
dir_base = 'data\\Chinese_Stock\\'
data_dir = dir_base + 'data_code\\'
files = os.listdir(data_dir)
num_files = len(files)
dcca_m = [[-2 for j in range(num_files)] for i in range(num_files)]
for i in range(num_files):
    dcca_m[i][i] = 1.0
    for j in range(i+1,num_files):
        tmp_df1 = pd.read_excel(data_dir + files[i])
        tmp_df2 = pd.read_excel(data_dir + files[j])
        tmp, tmp_dfx, tmp_dfy = combine_excels(tmp_df1, tmp_df2)
        func_dcca = MF_DCCA(-5, 5, 1, tmp)  
        #func_dfax = MF_DFA(-5, 5, 1, tmp_dfx)
        #func_dfay = MF_DFA(-5, 5, 1, tmp_dfy)
        #func_dcca.generate()
        #func_dfax.generate()
        #func_dfay.generate()
        func_dcca.corr_coef()
        cov_dcca = func_dcca.cov_list
        dcca_m[i][j] = cov_dcca
        dcca_m[j][i] = cov_dcca
        #cov_dfax = func_dcca.cov_list
        #cov_dfay = func_dcca.cov_list
        #coef = np.divide(cov_dcca, np.sqrt(np.multiply(cov_dfax, cov_dfay)))
        print(cov_dcca)

df_corr = pd.DataFrame(dcca_m, columns=files, index=files)
df_corr.to_excel(dir_base + 'corr.xlsx')

dist = np.sqrt(np.multiply(2, np.subtract(1, df_corr)))
df_dist = pd.DataFrame(dcca_m, columns=files, index=files)
df_dist.to_excel(dir_base + 'dist.xlsx')

