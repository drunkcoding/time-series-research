from method.InitMethod import stock_base_data, merge_excel, select_data
import pandas as pd
dict_base = 'data\\Chinese_Stock\\'

#stock_base = stock_base_data(time = 20000000)
#print(stock_base.keys())

stock_base = pd.read_excel(dict_base+'stock_base.xlsx', converters={'code': lambda x: str(x)})
select_data(stock_base)
df = merge_excel(dict_base+'data_code\\')

df.to_excel(dict_base+'merged.xlsx')

