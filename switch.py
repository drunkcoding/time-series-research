import pandas as pd
import numpy as np

from method.DPXA import MF_DPXA
from method.DCCA import MF_DCCA
from method.surrogate import FSE_init

point = 200
reader1 = pd.read_csv('period1_1.csv')
reader2 = pd.read_csv('period1_2.csv')
reader3 = pd.read_csv('period1_3.csv')

A = DPXA(-5, 5, 10, reader1)
index = A.flist.index(2.0)
A.generate()
print(A.hurst_list[index])
B = DPXA(-5, 5, 10, reader2)
B.generate()
C = DPXA(-5, 5, 10, reader3)
C.generate()
#df.iloc[np.random.permutation(len(df))]