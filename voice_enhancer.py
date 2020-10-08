import numpy as np
from matplotlib import pyplot
from scipy.io import wavfile
from scipy.io.wavfile import write

# Read WAV file
fs, data = wavfile.read('original.wav')

print("data length:",len(data))        # print for diagnostic purpose
print("sampling frequency:",fs)        # print for diagnostic purpose

xf = np.fft.fft(data)               # Fast Fourier Transform 
xfourier = xf/len(data)             # Fourier Transform Normalised
dbs = 20*np.log10(abs(xfourier))    # DB Conversion 

print("FFT data length:",len(xf))                         # print for diagnostic purpose
print("FFT normalised data length:",len(xfourier))        # print for diagnostic purpose
print("FFT normalised in dB data length:",len(dbs))       # print for diagnostic purpose

# Create x-axis for time domain plot
time = np.linspace(0,len(data)/fs,len(data))

# Plot Time Domain - raw
pyplot.figure(1)
pyplot.plot(time,data)
pyplot.title('Time domain (raw)')
pyplot.xlabel('Time(s)')
pyplot.ylabel('Amplitude')
pyplot.savefig('fig1.eps', format='eps', dpi=1200)

# Create x-axis for frequency domain plot
freq = np.linspace(0,fs,len(data))

# Plot Frequency Domain - log frequency
pyplot.figure(2)
pyplot.plot(freq, dbs)
pyplot.title('Frequency Domain (display until fs)')
pyplot.xlabel('Frequency(Hz)')
pyplot.ylabel('Amplitude(dB)')
pyplot.xscale('log')            # Log Scale
#pyplot.yscale('log')
pyplot.savefig('fig2.eps', format='eps', dpi=1200)

pyplot.figure(3)
pyplot.plot(freq, dbs)
pyplot.xlim(1,fs/2)
pyplot.title('Frequency Domain (display until fs/2)')
pyplot.xlabel('Frequency(Hz)')
pyplot.ylabel('Amplitude(dB)')
pyplot.xscale('log')            # Log Scale
#pyplot.yscale('log')
pyplot.savefig('fig3.eps', format='eps', dpi=1200)

# Find the array around 6000 - 10000 Hz
f1 = int(len(xf)/fs*6000)
f2 = int(len(xf)/fs*10000)
# Mirrored data point
f3 = len(xf) - f1
f4 = len(xf) - f2

print("6kHz data point:",f1)       # print for diagnostic purpose
print("10kHz data point:",f2)      # print for diagnostic purpose
print("data length - 6kHz:",f3)    # print for diagnostic purpose
print("data length - 10kHz:",f4)   # print for diagnostic purpose

# 6000 - 10000 hz is gained by 8
xf[f1:f2+1] *= 8
xf[f4:f3+1] *= 8

# Plot Frequency Domain - not log frequency
pyplot.figure(4)
pyplot.plot(freq,dbs)
pyplot.title('Before Modification')
pyplot.xlabel('Frequency(Hz)')
pyplot.ylabel('Amplitude(dB)')
pyplot.savefig('fig4.eps', format='eps', dpi=1200)

dbsm = 20*np.log10(abs(xf/len(data)))    # DB Conversion & Normalised for modified data
pyplot.figure(5)
pyplot.plot(freq,dbsm)
pyplot.title('After Modification')
pyplot.xlabel('Frequency(Hz)')
pyplot.ylabel('Amplitude(dB)')
pyplot.savefig('fig5.eps', format='eps', dpi=1200)

xffiltered = np.fft.ifft(xf)    # Inverse FFT

# Plot Time Domain - modified
pyplot.figure(6)
pyplot.plot(time,xffiltered)
pyplot.title('Time domain (modified)')
pyplot.xlabel('Time(s)')
pyplot.ylabel('Amplitude')
pyplot.savefig('fig6.eps', format='eps', dpi=1200)
    
write('improved.wav', fs, xffiltered.astype(data.dtype)) 