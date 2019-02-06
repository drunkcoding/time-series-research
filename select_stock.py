from method.InitMethod import stock_base_data, combine_excels, select_data
import pandas as pd
import numpy as np
import os
import tushare as ts
dir_base = 'data\\Chinese_Stock\\'
data_dir = dir_base + 'data_code\\'
lead_dir = dir_base + 'lead\\'

#stock_base = stock_base_data(time = 20130000)

#stock_base = pd.read_excel(dir_base+'stock_base.xlsx', converters={'code': lambda x: str(x)})
#stock_base = stock_base.dropna()
#stock_base.to_excel(dir_base + 'lead.xlsx')
stock_base = pd.read_excel(dir_base + 'stock_oil.xlsx',
                           converters={'code': lambda x: str(x)})
select_data(stock_base, dic='oil_stock_data\\')

# tmp = ts.get_k_data("sh", start='2000-01-01', autype=None)
# tmp = ts.get_stock_basics()
# tmp = tmp.dropna()
# tmp.to_csv('oil_stock_data\\000001.SH.txt')

"""
files = os.listdir(data_dir)

for file in files:
    reader = pd.read_excel(data_dir + file)
    close = np.diff(np.log(reader['close'].values.tolist()))
    mean_t = np.mean(close)
    profile = np.cumsum(np.subtract(close, mean_t)).tolist()

    var = np.mean(np.multiply(profile, profile))
    df = pd.DataFrame([var]+profile, columns=['X'])
    df.to_csv(data_dir + file.split('.')[0] + '.csv')

"""
#df = combine_excels(dir_base+'data_code\\')

# df.to_excel(dir_base+'merged.xlsx')
