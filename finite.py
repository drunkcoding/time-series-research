import pandas as pd
import numpy as np

from method.DPXA import MF_DPXA
from method.DCCA import MF_DCCA
from method.surrogate import FSE_init

reader, reader_rand, reader_surr = FSE_init('data\\period1_1.csv')
#print(reader, reader_rand, reader_surr)