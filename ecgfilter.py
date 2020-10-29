import numpy as np
from fir_filter import FIR_filter
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

fs = 250
M = 200

# 50 Hz Notch Filter
k1 = int(49/fs * M)
k2 = int(51/fs * M) 

Window = np.ones(M)
Coeff = np.ones(M)

Window[k1:k2+1] = 0
Window[M-k2:M-k1+1] = 0

pyplot.figure(1)
pyplot.plot(Window)

W = np.fft.ifft(Window)
W = np.real(W)

pyplot.figure(2)
pyplot.plot(W)

Coeff[0:int(M/2)] =  W[int(M/2):M]
Coeff[int(M/2):M] =  W[0:int(M/2)]

pyplot.figure(3)
pyplot.plot(Coeff)

Filter = FIR_filter(Coeff)


#DC filter
k3 = int(2/fs * M)
WindowDC = np.ones(M)
CoeffDC = np.ones(M)

WindowDC[0:k3+1] = 0
pyplot.figure(6)
pyplot.plot(WindowDC)

WDC = np.fft.ifft(WindowDC)
WDC = np.real(WDC)

pyplot.figure(7)
pyplot.plot(WDC)

CoeffDC[0:int(M/2)] =  WDC[int(M/2):M]
CoeffDC[int(M/2):M] =  WDC[0:int(M/2)]

pyplot.figure(8)
pyplot.plot(CoeffDC)

FilterDC = FIR_filter(CoeffDC)


# load ECG file
file1 = open('ECG.dat', 'r')    #line by line to use as real-time filter

ecg = loadtxt("ECG.dat")        #for diagnosis plot

pyplot.figure(4)
pyplot.plot(ecg)

# Investigate frequency domain
fx=np.fft.fft(ecg)
fxx = fx/len(ecg)             # Fourier Transform Normalised
dbs = 20*np.log10(abs(fxx))    # DB Conversion 
pyplot.figure(9)
freq = np.linspace(0,fs,len(ecg))
pyplot.plot(freq,dbs)


filterecg = np.ones(5000+1)
intermediate = 0

count = 0
for line in file1: 
    count += 1
    ecg1 = line.strip()
    print(ecg1)
    intermediate = Filter.dofilter(ecg1)
    filterecg[count] = FilterDC.dofilter(intermediate)
    
print(count)
pyplot.figure(5)
pyplot.plot(filterecg)
pyplot.ylim(-0.002,0.002)
    
np.savetxt('shortecg.dat',filterecg)
    






    
    
