from ecg_gudb_database import GUDb
import numpy as np
from fir_filter import FIR_filter
from numpy import loadtxt
from matplotlib import pyplot

fs = 250    #Hz
M = 500     #loses 2 heart beat to warm up the filter (2seconds)/affect frequency resolution

# 50 Hz Notch Filter
k1 = int(49.5/fs * M)
k2 = int(50.5/fs * M) 

Window = np.ones(M)
Coeff = np.ones(M)

Window[k1:k2+1] = 0
Window[M-k2:M-k1+1] = 0

pyplot.figure(1)
pyplot.plot(Window)
pyplot.title('50 Hz Notch Filter - Ideal')
pyplot.xlabel('M (sample number)')
pyplot.ylabel('Amplitude')

W = np.fft.ifft(Window)
W = np.real(W)

pyplot.figure(2)
pyplot.plot(W)
pyplot.title('50 Hz Notch Filter - IFFT')
pyplot.xlabel('Coefficient Index')
pyplot.ylabel('Amplitude')

Coeff[0:int(M/2)] =  W[int(M/2):M]
Coeff[int(M/2):M] =  W[0:int(M/2)]

pyplot.figure(3)
pyplot.plot(Coeff)
pyplot.title('50 Hz Notch Filter - IFFT(fixed)')
pyplot.xlabel('Coefficient Index')
pyplot.ylabel('Amplitude')

Filter = FIR_filter(Coeff)


#DC filter
k3 = int(0.5/fs * M)
WindowDC = np.ones(M)
CoeffDC = np.ones(M)

WindowDC[0:k3+1] = 0
pyplot.figure(4)
pyplot.plot(WindowDC)
pyplot.title('DC Filter - Ideal')
pyplot.xlabel('M (sample number)')
pyplot.ylabel('Amplitude')

WDC = np.fft.ifft(WindowDC)
WDC = np.real(WDC)

pyplot.figure(5)
pyplot.plot(WDC)
pyplot.title('DC Filter - IFFT')
pyplot.xlabel('Coefficient Index')
pyplot.ylabel('Amplitude')

CoeffDC[0:int(M/2)] =  WDC[int(M/2):M]
CoeffDC[int(M/2):M] =  WDC[0:int(M/2)]

pyplot.figure(6)
pyplot.plot(CoeffDC)
pyplot.title('DC Filter - IFFT(fixed)')
pyplot.xlabel('Coefficient Index')
pyplot.ylabel('Amplitude')

FilterDC = FIR_filter(CoeffDC)


# load first ECG file
file1 = open('ECG.dat', 'r')    #line by line to use as real-time filter

ecg = loadtxt("ECG.dat")        #for diagnosis plot

pyplot.figure(7)
print(len(ecg))
time = np.linspace(0,len(ecg)/fs,len(ecg))
pyplot.plot(time,ecg)
pyplot.title('ecg (raw)')
pyplot.xlabel('Time(s)')
pyplot.ylabel('Amplitude')


# Investigate frequency domain
fx=np.fft.fft(ecg)
fxx = fx/len(ecg)             # Fourier Transform Normalised
dbs = 20*np.log10(abs(fxx))    # DB Conversion 
pyplot.figure(8)
freq = np.linspace(0,fs,len(ecg))
pyplot.plot(freq,dbs)
pyplot.title('ecg (raw) - Frequency Domain')
pyplot.xlabel('Frequency (Hz)')
pyplot.ylabel('Amplitude')

#load second ECG data
'''Initialise experiments from the files of einthoven'''
subject_number = 3
experiment = 'maths' 
ecg_class = GUDb(subject_number, experiment)

'''Initialise experiments from the files of einthoven'''
chest_strap_V2_V1 = ecg_class.cs_V2_V1
einthoven_ii = ecg_class.einthoven_II

'''Filtered Data With Einthoven'''
ecg_class.filter_data()
einthoven_ii_filt = ecg_class.einthoven_II_filt

#define output array and intermediate variable
filterecg = np.zeros(len(ecg)+1)
filtereinthoven = np.zeros(len(einthoven_ii)+1)
intermediate = 0

#filter ecg for both data sets
count = 0
for line in file1: 
    count += 1
    ecg1 = line.strip()
    #print(ecg1)
    intermediate = Filter.dofilter(ecg1)
    filterecg[count] = FilterDC.dofilter(intermediate)
    
for i in range(len(einthoven_ii)): 
    intermediate = Filter.dofilter(einthoven_ii[i])
    filtereinthoven[i] = FilterDC.dofilter(intermediate)

#print(count)

#plot the filtered data    
pyplot.figure(9)
time2 = np.linspace(0,len(filterecg)/fs,len(filterecg))
pyplot.plot(time2,filterecg)
pyplot.ylim(-0.002,0.002)
pyplot.title('ecg (filtered)')
pyplot.xlabel('Time(s)')
pyplot.ylabel('Amplitude')

pyplot.figure(10)
time3 = np.linspace(0,len(filtereinthoven)/fs,len(filtereinthoven))
pyplot.plot(time3,filtereinthoven)
pyplot.ylim(-0.002,0.002)
pyplot.title('einthoven (filtered)')
pyplot.xlabel('Time(s)')
pyplot.ylabel('Amplitude')

''' 
#try to plot both raw and filtered on same plot figure 10 for diagnosis purpose
print(len(einthoven_ii))
time = np.linspace(0,len(einthoven_ii)/fs,len(einthoven_ii))
pyplot.plot(time,einthoven_ii)
pyplot.title('einthoven_ii walking (raw and filtered)')
pyplot.xlabel('Time(s)')
pyplot.ylabel('Amplitude')
'''

#save filtered data    
np.savetxt('shortecg.dat',filterecg)
np.savetxt('shorteint.dat',filtereinthoven)
    






    
    
