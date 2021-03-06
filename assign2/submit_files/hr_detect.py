import numpy as np
from matplotlib import pyplot
from numpy import loadtxt
from fir_filter import FIR_filter

Case = 0
#Case = int(input("Case 0 For shortecg.dat. Case 1 For Einthoven_ii Walking. Please enter case number: "))
for Case in range (2):
    if Case == 0:
        cleanecg = loadtxt("shortecg.dat")
    if Case == 1:
        cleanecg = loadtxt("shorteint.dat") 
        
    fs=250      #sampling frequency of the data
    
    pyplot.figure(8*Case+1)
    time = np.linspace(0,len(cleanecg)/fs,len(cleanecg))
    pyplot.plot(time,cleanecg)
    pyplot.title('ecg (filtered)')
    pyplot.xlabel('Time(s)')
    pyplot.ylabel('Amplitude')
    # if Case == 0:
    #     pyplot.savefig('hr_fig1.eps', format='eps')
    # if Case == 1:
    #     pyplot.savefig('hr_fig9.eps', format='eps')
    
    #ecg templates for each data set
    if Case == 0:
        template=cleanecg[775:975] 
    if Case == 1:
        template=cleanecg[7050:7225] 
     
    #plot template
    pyplot.figure(8*Case+2)
    time2 = np.linspace(0,len(template)/fs,len(template))
    pyplot.plot(time2,template)
    pyplot.title('1 ecg')
    pyplot.xlabel('Time(s)')
    pyplot.ylabel('Amplitude')
    # if Case == 0:
    #     pyplot.savefig('hr_fig2.eps', format='eps')
    # if Case == 1:
    #     pyplot.savefig('hr_fig10.eps', format='eps')
    
    #inverse the template
    fir_coeff = template[::-1]
    pyplot.figure(8*Case+3)
    pyplot.plot(time2,fir_coeff)
    pyplot.title('reversed 1 ecg')
    pyplot.xlabel('Time(s)')
    pyplot.ylabel('Amplitude')
    # if Case == 0:
    #     pyplot.savefig('hr_fig3.eps', format='eps')
    # if Case == 1:
    #     pyplot.savefig('hr_fig11.eps', format='eps')
    
    #matched filtered data    
    matchfilt = FIR_filter(fir_coeff)
    
    matchresult = np.zeros(len(cleanecg))
    for i in range(len(cleanecg)):
        matchresult[i] = matchfilt.dofilter(cleanecg[i])
    
    pyplot.figure(8*Case+4)
    pyplot.plot(time,matchresult)
    pyplot.title('Matched Filtered ecg')
    pyplot.xlabel('Time(s)')
    pyplot.ylabel('Amplitude')
    # if Case == 0:
    #     pyplot.savefig('hr_fig4.eps', format='eps')
    # if Case == 1:
    #     pyplot.savefig('hr_fig12.eps', format='eps')
    print(len(matchresult))
    
    #squared matched filtered data 
    matchresult = matchresult*matchresult
    pyplot.figure(8*Case+5)
    pyplot.plot(time,matchresult)           #
    pyplot.title('Squared Matched Filtered ecg')
    pyplot.xlabel('Time(s)')
    pyplot.ylabel('Amplitude')
    # if Case == 0:
    #     pyplot.savefig('hr_fig5.eps', format='eps')
    # if Case == 1:
    #     pyplot.savefig('hr_fig13.eps', format='eps')
    
    #using threshold to extract the peaks
    hr = np.zeros(len(matchresult))
    threshold = 0.00000000002 
    for i in range(len(matchresult)):
        if matchresult[i]>threshold:
            hr[i]=1
            
    pyplot.figure(8*Case+6)
    pyplot.plot(hr)
    pyplot.title('Heart Beat Detection Sequence')
    pyplot.xlabel('Sample number')
    pyplot.ylabel('Amplitude')
    #pyplot.xlim(3,120)             #to delete the first part where the buffer is being filled/diagnosis purpose
    # if Case == 0:
    #     pyplot.savefig('hr_fig6.eps', format='eps')
    # if Case == 1:
    #       pyplot.savefig('hr_fig14.eps', format='eps')
    
    #initiate counters
    peakCounter = 0   #count number of peaks > for array size
    detectIndex = 0   #detection index
    deltatIndex = 0   #deltat index
    
    index = np.zeros(len(hr))
    thresh = int(1/(3.66/fs))    #3.66beat/s is the maximum heart rate(220bpm)
    
    for i in range(len(hr)):
        if hr[i] == 1:
            peakCounter+=1
            for n in range(int(thresh)):    #fix the impossible detected peak to 0
                if i+n+1 <= 30000:          #If the time is less than 30000 
                    hr[i+n+1] = 0
    
    pyplot.figure(8*Case+7)
    pyplot.plot(hr)
    pyplot.title('Heart Beat Detection Sequence Fixed')
    pyplot.xlabel('Sample number')
    pyplot.ylabel('Amplitude')
    #pyplot.xlim(3,120)         #to delete the first part where the buffer is being filled/diagnosis purpose
    # if Case == 0:
    #     pyplot.savefig('hr_fig7.eps', format='eps')
    # if Case == 1:
    #     pyplot.savefig('hr_fig15.eps', format='eps')
    
    beatone = np.zeros(peakCounter)
    deltat = np.zeros(peakCounter)
    rate = np.zeros(peakCounter)
    
    print("Momentary Heart Rate(BPM)")
    for i in range(len(hr)):
        if hr[i] != 0:          # When element is not zero, input element to new array
            beatone[detectIndex] = i
            detectIndex += 1
            if detectIndex >= 0:          # To neglect the first detection
                deltat[deltatIndex] = (beatone[deltatIndex] - beatone[deltatIndex-1])/fs
                # print('ONE',beatone[deltatIndex])       #for diagnosis purpose
                # print('TWO',beatone[deltatIndex-1])
                # print('TIME',deltat[deltatIndex])
                rate[deltatIndex] = (1/deltat[deltatIndex])*60
                print(rate[deltatIndex])
                deltatIndex += 1
            
    pyplot.figure(8*Case+8)
    pyplot.plot(beatone/fs,rate)
    pyplot.title('Heart Rate Plot')
    pyplot.xlabel('Time(s)')
    pyplot.ylabel('Beats/Minute')
    #pyplot.xlim(4,max(beatone)/fs+1)        #to delete the first part where the buffer is being filled/diagnosis purpose
    # if Case == 0:
    #     pyplot.savefig('hr_fig8.eps', format='eps')
    # if Case == 1:
    #     pyplot.savefig('hr_fig16.eps', format='eps')
 

