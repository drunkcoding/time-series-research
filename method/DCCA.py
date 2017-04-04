# coding: utf-8
import pandas as pd
import numpy as np
from numpy import transpose, dot, polyfit, polyval, power, exp, log, sqrt, floor, cumsum, diff, mean, subtract, multiply, square, absolute
from numpy.linalg import lstsq, inv
import matplotlib.pyplot as plt
from scipy.special import gamma
#from InitMethod import partition

import warnings
warnings.simplefilter('ignore', np.RankWarning)

class MF_DCCA(object):
    def __init__(self, min_q, max_q, bandwith, reader):
        self.flist = [x/bandwith for x in range(min_q*bandwith, max_q*bandwith+1, 1)]
        #print(np.log(reader.X.values.tolist()))
        self.x_data = diff(np.log(reader.X.values.tolist())).tolist()
        self.y_data = diff(np.log(reader.Y.values.tolist())).tolist()   
        self.length = len(self.x_data)
        self.hurst_list = []
        self.cov_list = []
        self.tau = None
        self.alfa = None
        self.f_alfa = None
        #self.fig = 'graph\\' + filename + '_log.jpg'

    def _fit_residual(self, degree, x_wins, y_wins, r_x, step_t):
        num_wins = len(x_wins)
        nroot = lambda x, q: exp(mean(log(sqrt(x) )) ) if -1e-3<q<1e-3 else power(mean(power(x, q/2.0)), 1.0/q)
        corr = lambda x1, x2, y1, y2: mean(absolute(multiply(subtract(x1, x2), subtract(y1, y2) )), axis = 1)
        x_profile = cumsum(x_wins, axis = 1)
        y_profile = cumsum(y_wins, axis = 1)
        #r_x = [k for k in range(step_t)]
        x_trend_coef = [polyfit(r_x[i], x_profile[i], degree) for i in range(num_wins)]
        y_trend_coef = [polyfit(r_x[i], y_profile[i], degree) for i in range(num_wins)]
        x_trend = [polyval(x_trend_coef[i], r_x[i]) for i in range(num_wins)]
        y_trend = [polyval(y_trend_coef[i], r_x[i]) for i in range(num_wins)]
        corr_wins = corr(x_profile, x_trend, y_profile, y_trend)
        #print(step_t, corr_wins)
        self.cov_list.append(mean(corr_wins))
        q_order_corr = [nroot(corr_wins, q) for q in self.flist]
        return q_order_corr

    def partition(self, list_t, step_t, num_wins):
        len_t = len(list_t)
        a = [list_t[i:i+step_t] for i in range(0,len_t,step_t)]
        list_t.reverse()
        b = [list_t[i:i+step_t] for i in range(0,len_t,step_t)]
        if num_wins*step_t != len_t:
            a.pop()
            b.pop()
        return a+b

    def _cal_profile(self, data):
        """
        distributance profile
        """
        mean_t = mean(data)
        tmp = subtract(data, mean_t)
        return cumsum(tmp)

    def _cal_diff(self, profile, step_t):
        """
        difference between profile and local trend
        """
        length = len(profile)
        difference = []
        for i in range(length-step_t):
            window = profile[i:i+step_t]
            r_x = [x for x in range(i, i+step_t)]
            trend_coef = polyfit(r_x, window,1)
            trend = polyval(trend_coef, r_x)
            difference.append(subtract(window, trend))
        return difference

    def _cal_var(self, X, Y):
        multi = multiply(X, Y)
        return mean(multi)

    def corr_coef(self):
        step_list = [5, 10, 20, 40, 60, 120, 245, 500, 750, 1250, 1750]   #按照交易日均线
        #[k for k in range(15, 2000, 10)]
        profile_x = self._cal_profile(self.x_data)
        profile_y = self._cal_profile(self.y_data)
        for step_t in step_list:
            diff_x = self._cal_diff(profile_x, step_t)
            diff_y = self._cal_diff(profile_y, step_t)
            self.cov_list.append(self._cal_var(diff_x, diff_y)/np.sqrt(self._cal_var(diff_y, diff_y)*self._cal_var(diff_x, diff_x)))


    def generate(self):
        base = 2
        #step_list = [int(self.length/base**x) for x in range(2, int(log(self.length)/log(base))+1) if base**x <= self.length/20]
        step_list = [k for k in range(15, int(self.length/2), 10)]
        #step_list = [k for k in range(15, 2000, 10)]
        #partition = lambda list_t, start_range, end_range, step_t: [list_t[i:i+step_t] for i in range(0,end_range+1,step_t)] + [list_t[i-step_t:i] for i in range(self.length,start_range-1,-step_t)]
        corr_list = []
        for step_t in step_list:
            num_wins = int(floor(self.length/step_t))
            #end_range = (num_wins-1)*step_t
            #start_range = self.length-end_range
            x_wins = self.partition(self.x_data, step_t, num_wins)
            y_wins = self.partition(self.y_data, step_t, num_wins)
            #z_wins = partition(self.z_data, start_range, end_range, step_t)
            tmp = [i for i in range(1, num_wins*step_t+1)]
            r_x = self.partition(tmp, step_t, num_wins)
            corr_list.append(self._fit_residual(7, x_wins, y_wins, r_x, step_t))
        #plt.figure()
        expected = lambda n: 1/sqrt(n*np.pi/2)*sum([sqrt((n-i)/i) for i in range(1,n)]) if n >=340 else 1/sqrt(np.pi)/gamma(n/2)*gamma((n-1)/2)*sum([sqrt((n-i)/i) for i in range(1,n)])
        for i in range(len(self.flist)):
            F_q = [element[i] for element in corr_list]
            #print(F_q)
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
        
