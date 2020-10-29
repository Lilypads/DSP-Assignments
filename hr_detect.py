import numpy as np
from matplotlib import pyplot
from numpy import loadtxt
from fir_filter import FIR_filter

cleanecg = loadtxt("shortecg.dat") 
fs=250


pyplot.figure(1)
time = np.linspace(0,len(cleanecg)/fs,len(cleanecg))
pyplot.plot(time,cleanecg)
pyplot.title('ecg (filtered)')
pyplot.xlabel('Time(s)')
pyplot.ylabel('Amplitude')

#720-900
template=cleanecg[720:900]    
    
pyplot.figure(2)
time2 = np.linspace(0,len(template)/fs,len(template))
pyplot.plot(time2,template)
pyplot.title('1 ecg')
pyplot.xlabel('Time(s)')
pyplot.ylabel('Amplitude')

fir_coeff = template[::-1]
pyplot.figure(3)
pyplot.plot(time2,fir_coeff)
pyplot.title('reversed 1 ecg')
pyplot.xlabel('Time(s)')
pyplot.ylabel('Amplitude')

matchfilt = FIR_filter(fir_coeff)

matchresult = np.zeros(len(cleanecg))
for i in range(len(cleanecg)):
    matchresult[i] = matchfilt.dofilter(cleanecg[i])
    
pyplot.figure(4)
pyplot.plot(time,matchresult)
pyplot.title('Matched Filtered ecg')
pyplot.xlabel('Time(s)')
pyplot.ylabel('Amplitude')

matchresult = matchresult*matchresult
pyplot.figure(5)
pyplot.plot(time,matchresult)
pyplot.title('Squared Matched Filtered ecg')
pyplot.xlabel('Time(s)')
pyplot.ylabel('Amplitude')

hr = np.zeros(len(matchresult))
threshold = 0.00000000002
for i in range(len(matchresult)):
    if matchresult[i]>threshold:
        hr[i]=1

pyplot.figure(6)
pyplot.plot(time,hr)
pyplot.title('Heard Beat Detection Sequence')
pyplot.xlabel('Time(s)')
pyplot.ylabel('Amplitude')