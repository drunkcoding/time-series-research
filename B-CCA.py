import pandas as pd
import numpy as np
import os

from method.DPXA import MF_DPXA
from method.DCCA import MF_DCCA
from method.surrogate import FSE_init


def estimate_fse(filename, class_t, folder):
    reader, reader_rand, reader_surr = FSE_init('data\\' + filename)
    method_dcca = class_t(-5, 5, 10, reader)
    method_dcca_rand = class_t(-5, 5, 10, reader_rand)
    method_dcca_surr = class_t(-5, 5, 10, reader_surr)
    method_dcca.generate()
    method_dcca_rand.generate()
    method_dcca_surr.generate()
    print(filename)
    print('origin', max(method_dcca.alfa) - min(method_dcca.alfa))
    print('random', max(method_dcca_rand.alfa) - min(method_dcca_rand.alfa))
    print('surrogate', max(method_dcca_surr.alfa) - min(method_dcca_surr.alfa))
    return method_dcca.hurst_list


for i in range(10):
    estimate_fse("period1_2.csv", MF_DCCA, 'fse_dcca\\')