#! /usr/bin/env python

from scipy.special import erf, erfc
from math import sqrt,pi
import time
from scipy import special

def Q(x): return 0.5*erfc(x/sqrt(2))

class Qinverse:

    def __init__(self,limit=1000):
        self.limit = limit
        self.c = self.calc_c()

    def erfcinv(self,x): return self.erfinv(1-x)
    #def Qinv(self,x): return sqrt(2)*self.erfcinv(2*x)
    def Qinv(self,x): return sqrt(2)*special.erfcinv(2*x)
 
    def erfinv(self,z):
        c = self.c
        ans = 0
        for k in range(0,self.limit):
            ans = ans + (c[k]/(2*k+1))*(sqrt(pi)*z/2)**(2*k+1)
        return ans
    
    def calc_c(self):
        c=[1.0]
    
        for k in range(1,self.limit):
            tmp_c=0
            for m in range(0,k):
                tmp_c = tmp_c + (c[m]*c[k-1-m]/((m+1.0)*(2.0*m+1)))
            c.append(tmp_c)
        return c

def main():

    q = Qinverse()

    #c=q.calc_c()

    tic = time.clock()
    for t in range(0,10):
        print q.Qinv(1.0e-5*t +  1.0e-6)
    toc = time.clock()
    print "time: "+str(toc - tic)
    #s=[0.1*a for a in range(0,10)]
    #shat = [q.erfinv(erf(x)) for x in s]
    #print [(a,b) for a,b in zip(s,shat)]

if __name__=="__main__":
   main()
