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
        self.buffer = np.zeros(len(coefficients))
        
    def dofilter(self,u):
        result = 0
        self.buffer[self.offset] = u
        #print("offset index:",self.offset)
        
        for i in range(self.offset+1):
            result = result + self.buffer[i]*self.coeff[self.offset-i]
            #print("buffer index:",i) 
            #print("coeff index:",self.offset-i)
       
        #print("Second For Section")
        for i in range(self.offset+1,len(self.buffer),1):
            result = result + self.buffer[i]*self.coeff[len(self.buffer)-1+self.offset+1-i]
            #print("buffer index:",i) 
            #print("coeff index:",len(self.buffer)-1+self.offset+1-i)
            
        self.offset+=1
        if self.offset>=len(self.buffer):
            self.offset=0
        
        return result
    
    def dofilterPrint(self,u):      #index printing version for diagnosis purpose
        result = 0
        self.buffer[self.offset] = u
        print("offset index:",self.offset)
        
        for i in range(self.offset+1):
            result = result + self.buffer[i]*self.coeff[self.offset-i]
            print("buffer index:",i) 
            print("coeff index:",self.offset-i)
       
        print("Second For Section")
        for i in range(self.offset+1,len(self.buffer),1):
            result = result + self.buffer[i]*self.coeff[len(self.buffer)-1+self.offset+1-i]
            print("buffer index:",i) 
            print("coeff index:",len(self.buffer)-1+self.offset+1-i)
            
        self.offset+=1
        if self.offset>=len(self.buffer):
            self.offset=0
        
        return result
    
def unittest():
        h = np.array([1/2,1/2,0,0,0])
        print("Coefficient:",h)
        f = FIR_filter(h)
        y= f.dofilterPrint(0)       #use the index printing version 
        print("Input 0, Output",y)
        y= f.dofilterPrint(1)       #use the index printing version 
        print("Input 1, Output",y)
        for i in range (20):
            y= f.dofilterPrint(0)   #use the index printing version 
            print("Input 0, Output",y)

if __name__ == "__main__":
    unittest()