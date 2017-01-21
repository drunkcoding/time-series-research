A = DPXA(-5, 5, 10, 'period2_1.csv')
A.generate()
B = DPXA(-5, 5, 10, 'period2_2.csv')
B.generate()
C = DPXA(-5, 5, 10, 'period2_3.csv')
C.generate()
flist = A.flist
f_length = len(flist)
hurst_list = [A.hurst_list, B.hurst_list, C.hurst_list]
colors = np.random.rand(3)
size_t = 10
#print(A.hurst_lista)
#print(B.hurst_list)
#print(C.hurst_list)
#----------------------q vs. H_q
plt.figure()
plt.scatter(flist, hurst_list[0], s = size_t, c = 'b', edgecolors = 'none', label='A data')
plt.scatter(flist, hurst_list[1], s = size_t, c = 'r', edgecolors = 'none', label='B data')
plt.scatter(flist, hurst_list[2], s = size_t, c = 'y', edgecolors = 'none', label='C data')
plt.xlabel('q')
plt.ylabel('H_q')
plt.legend(loc = 'best')
plt.savefig('Hq_q2.jpg')

#----------------------q vs. tau
plt.figure()
tau = [[flist[i]*hurst_list[k][i]-1 for i in range(f_length)] for k in [0,1,2]]
#tau = [self.flist[i]*hurst_list[i]-(self.flist[i]*hurst_list[i]-1)/(self.flist[i]-1) for i in range(f_length)]
plt.scatter(flist, tau[0], s = size_t, c = 'b', edgecolors = 'none', label='A data')
plt.scatter(flist, tau[1], s = size_t, c = 'r', edgecolors = 'none', label='B data')
plt.scatter(flist, tau[2], s = size_t, c = 'y', edgecolors = 'none', label='C data')
plt.xlabel('q')
plt.ylabel('tau')
plt.legend(loc = 'lower right')
plt.savefig('tau_q2.jpg')
#----------------------alfa vs. f_alfa
tmp = diff(tau)
tmp2 = diff(flist)
#print(np.divide(tmp, tmp2))
alfa = np.divide(tmp, tmp2)
for k in alfa: print(max(k)-min(k))
#alfa = [tmp1[i]/tmp2[i] for i in range(f_length-1)]
#diff_list = [tmp1[i]/tmp2[i] for i in range(f_length-1)]
#alfa = [diff_list[i]*self.flist[i]+hurst_list[i] for i in range(f_length-1)]
#f_alfa = [diff_list[i]*self.flist[i]**2+1 for i in range(f_length-1)]
f_alfa = [[flist[i]*alfa[k][i]-tau[k][i] for i in range(f_length-1)] for k in [0,1,2]]
#f_alfa = [self.flist[i]*alfa[i]-tau[i] for i in range(f_length-1)]
plt.figure()
plt.scatter(alfa[0], f_alfa[0], s = size_t, c = 'b', edgecolors = 'none', label='A data')
plt.scatter(alfa[1], f_alfa[1], s = size_t, c = 'r', edgecolors = 'none', label='B data')
plt.scatter(alfa[2], f_alfa[2], s = size_t, c = 'y', edgecolors = 'none', label='C data')
plt.xlabel('alfa')
plt.ylabel('f_alfa')
plt.legend(loc = 'best')
plt.savefig('f_alfa2.jpg')

A = DCCA(-5, 5, 10, 'period2_1.csv')
A.generate()
B = DCCA(-5, 5, 10, 'period2_2.csv')
B.generate()
C = DCCA(-5, 5, 10, 'period2_3.csv')
C.generate()
flist = A.flist
f_length = len(flist)
hurst_list = [A.hurst_list, B.hurst_list, C.hurst_list]
colors = np.random.rand(3)
size_t = 10
#print(A.hurst_lista)
#print(B.hurst_list)
#print(C.hurst_list)
#----------------------q vs. H_q
plt.figure()
plt.scatter(flist, hurst_list[0], s = size_t, c = 'b', edgecolors = 'none', label='A data')
plt.scatter(flist, hurst_list[1], s = size_t, c = 'r', edgecolors = 'none', label='B data')
plt.scatter(flist, hurst_list[2], s = size_t, c = 'y', edgecolors = 'none', label='C data')
plt.xlabel('q')
plt.ylabel('H_q')
plt.legend(loc = 'best')
plt.savefig('Hq_q_NP2.jpg')

#----------------------q vs. tau
plt.figure()
tau = [[flist[i]*hurst_list[k][i]-1 for i in range(f_length)] for k in [0,1,2]]
#tau = [self.flist[i]*hurst_list[i]-(self.flist[i]*hurst_list[i]-1)/(self.flist[i]-1) for i in range(f_length)]
plt.scatter(flist, tau[0], s = size_t, c = 'b', edgecolors = 'none', label='A data')
plt.scatter(flist, tau[1], s = size_t, c = 'r', edgecolors = 'none', label='B data')
plt.scatter(flist, tau[2], s = size_t, c = 'y', edgecolors = 'none', label='C data')
plt.xlabel('q')
plt.ylabel('tau')
plt.legend(loc = 'lower right')
plt.savefig('tau_q_NP2.jpg')
#----------------------alfa vs. f_alfa
tmp = diff(tau)
tmp2 = diff(flist)
#print(np.divide(tmp, tmp2))
alfa = np.divide(tmp, tmp2)
for k in alfa: print(max(k)-min(k))
#alfa = [tmp1[i]/tmp2[i] for i in range(f_length-1)]
#diff_list = [tmp1[i]/tmp2[i] for i in range(f_length-1)]
#alfa = [diff_list[i]*self.flist[i]+hurst_list[i] for i in range(f_length-1)]
#f_alfa = [diff_list[i]*self.flist[i]**2+1 for i in range(f_length-1)]
f_alfa = [[flist[i]*alfa[k][i]-tau[k][i] for i in range(f_length-1)] for k in [0,1,2]]
#f_alfa = [self.flist[i]*alfa[i]-tau[i] for i in range(f_length-1)]
plt.figure()
plt.scatter(alfa[0], f_alfa[0], s = size_t, c = 'b', edgecolors = 'none', label='A data')
plt.scatter(alfa[1], f_alfa[1], s = size_t, c = 'r', edgecolors = 'none', label='B data')
plt.scatter(alfa[2], f_alfa[2], s = size_t, c = 'y', edgecolors = 'none', label='C data')
plt.xlabel('alfa')
plt.ylabel('f_alfa')
plt.legend(loc = 'best')
plt.savefig('f_alfa_NP2.jpg')
