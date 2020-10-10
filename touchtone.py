import numpy as np
import scipy
from numpy import loadtxt
from matplotlib import pyplot
from scipy.io.wavfile import write

# Load data
lines = loadtxt("touchtone3.dat")

# Separate data into two aspects
data = lines[:,1]
time = lines[:,0] #ms

fs = 1000 #hz
print(len(data))

# Plot Data
pyplot.figure(1)
pyplot.title('file touchtone')
pyplot.plot(time,data)
pyplot.xlabel('Time(ms)')
pyplot.ylabel('Amplitude')

#avg = sum(data)/len(data)

#Fourier Transform
xftone = np.fft.fft(data) 
xftone[0] = 0   # deleting weird bit

xfourier = xftone/len(data)
dbs = 20*np.log10(abs(xfourier))    # DB Conversion

freq = np.linspace(0,fs,len(data))

pyplot.figure(2)
pyplot.title('fft touchtone')
pyplot.plot(freq,dbs)
pyplot.xlabel('Frequency(Hz)')
pyplot.ylabel('Amplitude(dB)')

pyplot.figure(3)
pyplot.title('file touchtone partly')
pyplot.plot(time,data)
pyplot.xlim(2800,2900)
pyplot.xlabel('Time(ms)')
pyplot.ylabel('Amplitude')

# Plot frequency
def plotFreq(index,data,start,stop):
    section=np.empty(stop-start)
    for i in range(stop-start):
        section[i]=data[start+i]
    #time=np.linspace(0,stop-start,1)
    xfsection = np.fft.fft(section)
    xfsection[0] = 0        # deleting weird bit
    xfourier = xfsection/len(section)
    dbs = 20*np.log10(abs(xfourier))
    freq = np.linspace(0,fs,len(section))
    pyplot.figure(index+4)
    pyplot.title('fft section')
    pyplot.plot(freq,dbs)
    pyplot.xlabel('Frequency(Hz)')
    pyplot.ylabel('Amplitude(dB)')
    
    #find data point at respective frequencies
    n697 = int(len(xfsection)/fs*697)        
    n770 = int(len(xfsection)/fs*770)      
    n852 = int(len(xfsection)/fs*852) 
    n941 = int(len(xfsection)/fs*941)
    n1209 = int(len(xfsection)/fs*1209) 
    n1336 = int(len(xfsection)/fs*1336) 
    n1477 = int(len(xfsection)/fs*1477) 
    
    if dbs[n697] > 10 and dbs[n1209] > 10:
        number=1
    if dbs[n697] > 10 and dbs[n1336] > 10:
        number=2
    if dbs[n697] > 10 and dbs[n1477] > 10:
        number=3
    if dbs[n770] > 10 and dbs[n1209] > 10:
        number=4
    if dbs[n770] > 10 and dbs[n1336] > 10:
        number=5
    if dbs[n770] > 10 and dbs[n1477] > 10:
        number=6
    if dbs[n852] > 10 and dbs[n1209] > 10:
        number=7
    if dbs[n852] > 10 and dbs[n1336] > 10:
        number=8
    if dbs[n852] > 10 and dbs[n1477] > 10:
        number=9
    if dbs[n941] > 10 and dbs[n1336] > 10:
        number=0
    return number

# Cutting time finder
def oneDigit(data,time):
    start=np.empty(13,dtype=int)
    stop=np.empty(13,dtype=int)
    k=0     # grace ounter
    m=0     # Start + Stop counter
    j=0     # Start counter
    n=0     # Stop counter
    thresh=50
    mint=10
    grace=np.zeros(len(data)+1)
    for i in range(len(data)):
        if np.abs(data[i]-3235)<thresh:
            k+=1
            if k>mint:
                grace[i]=1
        if np.abs(data[i]-3235)>thresh:
            grace[i]=0
            k=0
        if grace[i-1]!=grace[i]:
            print(grace[i])
            if grace[i]==0:
                print("start time:",time[i])
                start[j]=time[i]
                j+=1
            else:
                print("stop time:",time[i])
                if m>0:             # we don't want first stop to be saved
                    stop[n]=time[i]
                    n+=1
                m+=1
    print(m)
    print(start)
    print(stop)
    return start,stop
        
start=np.empty(13,dtype=int)
stop=np.empty(13,dtype=int) 
start,stop = oneDigit(data,time)
for i in range(13):
    number = plotFreq(i,data,start[i],stop[i])
    print(number)

'''
# Sectioning each number
np.empty((j,stop[i]-start[i]))
for i in range(j):
    for b in range(stop[i]-start[i]+1):
        section = 
        section[i,b] = data[start[i]+b]
        
 '''     


'''
#half rect
datalist = list(data)
for i in range(len(data)):
    if datalist[i]<3233:
        datalist[i]=3333

#failed attempts
k=0
m=0
n=0
thresh=50
mint=700
for i in range(len(data)):
    if np.abs(data[i]-3235)<thresh:
        k+=1
    else:
        k=0
        n=+1
    if k>mint:
        silence=True
        m+=1
        k=0
    else:
        silence=False
        
    print(silence)
print(len(data))
print(n)
print(m)          

#Peak Detector
#peaks = scipy.signal.find_peaks(xftone, height = 50000, distance = 100)
freq= list(peaks[0])
print(freq)

#Frequency Parser
for i in freq:
    if 1000 < i < 2000:
        print('1')
    if 2000 < i < 3000:
        print('8')
    if 4000 < i < 5000:
        print('2')
    if 7000 < i < 8000:
        print('3')
    if 9000 < i < 10000:
        print('4')
    if 10000 < i < 11000:
        print('5')
    if 13000 < i < 14000:
        print('7')
    if 14000 < i < 15000:
        print('6')

'''