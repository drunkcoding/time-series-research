import pandas as pd
import numpy as np

from method.DPXA import MF_DPXA
from method.DCCA import MF_DCCA
from method.surrogate import FSE_init

reader, reader_rand, reader_surr = FSE_init('data\\period1_1.csv')
method_dcca = MF_DCCA(-5, 5, 1, reader)
method_dcca_rand = MF_DCCA(-5, 5, 1, reader_rand)
method_dcca_surr = MF_DCCA(-5, 5, 1, reader_surr)
method_dcca.generate()
method_dcca_rand.generate()
method_dcca_surr.generate()
hurst_list = [method_dcca.hurst_list, method_dcca_rand.hurst_list, method_dcca_surr.hurst_list]
for line in hurst_list: print(line)
#print(reader, reader_rand, reader_surr)