class HR_filter:
    def __init__(self,): 
        ecg = loadtxt("shortecg.dat")           #file which the template is extracted from
        template=ecg[775:975]                   #1ecg of the corresponding file
        fir_coeff = template[::-1]              #reverse template
        self.matchfilt = FIR_filter(fir_coeff)  
        self.hr = 0
        self.hrBuffer = 0                       #keep previous hr value for peak starts checking
        self.counter = 0                        #counts time difference before next peak arrive
        
    def realtimeHR(self,data,fs):        
        matchresult = self.matchfilt.dofilter(data)
        matchresult = matchresult*matchresult
        threshold = 0.00000000002               #observed by eye from graph
        
        #use threshold to extract peak area
        if matchresult>threshold:
            self.hr=1
        else:
            self.hr=0
        
        thresh = int(1/(3.66/fs))               #3.66beat/s is the maximum heart rate(220bpm)
        rate=0                                  #argument if another heart beat has not arrived
        
        #checks if the peak starts
        if self.hrBuffer==0 and self.hr==1:
            #peak=1      #for diagnosis purpose : peak starts
            if self.counter>thresh:
                rate = (fs/self.counter)*60
            self.counter=0                      #reset counter
        else:
            #peak=0      #for diagnosis purpose : no peak starting
            self.counter+=1
            
        return rate
        self.hrBuffer = self.hr                 #save value for future comparison

'''
#Example Use
data = loadtxt("shortecg.dat") 
fs=250
mhr = np.zeros(len(data))
hrfilt = HR_filter()                            #instantiate the HR_filter
for i in range(len(data)):
    mhr[i] = hrfilt.realtimeHR(data[i],fs)
    
pyplot.figure(17)
pyplot.plot(np.linspace(0,len(data)/fs,len(data)),mhr)
pyplot.title('Momentary Heart Rate Plot')
pyplot.xlabel('Time(s)')
pyplot.ylabel('Beats/Minute')
pyplot.savefig('hr_fig17.eps', format='eps')
'''







