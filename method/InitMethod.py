import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.regression.linear_model import OLS

def partition(list_t, step_t, num_wins):
    len_t = len(list_t)
    a = [list_t[i:i+step_t] for i in range(0,len_t,step_t)]
    list_t.reverse()
    b = [list_t[i:i+step_t] for i in range(0,len_t,step_t)]
    if num_wins*step_t != len_t:
        a.pop()
        b.pop()
    return a+b

def merge_excel(dirct, key):
    tmp_excels = []
    for root, dirs, files in os.walk(dirct):
        for file in files:
            tmp_excels.append(pd.read_excel(dirct + file))
    tmp = pd.merge(tmp_excels[0], tmp_excels[1], on=key)
    for i in range(2, len(tmp_excels)): tmp = pd.merge(tmp, tmp_excels[i], on=key)
    return tmp

def unit_root_test(df, remove = None):
    for key in remove: del df[key]
    check = lambda x: True if len(x)==0 else max(x) < 0
    orders = {}
    for key in df:
        index = 0
        series = df[key].values
        while True:
            if index>0: series = np.diff(series)
            result = adfuller(series)
            hypo = result[i][0]-result[i][4]['1%']
            index += 1
            if hypo < 0: break
        orders[index-1].append(series)
    return orders
    

