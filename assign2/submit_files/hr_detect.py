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
    #     pyplot.savefig('hr_fig14.eps', format='eps')
    
    #initiate counters
    j = 0   #count number of peaks
    k = 0   #detection index
    m = 0   #deltat index
    
    index = np.zeros(len(hr))
    thresh = int(1/(3.66/fs))    #3.66beat/s is the maximum heart rate(220bpm)
    
    for i in range(len(hr)):
        if hr[i] == 1:
            j+=1
            for n in range(int(thresh)):    #fix the impossible detected peak to 0
                if i+n+1 <= 30000: 
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
    
    beatone = np.zeros(j)
    deltat = np.zeros(j)
    rate = np.zeros(j)
    
    for i in range(len(hr)):
        if hr[i] != 0:
            beatone[k] = i
            k += 1
            if k >= 0:          # To neglect the first detection
                deltat[m] = (beatone[m] - beatone[m-1])/fs
                # print('ONE',beatone[m])       #for diagnosis purpose
                # print('TWO',beatone[m-1])
                # print('TIME',deltat[m])
                rate[m] = (1/deltat[m])*60
                print("Momentary Heart Rate(BPM):",rate[m])
                m += 1
            
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
    

         

        









