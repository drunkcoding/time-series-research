import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

from statsmodels.tsa.stattools import acf

reader = pd.read_excel('close.xlsx')
reader = reader.dropna()
close = reader['close'].values
ran_list = np.random.rand(3000)
print(ran_list)
ran_list.sort()
test = np.sin(ran_list)
print(test)
plt.figure()
plt.acorr(test[0], maxlags = 10)
plt.show()