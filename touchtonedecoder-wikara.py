import numpy as np
import scipy
from numpy import loadtxt
from matplotlib import pyplot
from scipy.io.wavfile import write

# Load data
lines = loadtxt("touchtones.dat")

# Separate data into two aspects
data = lines[:,1]
time = lines[:,0] #ms

fs = 1000 #hz
print("data length:",len(data))        # print for diagnostic purpose

# Plot Time Domain
pyplot.figure(1)
pyplot.title('file touchtone')
pyplot.plot(time,data)
pyplot.xlabel('Time(ms)')
pyplot.ylabel('Amplitude')

# Plot Frequency Domain
xftone = np.fft.fft(data) 
xftone[0] = 0   # deleting weird bit
xfourier = xftone/len(data)         # Normalised Data
dbs = 20*np.log10(abs(xfourier))    # DB Conversion
freq = np.linspace(0,fs,len(data))

pyplot.figure(2)
pyplot.title('fft touchtone')
pyplot.plot(freq,dbs)
pyplot.xlabel('Frequency(Hz)')
pyplot.ylabel('Amplitude(dB)')

# Zoomed version for diagnostic purpose
pyplot.figure(3)
pyplot.title('file touchtone partly')
pyplot.plot(time,data)
pyplot.xlim(2800,2900)
pyplot.xlabel('Time(ms)')
pyplot.ylabel('Amplitude')

# Plot Section Frequency Spectrum + Detect Number
def plotFreq(index,data,start,stop):
    section=np.empty(stop-start)    # Initialise Empty Array
    for i in range(stop-start):
        section[i]=data[start+i]
    #time=np.linspace(0,stop-start,1)
    xfsection = np.fft.fft(section)         # Fourier transform the whole thing
    xfourier = xfsection/len(section)       # Normalise
    dbs = 20*np.log10(abs(xfourier))
    dbs[0] = -20        # deleting weird bit
    
    freq = np.linspace(0,fs,len(section))
    pyplot.figure(index)
    pyplot.title('fft section')
    pyplot.plot(freq,dbs)
    pyplot.xlim(0,fs/2)
    pyplot.xlabel('Frequency(Hz)')
    pyplot.ylabel('Amplitude(dB)')
    
    print(max(dbs))
    #find data point at respective frequencies
    n697 = int(len(section)/fs*697)        
    n770 = int(len(section)/fs*770)      
    n852 = int(len(section)/fs*852) 
    n941 = int(len(section)/fs*941)
    n1209 = int(len(section)/fs*330) 
    n1336 = int(len(section)/fs*1336) 
    n1477 = int(len(section)/fs*1477)
    #print(n1209)        # print for diagnostic purpose
  
    numb=-1                                         # cannot detect any number arg
    if (dbs[n697] > 10) and (dbs[n1209] > 10):      # use 10dB as threshold
        numb=1
    elif (dbs[n697] > 10) and (dbs[n1336] > 10):
        numb=2
    elif (dbs[n697] > 10) and (dbs[n1477] > 10):
        numb=3
    elif (dbs[n770] > 10) and (dbs[n1209] > 10):
        numb=4
    elif (dbs[n770] > 10) and (dbs[n1336] > 10):
        numb=5
    elif (dbs[n770] > 10) and (dbs[n1477] > 10):
        numb=6
    elif (dbs[n852] > 10) and (dbs[n1209] > 10):
        numb=7
    elif (dbs[n852] > 10) and (dbs[n1336] > 10):
        numb=8
    elif (dbs[n852] > 10) and (dbs[n1477] > 10):
        numb=9
    elif (dbs[n941] > 10) and (dbs[n1336] > 10):
        numb=0
    return numb

# Section Split Time Finder
def oneDigit(data,time):
    start=np.empty(13,dtype=int)    # has 13 sections
    stop=np.empty(13,dtype=int)
    g=0     # grace counter
    m=0     # Start + Stop counter
    j=0     # Start counter
    k=0     # Stop counter
    thresh=50
    mint=10
    grace=np.zeros(len(data)+1)
    for i in range(len(data)):
        if np.abs(data[i]-3235)<thresh:
            g+=1
            if g>mint:
                grace[i]=1
        if np.abs(data[i]-3235)>thresh:
            grace[i]=0
            g=0
        if grace[i-1]!=grace[i]:
            #print(grace[i])        # print for diagnostic purpose
            if grace[i]==0:
                #print("start time:",time[i])
                start[j]=time[i]
                j+=1
            else:
                #print("stop time:",time[i])
                if m>0:       # we don't want first stop to be saved
                    stop[k]=time[i]
                    k+=1
            m+=1
            #print(m)        # print for diagnostic purpose
    #print(start)            # print for diagnostic purpose
    #print(stop)             # print for diagnostic purpose
    return start,stop



     
# Main Function   
start=np.empty(13,dtype=int)
stop=np.empty(13,dtype=int) 
start,stop = oneDigit(data,time)        # Get Start Stop Time
for i in range(13):
    num = plotFreq(i,data,start[i],stop[i])     # Process each section
    if num == -1:
        print("Cannot detect number.")
    else: 
        print("The number pressed:",num)            # Print output number



















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