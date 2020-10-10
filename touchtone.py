import numpy as np
import scipy
from numpy import loadtxt
from matplotlib import pyplot
from scipy.io.wavfile import write


lines = loadtxt("touchtone3.dat")

# Separate data into two aspects
data = lines[:,1]
time = lines[:,0]

# Touchtone Exported
datalist = list(data)
write('touchtonesounds.wav', 1000, data) 

for i in time:
    i *= 10
    
# Plot Data
pyplot.figure(1)
pyplot.title('file touchtone')
pyplot.plot(time,datalist)

avg = sum(data)/len(data)

#Fourier Transform
xftone = np.fft.fft(data) 
xftone[0] = 0



pyplot.figure(2)
pyplot.title('fft touchtone')
pyplot.plot(xftone)
#pyplot.xlim(1,len(time)/2)

#Peak Detector

peaks = scipy.signal.find_peaks(xftone, height = 50000, distance = 100)
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

