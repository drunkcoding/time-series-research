import pandas as pd
import numpy as np
from numpy import polyfit, polyval, power, sqrt, absolute, log, mean, subtract, diff
#from scipy.special import gamma
import matplotlib.pyplot as plt
from InitMethod import partition

import warnings
warnings.simplefilter('ignore', np.RankWarning)

class MF_DFA(object):
    def __init__(self, min_q, max_q, bandwith, reader):
        self.flist = [x/bandwith for x in range(min_q*bandwith, max_q*bandwith+1, 1)]
        self.x_data = diff(log(reader.X.values)).tolist()
        #self.y_data = diff(log(reader.Y.values)).tolist()
        del reader['X']
        #del reader['Y']
        #self.z_data = [diff(log(reader[key].values)).tolist() for key in reader]        
        self.length = len(self.x_data)
        self.hurst_list = []
        self.tau = None
        self.alfa = None
        self.f_alfa = None
        #self.fig = 'graph\\' + filename + '_log.jpg'

    def fit_residual(degree, y_wins, r_x, step_t):
        num_wins = len(y_wins)
        nroot = lambda x, q: power(mean(power(x, q/2.0)), 1.0/q)
        corr = lambda x1, x2: mean(power(subtract(x1, x2), 2 ), axis = 1)
        y_trend_coef = [polyfit(r_x[i], y_wins[i], degree) for i in range(num_wins)]
        y_trend = [polyval(y_trend_coef[i], r_x[i]) for i in range(num_wins)]
        corr_wins = corr(y_wins, y_trend)
        return [nroot(corr_wins, q) for q in flist]
        #return nroot(corr_wins, 2)

    def generate(self):
        base = 2
        #step_list = [int(self.length/base**x) for x in range(2, int(log(self.length)/log(base))+1) if base**x <= self.length/20]
        step_list = [k for k in range(15, int(self.length/2), 10)]
        corr_list = []
        for step_t in step_list:
            num_wins = int(np.floor(length/step_t))
            mean_t = np.mean(x_data)
            x_data = np.subtract(x_data, mean_t)
            y_data = np.cumsum(x_data)
            y_wins = partition(y_data.tolist(), step_t, num_wins)
            tmp = [i for i in range(1, num_wins*2*step_t+1)]
            r_wins = partition(tmp, step_t, num_wins)
            corr_list.append(fit_residual(1, y_wins, r_wins, step_t))
        expected = lambda n: 1/sqrt(n*np.pi/2)*sum([sqrt((n-i)/i) for i in range(1,n)]) if n >=340 else 1/sqrt(np.pi)/gamma(n/2)*gamma((n-1)/2)*sum([sqrt((n-i)/i) for i in range(1,n)])
        for i in range(len(self.flist)):
            F_q = [element[i] for element in corr_list]
            x_log = log(step_list)
            F_log = log(F_q)
            y_log = [F_log[i]-log(expected(step_list[i]))+x_log[i]/2 for i in range(len(step_list))]
            coef = polyfit(x_log, F_log, 1)
            #plot2 = plt.plot(x_log, y_log, label='trend')
            self.hurst_list.append(coef[0])
        #plt.savefig(self.fig)
        #print(self.hurst_list)
        #self.plot(self.hurst_list)
        f_length = len(self.flist)
        self.tau = [self.flist[i]*self.hurst_list[i]-1 for i in range(f_length)]
        tmp = diff(self.tau)
        tmp2 = diff(self.flist)
        self.alfa = np.divide(tmp, tmp2)
        self.f_alfa = [self.flist[i]*self.alfa[i]-self.tau[i] for i in range(f_length-1)]
