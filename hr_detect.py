import numpy as np
from matplotlib import pyplot
from numpy import loadtxt
from fir_filter import FIR_filter

cleanecg = loadtxt("shortecg.dat") 

pyplot.figure(1)
pyplot.plot(cleanecg)

#720-900
template=cleanecg[720:900]    
    
pyplot.figure(2)
pyplot.plot(template)

fir_coeff = template[::-1]
pyplot.figure(3)
pyplot.plot(fir_coeff)

matchfilt = FIR_filter(fir_coeff)

matchresult = np.zeros(len(cleanecg))
for i in range(len(cleanecg)):
    matchresult[i] = matchfilt.dofilter(cleanecg[i])
    
pyplot.figure(4)
pyplot.plot(matchresult)

matchresult = matchresult*matchresult
pyplot.figure(5)
pyplot.plot(matchresult)

hr = np.zeros(len(matchresult))
threshold = 0.00000000002
for i in range(len(matchresult)):
    if matchresult[i]>threshold:
        hr[i]=1

pyplot.figure(6)
pyplot.plot(hr)