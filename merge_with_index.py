from method.InitMethod import stock_base_data, combine_excels, select_data
from method.DCCA import MF_DCCA
from method.DFA import MF_DFA
import pandas as pd
import numpy as np
import tushare as ts
import os

dir_base = 'data\\Chinese_Stock\\'
data_dir = dir_base + 'data_code\\'
lead_dir = dir_base + 'lead\\'
corr_dir = dir_base + 'corr\\'
dist_dir = dir_base + 'dist\\'

files = os.listdir(lead_dir)
num_files = len(files)
pop_list = ['open', 'high', 'low', 'volume', 'code']
sh = ts.get_k_data('sh', start='2000-01-01', autype=None)
for item in pop_list:
    try:
        del sh[item]
    except:
        pass
for file in files:
    tmp = pd.read_excel(lead_dir + file)
    for item in pop_list:
        del tmp[item]
    df = pd.merge(sh, tmp, on='date')
    del df['date']
    df.columns = ['X', 'Y']
    df = df.dropna()
    df.to_excel(dir_base + 'lead-sh\\' + file)
