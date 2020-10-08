import scipy.io
import numpy as np
#import matplotlib.pylab as plot
from matplotlib import pyplot
from scipy.io import wavfile
from scipy.io.wavfile import write

# Read WAV file Frequency sample: 44100 Hz and Data
fs, data = wavfile.read('original.wav')


pyplot.figure(1)
pyplot.ylabel('amplitude')
pyplot.xlabel('time')
pyplot.plot(data)

'''
xf = np.fft.fft(data)   # Fourier Transform


# DB Conversion (Im not sure about this either)
dbs = 20*np.log10(data)
pyplot.figure(2)
pyplot.plot(dbs,tlog)


length= len(xf)
arraysize = len(dbs)
total = arraysize/fs
time = np.linspace(0,total,arraysize)

# Db VS time Plot
pyplot.figure(3)
pyplot.plot(time,abs(dbs))

# Freq vs Db Plot 
freq = np.linspace(0,fs,length)
pyplot.figure(4)
pyplot.plot(freq,abs(dbs))
pyplot.xscale('log')        # Log Scale
pyplot.yscale('log')

f1 = len(dbs)/fs*6000
f2 = len(dbs)/fs*10000
f3 = len(dbs) - int(f1)
f4 = len(dbs) - int(f2)

print(f1)
print(f2)
print(f3)
print(f4)

dbs[int(f1):int(f2)+1] = dbs[int(f1):int(f2)+1]*2


pyplot.figure(5)
pyplot.plot(freq,abs(dbs))
pyplot.xscale('log')        # Log Scale
pyplot.yscale('log')

# Convert back to non db units
nondb = 10 ** (dbs / 20)

dbfilter = np.fft.ifft(nondb)
    
pyplot.figure(6)
pyplot.plot(nondb)

write('improved.wav', fs, dbfilter.astype(data.dtype)) 
'''