import numpy as np 

from scipy import stats
from statsmodels.compat.python import lzip

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
