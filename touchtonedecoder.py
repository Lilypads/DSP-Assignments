import numpy as np
from numpy import loadtxt
from matplotlib import pyplot
#from scipy import signal

# Load data
lines = loadtxt("touchtones.dat")

# Separate data into two aspects
data = lines[:,1]
time = lines[:,0] #ms

fs = 1000 #hz
print("data length:",len(data))        # print for diagnostic purpose

#Plot Time Domain
pyplot.figure(1)
pyplot.title('file touchtone')
pyplot.plot(time,data)
pyplot.xlabel('Time(ms)')
pyplot.ylabel('Amplitude')
pyplot.savefig('tt_fig1.eps', format='eps')

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
pyplot.savefig('tt_fig2.eps', format='eps')

# Zoomed version for diagnostic purpose
pyplot.figure(3)
pyplot.title('file touchtone partly')
pyplot.plot(time,data)
pyplot.xlim(2800,2900)
pyplot.xlabel('Time(ms)')
pyplot.ylabel('Amplitude')
pyplot.savefig('tt_fig3.eps', format='eps')

# Plot Section Frequency Spectrum + Detect Number
count = 0
def plotFreq(index,data,start,stop):
    global count
    count +=1
    
    section=np.empty(stop-start)    # Initialise Empty Array
    for i in range(stop-start):
        section[i]=data[start+i]
    #time=np.linspace(0,stop-start,1)
    xfsection = np.fft.fft(section)         # Fourier transfor the whole thing
    xfourier = xfsection/len(section)
    dbs = 20*np.log10(abs(xfourier))
    dbs[0] = -20        # deleting weird bit
    freq = np.linspace(0,fs,len(section))
    pyplot.figure(index+4)
    pyplot.title('fft section')
    pyplot.plot(freq,dbs)
    pyplot.xlim(0,fs/2)
    pyplot.xlabel('Frequency(Hz)')
    pyplot.ylabel('Amplitude(dB)')
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
    
    
    #find data point at respective frequencies either add or minus 1000
    print("Section Length:",len(section))   # print for diagnostic purpose
    n697 = int((abs(697-fs))/fs*len(section))   
    n770 = int((abs(770-fs))/fs*len(section))       
    n852 = int((abs(852-fs))/fs*len(section))   
    n941 = int((abs(941-fs))/fs*len(section))
    n1209 = int((abs(1209-fs))/fs*len(section)) 
    n1336 = int((abs(1336-fs))/fs*len(section)) 
    n1477 = int((abs(1477-fs))/fs*len(section))
    
    #findpeaks 
    #peaks = scipy.signal.find_peaks(dbs, height=10)  
    #print("Peaks:",peaks[0])        # print for diagnostic purpose
    #print(n770,n1209)              # print for diagnostic purpose
    

    numb=-1                                          # cannot detect any number arg
    offs=18
                                    
    if (max(dbs[n697-offs:n697+offs]) > 20) and (max(dbs[n1209-offs:n1209+offs]) > 20):      # use 20dB as threshold
        numb=1
    if (max(dbs[n697-offs:n697+offs]) > 20) and (max(dbs[n1336-offs:n1336+offs]) > 20):      # use 20dB as threshold
        numb=2
    if (max(dbs[n697-offs:n697+offs]) > 20) and (max(dbs[n1477-offs:n1477+offs]) > 20):     
        numb=3
    if (max(dbs[n770-offs:n770+offs]) > 20) and (max(dbs[n1209-offs:n1209+offs]) > 20):
        numb=4
    if (max(dbs[n770-offs:n770+offs]) > 20) and (max(dbs[n1336-offs:n1336+offs]) > 20):
        numb=5
    if (max(dbs[n770-offs:n770+offs]) > 20) and (max(dbs[n1477-offs:n1477+offs]) > 20):
        numb=6
    if (max(dbs[n852-offs:n852+offs]) > 20) and (max(dbs[n1209-offs:n1209+offs]) > 20):
        numb=7
    if (max(dbs[n852-offs:n852+offs]) > 20) and (max(dbs[n1336-offs:n1336+offs]) > 20):
        numb=8
    if (max(dbs[n852-offs:n852+offs]) > 20) and (max(dbs[n1477-offs:n1477+offs]) > 20):
        numb=9
    if (max(dbs[n941-offs:n941+offs]) > 20) and (max(dbs[n1336-offs:n1336+offs]) > 20):
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

