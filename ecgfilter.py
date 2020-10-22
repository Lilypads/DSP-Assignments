import numpy as np
from fir-filter import FIR_filter

h = np.array([1/2,1/2,0,0,0])
f = FIR_filter(h)
y= f.dofilter(0)
print(y)
y= f.dofilter(1)
print(y)
for i in range (20):
   y= f.dofilter(0)
   print(y)
