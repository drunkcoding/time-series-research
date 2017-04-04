import pandas as pd
import numpy as np
import os

dir_base = 'data\\Chinese_Stock\\'
data_dir = dir_base + 'data_code\\'
lead_dir = dir_base + 'lead\\'

reader = pd.read_excel(dir_base + 'corr.xlsx')
files = os.listdir(lead_dir)
num_files = len(files)
step_list = [5, 10, 20, 40, 60, 120, 245, 500, 750, 1250, 1750]
unit_list = [[1.0 for i in range(num_files)] for j in range(num_files)]

for i in range(len(step_list)):
    tmp_reader = reader
    for c in reader.columns.values:
        for r in reader.index.values:
            if c != r:
                tmp_reader.loc[r, c] = tmp_reader.loc[r, c][i]
    print(tmp_reader)
    dist = np.sqrt(np.multiply(2, np.subtract(unit_list, tmp_reader.values)))
    df_dist = pd.DataFrame(dist, columns=files, index=files)
    df_dist.to_excel(dir_base + 'dist\\' + 'dist_' + str(step_list[i]) +'.xlsx')
