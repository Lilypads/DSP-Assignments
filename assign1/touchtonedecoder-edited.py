import numpy as np
import scipy
from numpy import loadtxt
from matplotlib import pyplot
from scipy.io.wavfile import write
from scipy import signal

# Load data
lines = loadtxt("touchtones8.dat")

# Separate data into two aspects
data = lines[:,1]
time = lines[:,0] #ms

fs = 1000 #hz
print("data length:",len(data))        # print for diagnostic purpose

# Plot Time Domain
#pyplot.figure(1)
#pyplot.title('file touchtone')
#pyplot.plot(time,data)
#pyplot.xlabel('Time(ms)')
#pyplot.ylabel('Amplitude')

# Plot Frequency Domain
xftone = np.fft.fft(data) 
xftone[0] = 0   # deleting weird bit
xfourier = xftone/len(data)         # Normalised Data
dbs = 20*np.log10(abs(xfourier))    # DB Conversion
freq = np.linspace(0,fs,len(data))

#pyplot.figure(2)
#pyplot.title('fft touchtone')
#pyplot.plot(freq,dbs)
#pyplot.xlabel('Frequency(Hz)')
#pyplot.ylabel('Amplitude(dB)')

# Zoomed version for diagnostic purpose
#pyplot.figure(3)
#pyplot.title('file touchtone partly')
#pyplot.plot(time,data)
#pyplot.xlim(2800,2900)
#pyplot.xlabel('Time(ms)')
#pyplot.ylabel('Amplitude')

# Plot Section Frequency Spectrum + Detect Number
count = 0
def plotFreq(index,data,start,stop):
    global count
    count +=1
    
    section=np.empty(stop-start)    # Initialise Empty Array
    for i in range(stop-start):
        section[i]=data[start+i]
    #time=np.linspace(0,stop-start,1)
    xfsection = np.fft.fft(section)         # Fourier transform the whole thing
    xfourier = xfsection/len(section)
    dbs = 20*np.log10(abs(xfourier))
    dbs[0] = -20        # deleting weird bit
    freq = np.linspace(0,fs,len(section))
    
#    pyplot.figure(index+4)
#    pyplot.title('fft section')
#    pyplot.plot(freq,dbs)
#    pyplot.xlim(0,fs)
#    pyplot.xlabel('Frequency(Hz)')
#    pyplot.ylabel('Amplitude(dB)')
    
    # split frequency into two to erase mirror  
    dbsS = np.array_split(dbs, 2)
    dbsa = dbsS[0]            # dbsa array is the first half of the set of the data
    
    # find the fiirst frequency of the peak of the 
    result = np.where(dbsa == np.amax(dbsa))
    maxs = result[0]
    maxf = int(maxs/len(section)*1000) 
    dbsb = np.delete(dbsa,maxs)
    result2 = np.where(dbsb == np.amax(dbsb))
    maxs2 = result2[0]
    maxf2 = int(maxs2[0]/len(section)*1000)
    
    # Decide which peak corresponds to either the high tone frequency or the low tone 
    if maxs[0] > maxs2[0]: 
   #     dbs1 = dbsa
    #    dbs2 = dbsb
        freq2 = maxf + 1000           # Reverse fold-down method 
        freq1 = abs(maxf2 - 1000)
    elif maxs[0] < maxs2[0]:
   #     dbs1 = dbsb
    #    dbs2 = dbsa
        freq2 = maxf2 + 1000
        freq1 = abs(maxf - 1000) 
    
    # print detected frequency 
    print(freq1)
    print(freq2)
    '''    
    pyplot.figure(index+4)
    pyplot.title('fft section')
    pyplot.plot(dbs1)
    pyplot.plot(dbs2)
    pyplot.xlim(0,fs)
    pyplot.xlabel('Frequency(Hz)')
    pyplot.ylabel('Amplitude(dB)')
    ''' 
  
    numb=-1                                          # cannot detect any number arg
    omin = 40
    omax = 40
    if ((697-omin) < freq2 < (697+omax)) and ((1209-omin) < freq1 < (1209+omax)):      # use 20dB as threshold
        numb=1
    elif ((697-omin) < freq1 < (697+omax)) and ((1336-omin) < freq2 < (1336+omax)):      # use 20dB as threshold
        numb=2
    elif ((697-omin) < freq1 < (697+omax)) and ((1477-omin) < freq2 < (1477+omax)):      # use 20dB as threshold
        numb=3
    elif ((770-omin) < freq2 < (770+omax)) and ((1209-omin) < freq1 < (1209+omax)):      # use 20dB as threshold
        numb=4
    elif ((770-omin) < freq1 < (770+omax)) and ((1336-omin) < freq2 < (1336+omax)):      # use 20dB as threshold
        numb=5
    elif ((770-omin) < freq1 < (770+omax)) and ((1477-omin) < freq2 < (1477+omax)):      # use 20dB as threshold
        numb=6
    elif ((852-omin) < freq1 < (852+omax)) and ((1209-omin) < freq2 < (1209+omax)):      # use 20dB as threshold
        numb=7
    elif ((852-omin) < freq1 < (852+omax)) and ((1336-omin) < freq2 < (1336+omax)):      # use 20dB as threshold
        numb=8
    elif ((852-omin) < freq1 < (852+omax)) and ((1477-omin) < freq2 < (1477+omax)):      # use 20dB as threshold
        numb=9
    elif ((941-omin) < freq1 < (941+omax)) and ((1336-omin) < freq2 < (1336+omax)):      # use 20dB as threshold
        numb=0
    return numb

    # End of Function


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
                    stop[k]=time[i]-10
                    k+=1
            m+=1
            #print(m)        # print for diagnostic purpose
    #print(start)            # print for diagnostic purpose
    #print(stop)             # print for diagnostic purpose
    return start,stop



     
# Main Function   
start=np.empty(13,dtype=int)
stop=np.empty(13,dtype=int) 
dial=np.empty(13,dtype=int) 
start,stop = oneDigit(data,time)        # Get Start Stop Time
for i in range(13):
    num = plotFreq(i,data,start[i],stop[i]) # Process each section
    dial[i] = num
    if num == -1:
        print("Cannot detect number.")
    else: 
        print("The number pressed:",num)

print(dial)



















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