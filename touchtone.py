import numpy as np
import scipy
from numpy import loadtxt
from matplotlib import pyplot
from scipy.io.wavfile import write


lines = loadtxt("touchtone3.dat")

# Separate data into two aspects
data = lines[:,1]
time = lines[:,0] #ms

fs = 1000 #hz
# Touchtone Exported
datalist = list(data)
#write('touchtonesounds.wav', 1000, data) 
'''
for i in time:
    i *= 10
 '''   
# Plot Data
pyplot.figure(1)
pyplot.title('file touchtone')
pyplot.plot(time,datalist)

#avg = sum(data)/len(data)

#Fourier Transform
xftone = np.fft.fft(datalist) 
xftone[0] = 0   #weird bit

xfourier = xftone/len(datalist)
dbs = 20*np.log10(abs(xfourier))    # DB Conversion

freq = np.linspace(0,fs,len(datalist))

pyplot.figure(2)
pyplot.title('fft touchtone')
pyplot.plot(freq,dbs)
#pyplot.xlim(1,len(time)/2)

recording=np.array([1,1])
k=0     # grace counter
m=0     # Start Stop Cunter
thresh=50
mint=10
grace=np.zeros(len(datalist)+1)
pulse=None
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
        else:
            print("stop time:",time[i])
        m+=1
        
         
print(len(data))
print(m)

#half rect
for i in range(len(data)):
    if datalist[i]<3233:
        datalist[i]=3333

pyplot.figure(3)
pyplot.title('file touchtone halfrect')
pyplot.plot(time,data)
pyplot.xlim(2800,2900)




#failed attempts

'''
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
  '''          
    


#Peak Detector
'''
#peaks = scipy.signal.find_peaks(xftone, height = 50000, distance = 100)
freq= list(peaks[0])

print(freq)
'''
'''
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