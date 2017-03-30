from method.InitMethod import stock_base_data, merge_excel, select_data

dict_base = 'data\\Chinese_Stock\\'

#stock_base = stock_base_data(time = 20000000)
#print(stock_base.keys())
stock_base = pd.read_excel(dict_base+'stock_base.xlsx')
select_data(stock_base)
df = merge_excel(dict_base+'data_code\\')

df.to_excel(dict_base+'merged.xlsx')

