import pandas as pd
import matplotlib.pyplot as plt
import os

from method.DCCA import MF_DCCA
from method.CCA import MF_CCA

current_dir = 'data'
for root, dirs, files in os.walk(current_dir):
    for file in files:
        reader = pd.read_csv('data\\' + file)
        method = MF_CCA(-5, 5, 1, reader, file)
        method.generate()
        method = MF_DCCA(-5, 5, 1, reader, file)
        method.generate()
