# coding: utf-8
import pandas as pd
import numpy as np
from numpy import transpose, dot, polyfit, polyval, power, exp, log, sqrt, floor, cumsum, diff, mean, subtract, multiply, square, absolute
from numpy.linalg import lstsq, inv
import matplotlib.pyplot as plt
from scipy.special import gamma

import warnings
warnings.simplefilter('ignore', np.RankWarning)

class DPXA(object):
    def __init__(self, min_q, max_q, bandwith, filename):
        self.flist = [x/bandwith for x in range(min_q*bandwith, max_q*bandwith+1, 1)]
        reader = pd.read_csv(filename)
        #print(reader)
        self.x_data = diff(log(reader.X.values)).tolist()
        self.y_data = diff(log(reader.Y.values)).tolist()
        del reader['X']
        del reader['Y']
        self.z_data = [diff(log(reader[key].values)).tolist() for key in reader]        
        self.length = len(self.x_data)
        self.hurst_list = []
        self.fig = filename + '_loglog.jpg'

    def partition(self, list_t, step_t, num_wins):
        len_t = len(list_t)
        a = [list_t[i:i+step_t] for i in range(0,len_t,step_t)]
        list_t.reverse()
        b = [list_t[i:i+step_t] for i in range(0,len_t,step_t)]
        if num_wins*step_t != len_t:
            a.pop()
            b.pop()
        return a+b

    def plot(self, hurst_list):
        f_length = len(self.flist)
        plt.figure()
        plot1 = plt.scatter(self.flist, hurst_list)
        plt.savefig('Hq_q.jpg')
        plt.figure()
        tau = [self.flist[i]*hurst_list[i]-1 for i in range(f_length)]
        #tau = [self.flist[i]*hurst_list[i]-(self.flist[i]*hurst_list[i]-1)/(self.flist[i]-1) for i in range(f_length)]
        plot1 = plt.scatter(self.flist, tau)
        plt.savefig('tau_q.jpg')
        #----------------------q vs. D_q
        '''
        plt.figure()
        D = [tau[i]/(self.flist[i]-1) for i in range(f_length)]
        #tau = [self.flist[i]*hurst_list[i]-(self.flist[i]*hurst_list[i]-1)/(self.flist[i]-1) for i in range(f_length)]
        plot1 = plt.scatter(self.flist, D)
        plt.savefig('D_q.jpg')
        '''
        #----------------------alfa vs. f_alfa
        tmp1 = diff(tau)
        tmp2 = diff(self.flist)
        alfa = [tmp1[i]/tmp2[i] for i in range(f_length-1)]
        #diff_list = [tmp1[i]/tmp2[i] for i in range(f_length-1)]
        #alfa = [diff_list[i]*self.flist[i]+hurst_list[i] for i in range(f_length-1)]
        #f_alfa = [diff_list[i]*self.flist[i]**2+1 for i in range(f_length-1)]
        f_alfa = [self.flist[i]*alfa[i]-tau[i] for i in range(f_length-1)]
        plt.figure()
        plot1 = plt.scatter(alfa, f_alfa)
        plt.savefig('f_alfa_alfa.jpg')
        '''
        plt.figure() 
        x = [k+1 for k in range(len(x_data))]
        plot1 = plt.plot(x, x_data, label='x data')
        plot2 = plt.plot(x, y_data, label='y data')
        plt.xlabel('index')
        plt.ylabel('price')
        plt.legend(loc = 'best')
        plt.show()
        '''

    def _fit_residual(self, degree, x_wins, y_wins, z_wins, r_x, step_t):
        num_wins = len(x_wins)
        nroot = lambda x, q: exp(mean(log(sqrt(x) )) ) if -1e-3<q<1e-3 else power(mean(power(x, q/2.0)), 1.0/q)
        residual = lambda x, z: subtract(x, dot(z, lstsq(z, x)[0]) )
        corr = lambda x1, x2, y1, y2: mean(absolute(multiply(subtract(x1, x2), subtract(y1, y2) )), axis = 1)
        #profile = lambda res, mean: subtract(cumsum(res, axis = 1), cumsum(mean, axis = 1))
        x_result = [lstsq(transpose(z_wins[i]), x_wins[i])[0] for i in range(num_wins)]
        y_result = [lstsq(transpose(z_wins[i]), y_wins[i])[0] for i in range(num_wins)]
        x_point_residual = [subtract(x_wins[i], dot(transpose(z_wins[i]), x_result[i])) for i in range(num_wins)]
        y_point_residual = [subtract(y_wins[i], dot(transpose(z_wins[i]), y_result[i])) for i in range(num_wins)]
        x_profile = cumsum(x_point_residual, axis = 1)
        y_profile = cumsum(y_point_residual, axis = 1)
        #r_x = [k for k in range(step_t)]
        x_trend_coef = [polyfit(r_x[i], x_profile[i], degree) for i in range(num_wins)]
        y_trend_coef = [polyfit(r_x[i], y_profile[i], degree) for i in range(num_wins)]
        x_trend = [polyval(x_trend_coef[i], r_x[i]) for i in range(num_wins)]
        y_trend = [polyval(y_trend_coef[i], r_x[i]) for i in range(num_wins)]
        corr_wins = corr(x_profile, x_trend, y_profile, y_trend)
        #print(step_t, corr_wins)
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

    def generate(self):
        base = 1.025
        #step_list = [int(self.length/base**x) for x in range(int(log(4)/log(base)), int(log(self.length)/log(base))+1) if base**x <= self.length/15]
        #print(step_list)
        step_list = [k for k in range(10, int(self.length/4), 10)]
        #step_list = [k for k in range(15, 500)]
        #partition = lambda list_t, start_range, end_range, step_t: [list_t[i:i+step_t] for i in range(0,end_range+1,step_t)] + [list_t[i-step_t:i] for i in range(self.length,start_range-1,-step_t)]
        corr_list = []
        for step_t in step_list:
            num_wins = int(floor(self.length/step_t))
            #end_range = (num_wins-1)*step_t
            #start_range = self.length-end_range
            x_wins = self.partition(self.x_data, step_t, num_wins)
            y_wins = self.partition(self.y_data, step_t, num_wins)
            z_wins_list = [self.partition(line, step_t, num_wins) for line in self.z_data]
            length = len(z_wins_list[0])
            z_wins = [[element[i] for element in z_wins_list] for i in range(length)]
            #z_wins = partition(self.z_data, start_range, end_range, step_t)
            tmp = [i for i in range(1, num_wins*step_t+1)]
            r_x = self.partition(tmp, step_t, num_wins)
            corr_list.append(self._fit_residual(7, x_wins, y_wins, z_wins, r_x, step_t))
        #plt.figure()
        expected = lambda n: 1/sqrt(n*np.pi/2)*sum([sqrt((n-i)/i) for i in range(1,n)]) if n >=340 else 1/sqrt(np.pi)/gamma(n/2)*gamma((n-1)/2)*sum([sqrt((n-i)/i) for i in range(1,n)])
        F_q = [element[len(self.flist)-4] for element in corr_list]
        x_log = log(step_list)
        F_log = log(F_q)
        y_log = [F_log[i]-log(expected(step_list[i]))+x_log[i]/2 for i in range(len(step_list))]
        coef = polyfit(x_log, y_log, 1)
        print(coef[0])
        self.hurst_list.append(coef[0])
        plt.figure()
        for i in range(len(self.flist)):
            F_q = [element[i] for element in corr_list]
            x_log = log(step_list)
            F_log = log(F_q)
            y_log = [F_log[i]-log(expected(step_list[i]))+x_log[i]/2 for i in range(len(step_list))]
            tmp = plt.plot(x_log, y_log)
        plt.savefig(self.fig)
        
A = DPXA(-5, 5, 1, 'period2_1.csv')
A.generate()
B = DPXA(-5, 5, 1, 'period2_2.csv')
B.generate()
C = DPXA(-5, 5, 1, 'period2_3.csv')
C.generate()