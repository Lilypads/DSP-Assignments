'''
import numpy as np
# Inefficient way
class FIR_filter:
    def __init__(self,coefficients):
        self.coeff = coefficients
        self.offset = 0
        self.buffer = np.empty(len(coefficients))
        
    def dofilter(self,u):
        result = 0
        for i in range(len(self.buffer)-1,0,1): #range(start,end,step)
            self.buffer[i+1] = self.buffer[i]
        self.buffer[0] = u
        for i in range(len(self.buffer)-1):
            result = result + self.coeff[i] * self.buffer[i]
        return result
     
'''
import numpy as np
class FIR_filter:
    def __init__(self,coefficients):
        self.coeff = coefficients
        self.offset = 0
        #self.coeffIndex = 0
        self.buffer = np.zeros(len(coefficients))
        
    def dofilter(self,u):
        result = 0
        self.buffer[self.offset] = u
        #print("offset index:",self.offset)
        
        for i in range(self.offset+1):
            result = result + self.buffer[i]*self.coeff[self.offset-i]
            #print("buffer index:",i) 
            #print("coeff index:",self.offset-i)
       
        for i in range(self.offset+1,len(self.buffer),1):
            result = result + self.buffer[i]*self.coeff[len(self.buffer)-1+self.offset+1-i]
            #print("buffer index:",i) 
            #print("coeff index:",len(self.buffer)-1+self.offset+1-i)
            
        self.offset+=1
        if self.offset>=len(self.buffer):
            self.offset=0
        
        return result
    
def unittest():
        h = np.array([1/2,1/2,0,0,0])
        f = FIR_filter(h)
        y= f.dofilter(0)
        print(y)
        y= f.dofilter(1)
        print(y)
        for i in range (20):
            y= f.dofilter(0)
            print(y)

if __name__ == "__main__":
    unittest()