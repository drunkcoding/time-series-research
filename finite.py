import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from method.DCCA import MF_DCCA
from method.CCA import MF_CCA
from method.surrogate import FSE_init


def print_graph(filename, folder, x, y, labels, label_x, label_y, scale, locate='lower left'):
    size_t = 10
    plt.figure()
    plt.scatter(x[0], y[0], s=size_t, c='b',
                edgecolors='none', label=labels[0])
    plt.scatter(x[1], y[1], s=size_t, c='r',
                edgecolors='none', label=labels[1])
    plt.scatter(x[2], y[2], s=size_t, c='y',
                edgecolors='none', label=labels[2])
    plt.axis(scale)
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.legend(loc=locate)
    plt.savefig('graph\\' + folder + filename.split('.')[0] + '.jpg')
    plt.close()


def estimate_fse(filename, class_t, folder):
    reader, reader_rand, reader_surr = FSE_init('data\\' + filename)
    method_dcca = class_t(-5, 5, 1, reader)
    method_dcca_rand = class_t(-5, 5, 1, reader_rand)
    method_dcca_surr = class_t(-5, 5, 1, reader_surr)
    method_dcca.generate()
    method_dcca_rand.generate()
    method_dcca_surr.generate()
    # flist = method_dcca.flist
    # hurst_list = method_dcca.hurst_list
    alfa = [method_dcca.alfa, method_dcca_rand.alfa, method_dcca_surr.alfa]
    f_alfa = [method_dcca.f_alfa,
              method_dcca_rand.f_alfa, method_dcca_surr.f_alfa]
    label_fse = ['origin', 'random', 'surrogate']
    label_hurst = ['A Data', 'B Data', 'C Data']
    print_graph(filename, folder, alfa, f_alfa, label_fse,
                'alfa', 'f_alfa', scale=[0, 1.6, 0, 1.05])
    # print_graph('Hurst' + filename, folder, flist, hurst_list, label_hurst,
    # 'q', 'H_q')
    print(filename)
    print('origin', max(method_dcca.alfa) - min(method_dcca.alfa))
    print('random', max(method_dcca_rand.alfa) - min(method_dcca_rand.alfa))
    print('surrogate', max(method_dcca_surr.alfa) - min(method_dcca_surr.alfa))
    return method_dcca.hurst_list


current_dir = 'data'
# list_t =
# [-5.0, -4.9, -4.8, -4.7, -4.6, -4.5, -4.4, -4.3, -4.2, -4.1, -4.0, -3.9, -3.8, -3.7, -3.6, -3.5, -3.4, -3.3, -3.2, -3.1, -3.0, -2.9, -2.8, -2.7, -2.6, -2.5, -2.4, -2.3, -2.2, -2.1, -2.0, -1.9, -1.8, -1.7, -1.6, -1.5, -1.4, -1.3, -1.2, -1.1, -1.0, -0.9, -0.8, -0.7, -0.6, -
# 0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7,
# 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1,
# 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5,
# 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9,
# 5.0]
list_t = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
flist = [list_t, list_t, list_t]
hurst_cca = []
hurst_dcca = []
label_hurst = ['A Data', 'B Data', 'C Data']
for root, dirs, files in os.walk(current_dir):
    for file in files:
        hurst_cca.append(estimate_fse(file, MF_CCA, 'fse_cca\\'))
        hurst_dcca.append(estimate_fse(file, MF_DCCA, 'fse_dcca\\'))
for item in hurst_cca:
    print item[7]
for item in hurst_dcca:
    print item[7]
dcca_p1 = hurst_cca[0:3]
dcca_p2 = hurst_cca[3:6]
dpxa_p1 = hurst_dcca[0:3]
dpxa_p2 = hurst_dcca[3:6]
axiss = [-5.5, 5.5, 0, 1.4])
print_graph('hurst_cca1', 'fse_cca\\', flist,
            dcca_p1, label_hurst, 'q', 'H_q', scale = axiss)
print_graph('hurst_cca2', 'fse_dcca\\', flist,
            dcca_p2, label_hurst, 'q', 'H_q', scale = axiss)
print_graph('hurst_dcca1', 'fse_cca\\', flist,
            dpxa_p1, label_hurst, 'q', 'H_q', scale = axiss)
print_graph('hurst_dcca2', 'fse_dcca\\', flist,
            dpxa_p2, label_hurst, 'q', 'H_q', scale = axiss)
