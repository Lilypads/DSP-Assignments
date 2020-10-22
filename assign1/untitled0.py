import numpy as np
import scipy
from numpy import loadtxt
from matplotlib import pyplot
from scipy.io import wavfile
from scipy import signal
from scipy.io.wavfile import write

fs, data = wavfile.read('Dtmf4.wav')

print(fs)

xftone = np.fft.fft(data)
xfourier = xftone/len(data)
dbs = 20*np.log10(abs(xfourier)) 

freq = np.linspace(0,fs,len(data))

peaks = scipy.signal.find_peaks(dbs, height=70)  
print(peaks)

pyplot.plot(freq,dbs)
pyplot.xlim(600,1600)