import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

#from statsmodels.tsa.stattools import acf, pacf
from statsmodels.graphics import tsaplots
from matplotlib import mlab
from scipy import stats
from statsmodels.compat.python import (iteritems, range, lrange, string_types,
                                       lzip, zip, long)

def acovf(x):
    x = np.squeeze(np.asarray(x))
    #xo = x - x.mean()
    xo = x
    n = len(x)
    d = n * np.ones(2 * n - 1)
    acov = (np.correlate(xo, xo, 'full') / d)[n - 1:]
    print(acov)
    return acov

def acf(x, nlags=40, alpha=0.05):
    nobs = len(x)  # should this shrink for missing='drop' and NaNs in x?
    avf = acovf(x)
    acf = avf[:nlags + 1] / avf[0]
    varacf = np.ones(nlags + 1) / nobs
    varacf[0] = 0
    varacf[1] = 1. / nobs
    varacf[2:] *= 1 + 2 * np.cumsum(acf[1:-1]**2)
    interval = stats.norm.ppf(1 - alpha / 2.) * np.sqrt(varacf)
    confint = np.array(lzip(acf - interval, acf + interval))
    print(acf)
    return acf


reader = pd.read_excel('close.xlsx')
reader = reader.dropna()
close = reader['close'].values
mean_c = reader['meanc'].values

fig, axes = plt.subplots(nrows=2, figsize=(8, 12))
fig.tight_layout()
axes[0].plot(close)
#label(axes[0], 'Raw Data')
tsaplots.plot_acf(close, axes[1])
#label(axes[1], 'Statsmodels Autocorrelation')
plt.show()


mean_t = np.mean(close)
print(mean_t)
close_t = np.subtract(close, mean_t-1000)
'''
plt.figure()
plt.xcorr(close, close_t, usevlines=True, maxlags=100, normed=True, lw=2)
plt.axis([0,100,-0.5,0.5])
plt.show()
'''
end = len(mean_c)-1
pacf_t = acf(close, nlags=end)
#x_t = [k for k in range(pacf_t)]
plt.figure()
#plt.acorr(np.absolute(close_t), maxlags=200)

plt.acorr(mean_c, maxlags=end)
plt.axis([0,end,0,1])
plt.show()
#for k in pacf_t: print(k)
