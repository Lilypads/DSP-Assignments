import numpy as np
from numpy import loadtxt
from matplotlib import pyplot

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
#pyplot.savefig('tt_fig1.eps', format='eps')

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
#pyplot.savefig('tt_fig2.eps', format='eps')

# Zoomed version for diagnostic purpose
pyplot.figure(3)
pyplot.title('file touchtone partly')
pyplot.plot(time,data)
pyplot.xlim(2800,2900)
pyplot.xlabel('Time(ms)')
pyplot.ylabel('Amplitude')
#pyplot.savefig('tt_fig3.eps', format='eps')

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
    
    '''
    if index==0:
        pyplot.savefig('tt_fig4.eps', format='eps')
    if index==1:
        pyplot.savefig('tt_fig5.eps', format='eps')
    if index==2:
        pyplot.savefig('tt_fig6.eps', format='eps')
    if index==3:
        pyplot.savefig('tt_fig7.eps', format='eps')
    if index==4:
        pyplot.savefig('tt_fig8.eps', format='eps')
    if index==5:
        pyplot.savefig('tt_fig9.eps', format='eps')
    if index==6:
        pyplot.savefig('tt_fig10.eps', format='eps')
    if index==7:
        pyplot.savefig('tt_fig11.eps', format='eps')
    if index==8:
        pyplot.savefig('tt_fig12.eps', format='eps')
    if index==9:
        pyplot.savefig('tt_fig13.eps', format='eps')
    if index==10:
        pyplot.savefig('tt_fig14.eps', format='eps')
    if index==11:
        pyplot.savefig('tt_fig15.eps', format='eps')
    if index==12:
        pyplot.savefig('tt_fig16.eps', format='eps')
    '''
    
    #print(max(dbs))     # print for diagnostic purpose
    #find data point at respective frequencies
    n697 = int(len(section)/fs*np.abs(fs-697))        
    n770 = int(len(section)/fs*np.abs(fs-770))      
    n852 = int(len(section)/fs*np.abs(fs-852)) 
    n941 = int(len(section)/fs*np.abs(fs-941))
    n1209 = int(len(section)/fs*np.abs(fs-1209)) 
    n1336 = int(len(section)/fs*np.abs(fs-1336)) 
    n1477 = int(len(section)/fs*np.abs(fs-1477))
    #print(n1209)        # print for diagnostic purpose
  
    numb=-1                                         # cannot detect any number arg
    offset=18
    if (max(dbs[n697-offset:n697+offset]) > 20) and (max(dbs[n1209-offset:n1209+offset]) > 20):      # use 20dB as threshold
        numb=1
    elif (max(dbs[n697-offset:n697+offset]) > 20) and (max(dbs[n1336-offset:n1336+offset]) > 20):
        numb=2
    elif (max(dbs[n697-offset:n697+offset]) > 20) and (max(dbs[n1477-offset:n1477+offset]) > 20):
        numb=3
    elif (max(dbs[n770-offset:n770+offset]) > 20) and (max(dbs[n1209-offset:n1209+offset]) > 20):
        numb=4
    elif (max(dbs[n770-offset:n770+offset]) > 20) and (max(dbs[n1336-offset:n1336+offset]) > 20):
        numb=5
    elif (max(dbs[n770-offset:n770+offset]) > 20) and (max(dbs[n1477-offset:n1477+offset]) > 20):
        numb=6
    elif (max(dbs[n852-offset:n852+offset]) > 20) and (max(dbs[n1209-offset:n1209+offset]) > 20):
        numb=7
    elif (max(dbs[n852-offset:n852+offset]) > 20) and (max(dbs[n1336-offset:n1336+offset]) > 20):
        numb=8
    elif (max(dbs[n852-offset:n852+offset]) > 20) and (max(dbs[n1477-offset:n1477+offset]) > 20):
        numb=9
    elif (max(dbs[n941-offset:n941+offset]) > 20) and (max(dbs[n1336-offset:n1336+offset]) > 20):
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
start,stop = oneDigit(data,time)        # Get Start Stop Time arrays
for i in range(13):
    num = plotFreq(i,data,start[i],stop[i])     # Process each section
    if num == -1:
        print("Cannot detect number.")
    else: 
        print("The number pressed:",num)            # Print output number

