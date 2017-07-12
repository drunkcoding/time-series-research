from method.DCCA import MF_DCCA
from method.DFA import MF_DFA
import pandas as pd
import numpy as np
#import tushare as ts
import os

dir_base = 'data\\Chinese_Stock\\'
data_dir = dir_base + 'data_code\\'
lead_dir = dir_base + 'lead\\'
corr_dir = dir_base + 'corr_dpxa\\'
dist_dir = dir_base + 'dist_dpxa\\'
oil_list = dir_base + 'oil\\'
dpxa_list = dir_base + 'lead-sh\\'

files = os.listdir(oil_list)
num_files = len(files)
pop_list = ['open', 'high', 'low', 'volume', 'code']

sh = pd.read_excel(dir_base + 'sh_13-15.xlsx')


df_list = {}
pop_list = ['open', 'high', 'low', 'volume', 'code']
for file in files:
    tmp = pd.read_excel(oil_list + file)
    for item in pop_list:
        del tmp[item]
    df_list[file] = tmp


for i in range(num_files):
    for j in range(i + 1, num_files):
        tmp = pd.merge(df_list[files[i]], df_list[files[j]], on='date')
        tmp = pd.merge(tmp, sh, on='date')
        del tmp['date']
        tmp = tmp.dropna()
        tmp.columns = ['X', 'Y', 'Z']
        tmp.to_excel(dir_base + 'oil-up\\' +
                     files[i].split('.')[0] + '-' + files[j])
"""
for file in files:
    tmp = pd.read_excel(lead_dir + file)
    for item in pop_list:
        del tmp[item]
    df = pd.merge(sh, tmp, on='date')
    del df['date']
    df.columns = ['X', 'Y']
    df = df.dropna()
    df.to_excel(dir_base + 'lead-sh\\' + file)
"""
