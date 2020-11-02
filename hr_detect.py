from ecg_gudb_database import GUDb
import numpy as np
from matplotlib import pyplot
from numpy import loadtxt
from fir_filter import FIR_filter

    
    
#cleanecg = loadtxt("shortecg.dat") cleanecg = loadtxt("shortecg.dat") 
cleanecg = loadtxt("shorteint.dat") 
fs=250

pyplot.figure(1)
time = np.linspace(0,len(cleanecg)/fs,len(cleanecg))
pyplot.plot(time,cleanecg)
pyplot.title('ecg (filtered)')
pyplot.xlabel('Time(s)')
pyplot.ylabel('Amplitude')

#775-975
#template=cleanecg[775:975]  
template=cleanecg[7050:7225]    
      
    
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
print(len(matchresult))

matchresult = matchresult*matchresult
pyplot.figure(5)
pyplot.plot(time,matchresult)           #
pyplot.title('Squared Matched Filtered ecg')
pyplot.xlabel('Time(s)')
pyplot.ylabel('Amplitude')

hr = np.zeros(len(matchresult))
threshold = 0.00000000002 
for i in range(len(matchresult)):
    if matchresult[i]>threshold:
        hr[i]=1
        

pyplot.figure(6)
pyplot.plot(hr)
pyplot.title('Heart Beat Detection Sequence')
pyplot.xlabel('Time(s)')
pyplot.ylabel('Amplitude')
#pyplot.xlim(3,120)

j = 0
k = 0
m = 0
index = np.zeros(len(hr))
beatone = np.zeros(len(hr))
beatwo = np.zeros(len(hr))
deltat = np.zeros(len(hr)+1)
rate = np.zeros(len(hr))

thresh = int(1/(3.66/fs))    #3.66 is the maximum that would ever occur (upper limit)

for i in range(len(hr)):
    if hr[i] == 1:
        for n in range(int(thresh)):
            if i+n+1 <= 30000: 
                hr[i+n+1] = 0
            
      #  index[j] = i
      #  j += 1
      #  if j != 0:    
      #      if index[j] - index[j-1] < thresh: 
      #         hr[i] = 0

pyplot.figure(7)
pyplot.plot(hr)
pyplot.title('Heart Beat Detection Sequence Error')
pyplot.xlabel('Time(s)')
pyplot.ylabel('Amplitude')
#pyplot.xlim(3,120)


for i in range(len(hr)):
    if hr[i] != 0:
        beatone[k] = i
        beatwo[k-1] = i
        #print('ONE',beatone[k])
        #print('TWO',beatone[k-1])
        k += 1
        if k >= 0:          # To neglect the first detection
            deltat[m] = (beatone[m] - beatone[m-1])/fs
            print('ONE',beatone[m])
            print('TWO',beatone[m-1])
            print('TIME',deltat[m])
            rate[m] = (1/deltat[m])*60
            print(rate[m])
            m += 1
        
            

        









