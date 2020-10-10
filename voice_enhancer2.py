import numpy as np
from matplotlib import pyplot
from scipy.io import wavfile
from scipy.io.wavfile import write

# Read WAV file Frequency sample: 44100 Hz and Data
fs, data = wavfile.read(r'C:\Users\Visitor\Desktop\DSP\Brownfox.wav')

print(len(data))

xf = np.fft.fft(data)     # Fourier Transform 

xfourier = xf/len(data)   # Fourier Transform Normalised
# DB Conversion 
dbs = 20*np.log10(abs(xfourier))

print(len(xf))


arraysize = len(dbs)
total = arraysize/fs
time = np.linspace(0,total,arraysize)
# Plot Time file
pyplot.figure(1)
pyplot.title('wavfile')
pyplot.plot(time,data)
pyplot.xlabel('Time(s)')

# Freq vs Db Plot 
freq = np.linspace(0,fs,arraysize)
pyplot.figure(3)
pyplot.plot(freq, dbs)
pyplot.xlim(1,fs/2)
pyplot.title('freq vs DB')
pyplot.xlabel('Frequency(hz)')
pyplot.ylabel('Amplitude(db)')
pyplot.xscale('log')        # Log Scale
#pyplot.yscale('log')

pyplot.figure(4)
pyplot.plot(freq, dbs)
#pyplot.xlim(0,22050)
pyplot.title('freq vs DB')
pyplot.xlabel('Frequency(hz)')
pyplot.ylabel('Amplitude(db)')
pyplot.xscale('log')        # Log Scale
#pyplot.yscale('log')

# Find the array around 6000 - 10000 Hz
f1 = int(len(xf)/fs*6000)
f2 = int(len(xf)/fs*10000)
f3 = len(xf) - f1
f4 = len(xf) - f2

# Increase Bass Area
b1 = int(len(xf)/fs*60)
b2 = int(len(xf)/fs*250)
b3 = len(xf) - b1
b4 = len(xf) - b2

print(f1,f2,f3,f4)
print(b1,b2,b3,b4)

# 6000 - 10000 hz is gained by
gain = 8
#xf[f1:f2+1] *= gain
#xf[f4:f3+1] *= gain

# 6000 - 10000 hz is gained by
bassgain = 2

pyplot.figure(7)
pyplot.plot(xf)

xf[b1:b2+1] *= bassgain
xf[b4:b3+1] *= bassgain


pyplot.figure(5)
pyplot.plot(xf)

xffiltered = np.fft.ifft(xf)

pyplot.figure(6)
pyplot.plot(xffiltered)
    
write('output5.wav', fs, xffiltered.astype(data.dtype)) 
