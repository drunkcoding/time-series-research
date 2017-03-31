from method.InitMethod import stock_base_data, combine_excels, select_data
from method.DCCA import MF_DCCA
from method.DFA import MF_DFA
import pandas as pd
import numpy as np
import os
dir_base = 'data\\Chinese_Stock\\'

#stock_base = stock_base_data(time = 20000000)
#print(stock_base.keys())

#stock_base = pd.read_excel(dir_base+'stock_base.xlsx', converters={'code': lambda x: str(x)})
#select_data(stock_base)

#df = combine_excels(dir_base+'data_code\\')

#df.to_excel(dir_base+'merged.xlsx')
data_dir = dir_base + 'data_code\\'
files = os.listdir(data_dir)
num_files = len(files)
for i in range(num_files):
    for j in range(i+1,num_files):
        tmp_df1 = pd.read_excel(data_dir + files[i])
        tmp_df2 = pd.read_excel(data_dir + files[j])
        tmp, tmp_dfx, tmp_dfy = combine_excels(tmp_df1, tmp_df2)
        func_dcca = MF_DCCA(-5, 5, 1, tmp)
        func_dfax = MF_DFA(-5, 5, 1, tmp_dfx)
        func_dfay = MF_DFA(-5, 5, 1, tmp_dfy)
