import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
    alfa = [method_dcca.alfa, method_dcca_rand.alfa, method_dcca_surr.alfa]
    f_alfa = [method_dcca.f_alfa, method_dcca_rand.f_alfa, method_dcca_surr.f_alfa]
    size_t = 10
    plt.figure()
    plt.scatter(alfa[0], f_alfa[0], s = size_t, c = 'b', edgecolors = 'none', label='origin')
    plt.scatter(alfa[1], f_alfa[1], s = size_t, c = 'r', edgecolors = 'none', label='random')
    plt.scatter(alfa[2], f_alfa[2], s = size_t, c = 'y', edgecolors = 'none', label='surrogate')
    plt.xlabel('alfa')
    plt.ylabel('f_alfa')
    plt.legend(loc = 'lower left')
    plt.savefig('graph\\'+ folder + filename +'.jpg')
    print(filename)
    print('origin', max(method_dcca.alfa)-min(method_dcca.alfa))
    print('random', max(method_dcca_rand.alfa)-min(method_dcca_rand.alfa))
    print('surrogate', max(method_dcca_surr.alfa)-min(method_dcca_surr.alfa))

current_dir = 'data'
for root, dirs, files in os.walk(current_dir):
    for file in files:
        estimate_fse(file, MF_DCCA, 'fse_dcca\\')
        estimate_fse(file, MF_DPXA, 'fse_dpxa\\')
