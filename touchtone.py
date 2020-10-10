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

# Cutting time finder
def oneDigit(data):
    start=np.empty(13)
    stop=np.empty(13)
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