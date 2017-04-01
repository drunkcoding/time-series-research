from method.InitMethod import stock_base_data, combine_excels, select_data
import pandas as pd
import numpy as np
import os
dir_base = 'data\\Chinese_Stock\\'

stock_base = stock_base_data(time = 20000000)
#print(stock_base.keys())

stock_base = pd.read_excel(dir_base+'stock_base.xlsx', converters={'code': lambda x: str(x)})
select_data(stock_base)

#df = combine_excels(dir_base+'data_code\\')

#df.to_excel(dir_base+'merged.xlsx')