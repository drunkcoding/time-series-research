from method.InitMethod import stock_base_data, combine_excels, select_data
import pandas as pd
import numpy as np
import os
dir_base = 'data\\Chinese_Stock\\'
data_dir = dir_base + 'data_code\\'


#stock_base = stock_base_data(time = 20000000)

stock_base = pd.read_excel(dir_base+'stock_base.xlsx', converters={'code': lambda x: str(x)})
select_data(stock_base)
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

#df.to_excel(dir_base+'merged.xlsx')