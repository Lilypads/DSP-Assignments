import scipy.io
import numpy as np
import matplotlib.pylab as plot
from matplotlib import pyplot
from scipy.io import wavfile
from scipy.io.wavfile import write

# Read WAV file Frequency sample: 44100 Hz and Data
fs, data = wavfile.read('seashells.wav')
print(fs)

pyplot.figure(1)
pyplot.plot(data)
plot.axes.Axes.set_xlabel('time')
plot.axes.Axes.set_ylabel('amplitude')
plot.axes.Axes.set_title('Time Domain')
