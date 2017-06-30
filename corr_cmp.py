import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

dir_base = 'data\\Chinese_Stock\\'
corr_dir_down = dir_base + 'corr_dcca_down\\'
corr_dir_up = dir_base + 'corr_dcca_up\\'
oil_list = dir_base + 'oil\\'

corrs_up = os.listdir(corr_dir_up)
corrs_up.sort()
print corrs_up
corrs_down = os.listdir(corr_dir_down)
corrs_down.sort()
print corrs_down
files = os.listdir(oil_list)
num_name = len(files)
num_file = len(corrs_down)
step_list = [10,120,1250,1750,20,245,40,5,500,60,750]
for i in range(num_file):
    tmp_up = pd.read_excel(corr_dir_up + corrs_up[i])
    tmp_down = pd.read_excel(corr_dir_down + corrs_down[i])
    for name in files:
        x = tmp_up[name].values.tolist()
        y = tmp_down[name].values.tolist()
        plt.figure()
        plt.scatter(x, y, s=12, c='b', edgecolors='none')
        plt.plot([-0.5,1], [-0.5,1], 'r--',linewidth=1.5)
        plt.axis([-0.5,1,-0.5,1])
        plt.savefig('graph\\\corr_cmp\\' + name.split('.')[0]+ '-' + str(step_list[i]) + '.jpg')
        plt.close()