import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

from statsmodels.tsa.stattools import acf, pacf
from statsmodels.graphics import tsaplots
from matplotlib import mlab

reader = pd.read_excel('close.xlsx')
reader = reader.dropna()
close = reader['close'].values

fig, axes = plt.subplots(nrows=2, figsize=(8, 12))
fig.tight_layout()
axes[0].plot(close)
#label(axes[0], 'Raw Data')
tsaplots.plot_acf(close, axes[1])
#label(axes[1], 'Statsmodels Autocorrelation')
plt.show()

mean_t = np.mean(close)
close_t = np.subtract(close, mean_t)
plt.figure()
plt.xcorr(close, close_t, usevlines=True, maxlags=2000, normed=True, lw=2)
plt.axis([0,2000,-0.5,0.5])
plt.show()

pacf_t = acf(close_t, nlags=100)
#for k in pacf_t: print(k)
