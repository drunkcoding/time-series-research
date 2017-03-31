import pandas as pd
import numpy as np
import tushare as ts
import os
from statsmodels.tsa.stattools import adfuller
from statsmodels.regression.linear_model import OLS
from sklearn.preprocessing import normalize

def partition(list_t, step_t, num_wins):
    len_t = len(list_t)
    a = [list_t[i:i+step_t] for i in range(0,len_t,step_t)]
    list_t.reverse()
    b = [list_t[i:i+step_t] for i in range(0,len_t,step_t)]
    if num_wins*step_t != len_t:
        a.pop()
        b.pop()
    return a+b

def merge_excel(dirct, key='date'):
    tmp_excels = []
    for root, dirs, files in os.walk(dirct):
        for file in files:
            tmp_excels.append(pd.read_excel(dirct + file))
    tmp = pd.merge(tmp_excels[0], tmp_excels[1], on=key)
    for i in range(2, len(tmp_excels)): tmp = pd.merge(tmp, tmp_excels[i], on=key)
    return tmp

def combine_excels(df1, df2, key='close'):
    new_data = lambda df, label: pd.DataFrame(np.transpose([df.date.values, df[key].values]), \
    columns=['date', label])
    tmp_df1 = new_data(df1, 'X')
    tmp_df2 = new_data(df2, 'Y')
    tmp_dfx = new_data(df2, 'X')
    tmp = pd.merge(tmp_df1, tmp_df2, on='date')        
    return tmp, tmp_df1, tmp_dfx

def unit_root_test(df, remove = None):
    for key in remove: del df[key]
    #check = lambda x: True if len(x) == 0 else max(x) < 0
    orders = {}
    for key in df:
        index = 0
        series = df[key].values
        while True:
            if index > 0: series = np.diff(series)
            result = adfuller(series)
            hypo = result[i][0]-result[i][4]['1%']
            index += 1
            if hypo < 0: break
        orders[index-1].append(series)
    return orders

def cointegration_test(s1, s2):
    if (len(s1) != len(s2)): return None
    reg = OLS(s1, s2).fit()
    residual = lambda param, y, x: np.subtract(y, np.multiply(param, x))
    result = adfuller(residual(reg.params, s1, s2))
    return (result[i][0]-result[i][4]['1%']) < 0

def subtract_mean(L):
    mean_t = np.mean(L)
    return np.subtract(L, mean_t)

def stock_base_data(dic='data\\Chinese_Stock\\', time=0):
    """
    return selected stock code and general data
    """
    stock_base = ts.get_stock_basics()
    length = len(stock_base.index)
    drop_list = [x for x in range(length) \
    if stock_base['holders'][x] == 0 or stock_base['timeToMarket'][x] >= time]
    #print (drop_list)
    stock_base = stock_base.drop(stock_base.index[drop_list])
    #length = len(stock_base['pe'])
    #df = pd.DataFrame(index=[x for x in range(length)])
    #stock_base.insert(0, 'index', [x for x in range(length)])
    #stock_base = pd.merge(df, stock_base)
    stock_base.dropna()
    stock_base.to_excel(dic + 'stock_base.xlsx')
    return stock_base

def select_data(df, dic='data\\Chinese_Stock\\data_code\\'):
    code_list = df.code.values
    #print(code_list)
    for x in code_list:
        #print(x)
        try:
            tmp = ts.get_k_data(x, start='2000-01-01')
        except:
            pass
        tmp = tmp.dropna()
        tmp.to_excel(dic+x+'.xlsx')


class MAP(object):
    def __init__(self, reader, remove = None):
        self.reader = reader.dropna()
        self.reader.dropna()
        for key in remove: del self.reader[key]

    def score(self, edges, X):
        tmp_e = deepcopy(edges)
        tmp_e.append(X)
        tmp_e = sorted(tmp_e)
        cnt = 0
        while X > tmp_e[cnt]: 
            cnt += 1
            if cnt == len(tmp_e): break
        return cnt+1

    def try_t(self, Indx, L, step_t):
        tmp = sorted(L[Indx-step_t:Indx])
        return score(tmp, L[Indx])

    def generate(self, step_t):
        make = lambda L: [try_t(i, L, step_t) for i in range(step_t, length)]
        total = [make(self.reader[key].values) for key in self.reader]
        total = normalize(total, norm='max')
        return total, [key for key in self.reader]


