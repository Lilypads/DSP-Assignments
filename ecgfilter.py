import numpy as np
from firfilter import FIR_filter
from numpy import loadtxt
from matplotlib import pyplot


'''
h = np.array([1/2,1/2,0,0,0])
f = FIR_filter(h)
y= f.dofilter(0)
print(y)
y= f.dofilter(1)
print(y)
for i in range (20):
   y= f.dofilter(0)
   print(y)
'''

fs = 500
M = 200

k1 = int(45/fs * M)
k2 = int(55/fs * M) 

Window = np.ones(M)
Coeff = np.ones(M)

Window[k1:k2+1] = 0
Window[M-k2:M-k1+1] = 0

pyplot.figure(4)
pyplot.plot(Window)

W = np.fft.ifft(Window)
W = np.real(W)

pyplot.figure(5)
pyplot.plot(W)

Coeff[0:int(M/2)] =  W[int(M/2):M]
Coeff[int(M/2):M] =  W[0:int(M/2)]

pyplot.figure(6)
pyplot.plot(Coeff)

file1 = open('ECG.dat', 'r') 

ecg = loadtxt("ECG.dat")

pyplot.figure(1)
pyplot.plot(ecg)

count = 0

Filter = FIR_filter(Coeff)

filterecg = np.ones(5000+1)

for line in file1: 
    count += 1
    ecg1 = line.strip()
    print(ecg1)
    filterecg[count] = Filter.dofilter(ecg1)
    
print(count)
filterecg[0] = 0
pyplot.figure(7)
pyplot.plot(filterecg)
#pyplot.xlim(1000,2000)
    
    
    






    
    
