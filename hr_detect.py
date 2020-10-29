import numpy as np
from matplotlib import pyplot
from numpy import loadtxt
from fir_filter import FIR_filter

cleanecg = loadtxt("shortecg.dat") 

pyplot.figure(1)
pyplot.plot(cleanecg)

template = np.empty(181)
template = cleanecg[720,900]
pyplot.figure(2)
pyplot.plot(template)

fir_coeff = template[::-1]
pyplot.figure(3)
pyplot.plot(fir_coeff)

matchfilt = FIR_filter(fir_coeff)

matchresult = matchfilt.dofilter(cleanecg)
pyplot.figure(4)
pyplot.plot(matchresult)

