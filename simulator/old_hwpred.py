#! /usr/bin/env python

import numpy
from trace_chan import TraceChan

# This is the old holts winter prediction.
# This file was never used in evaluation.
# The correctness is also suspect.
# It has been replaced by Yi-Chao's prediciton implementation.

class HoltsWinter:

    def __init__(self):
        self.a_prev = None
        self.b_prev = None
        self.alpha = 0.2
        self.beta = 0.1

    def setup_a(self,y): self.a_prev = y;
    def setup_b(self,y): self.b_prev = numpy.zeros((y.shape))


#    def modget_next_pred(self,chan):
#
#        assert self.a_prev_real != None, "setup_a(chan) method not called"
#        assert self.b_prev_real != None, "setup_b(chan) method not called"
#
#        [M,N,S] = chan.shape
#        y_pred = numpy.zeros((M,N,S))*1j
#        for num in range(0,S):
#            for rows in range(0,M):
#                for cols in range(0,N):
#                    ap_real = self.a_prev_real[rows,cols,num]
#                    bp_real = self.b_prev_real[rows,cols,num]
#                    ap_imag = self.a_prev_imag[rows,cols,num]
#                    bp_imag = self.b_prev_imag[rows,cols,num]
#
#                    a_real = self.alpha*chan[rows,cols,num].real + (1 - self.alpha)*(ap_real + bp_real)
#                    a_imag = self.alpha*chan[rows,cols,num].imag + (1 - self.alpha)*(ap_imag + bp_imag)
#                    b_real = self.beta*(a_real - ap_real) + (1 - self.beta)*bp_real
#                    b_imag = self.beta*(a_imag - ap_imag) + (1 - self.beta)*bp_imag
#
#                    y_real = a_real+b_real
#                    y_imag = a_imag+b_imag
#                    y_pred[rows,cols,num] = complex(y_real,y_imag)
#                    self.a_prev_real[rows,cols,num] = a_real
#                    self.b_prev_real[rows,cols,num] = b_real
#                    self.a_prev_imag[rows,cols,num] = a_imag
#                    self.b_prev_imag[rows,cols,num] = b_imag
# 
#        return y_pred

    def get_next_pred(self,chan):

        assert self.a_prev != None, "setup_a(chan) method not called"
        assert self.b_prev != None, "setup_b(chan) method not called"

        [M,N,S] = chan.shape
        y_pred = numpy.zeros((M,N,S))*1j

        for num in range(0,S):
            for rows in range(0,M):
                for cols in range(0,N):
                    ap = self.a_prev[rows,cols,num]
                    bp = self.b_prev[rows,cols,num]

                    a = self.alpha*chan[rows,cols,num] + (1 - self.alpha)*(ap + bp)
                    b = self.beta*(a - ap) + (1 - self.beta)*bp

                    y_pred[rows,cols,num] = a+b
                    self.a_prev[rows,cols,num] = a
                    self.b_prev[rows,cols,num] = b
 
        return y_pred



def main():
 
    hwpred = HoltsWinter()
    chan = TraceChan()
    chan_len = chan.create_chan(3,3)

    chan.get_next_channel()
    Hint = chan.curr_chan
    hwpred.setup_a(Hint)
    hwpred.setup_b(Hint)

    Hpred = Hint
    Hprev = Hint
    for c in range(0,100):
        H = chan.curr_chan
        print "pred:"+str(sum(sum(sum(abs(Hpred - H)))))
        print "diff:"+str(sum(sum(sum(abs(Hprev - H)))))
        Hpred = hwpred.get_next_pred(H)
        Hprev = H
        chan.get_next_channel()
    

if __name__ == "__main__":
   main()
