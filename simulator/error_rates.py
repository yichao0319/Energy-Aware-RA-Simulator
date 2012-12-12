#! /usr/bin/env python

from scipy.special import erfc,erfcinv,erf
from numpy import sqrt,log2
import math
#from wins.digital.rcpc import RCPC
from helper import mcs2rate
import ast
import time

def Q(x): return 0.5*erfc(x/sqrt(2))

    
def calc_qam_ber(snr,M):
    gamma=1.0
    ter = [2.0*(1 - 1/sqrt(M))*Q(sqrt(3*s/(M-1))) for s in snr]
    ser = [1 - (1-t)**2.0 for t in ter]
    ber = [s/log2(M) for s in ser]
    return ber

def calc_exact_ber_BPSK(snr): return [Q(sqrt(2*s)) for s in snr]
def calc_exact_ber_QPSK(snr): return calc_qam_ber(snr,4)
def calc_exact_ber_QAM16(snr): return calc_qam_ber(snr,16)
def calc_exact_ber_QAM64(snr): return calc_qam_ber(snr,64)

#def calc_ber_BPSK(snr): return [Q(sqrt(2*snr))]
#def calc_ber_QPSK(snr): return [Q(sqrt(snr))]
#def calc_ber_QAM16(snr): return [(3.0/4)*Q(sqrt(s/5)) for s in snr]
#def calc_ber_QAM64(snr): return [(7.0/12)*Q(sqrt(s/21)) for s in snr]

def calc_ber_BPSK(snr): return [Q(sqrt(2*s)) for s in snr]
def calc_ber_QPSK(snr): return [Q(sqrt(s)) for s in snr]
def calc_ber_QAM16(snr): return [(3.0/4)*Q(sqrt(s/5)) for s in snr]
def calc_ber_QAM64(snr): return [(7.0/12)*Q(sqrt(s/21)) for s in snr]


def calc_effber_BPSK(snr): return [Q(sqrt(2*s)) for s in snr]
def calc_effber_QPSK(snr): return [Q(sqrt(s)) for s in snr]
def calc_effber_QAM16(snr): return [(3.0/4)*Q(sqrt(s/5)) for s in snr]
def calc_effber_QAM64(snr): return [(7.0/12)*Q(sqrt(s/21)) for s in snr]



Check=0
PreComputedPER={}
def read_precomputed_per():

    global PerComputedPER

    file = open("simulator/perdata.dat")
    data=[]
    for line in file:
        data.append(ast.literal_eval(line))

    for line in data: 
        for mcs in range(0,8):
            PreComputedPER["MCS%d"%mcs]=line["MCS%d"%mcs]
    file.close()

def calc_per(plen,mcs,ber):

    global Check
    global PreComputedPER

    if Check == 0:
       read_tic = time.clock()
       read_precomputed_per()
       read_toc = time.clock()
       print "reading time: "+str(read_toc - read_tic)
       Check=1

    perdata=PreComputedPER["MCS%d"%mcs]

    assert perdata != [], "PER values not correctly read from file"

    highest_ber=perdata[0][0]
    lowest_ber=perdata[-1][0]

    if ber > highest_ber: return perdata[0][1]
    if ber <= lowest_ber: return 0.0

    for p in perdata:
       if ber > p[0]:
          per = p[1]
          break
           
    return per


def old_calc_per(plen,mcs,ber):

    #psearch_tic = time.clock()*1e6
    global Check
    global PreComputedPER

    if Check == 0:
       read_tic = time.clock()
       read_precomputed_per()
       read_toc = time.clock()
       print "reading time: "+str(read_toc - read_tic)
       Check=1

    perdata=PreComputedPER["MCS%d"%mcs]

    assert perdata != [], "PER values not correctly read from file"

    tmp=[p for p in perdata if ber>p[0]]
    if tmp==[]: per = 0.0
    else: per = tmp[0][1]

    #psearch_toc = time.clock()*1e6
    #print "per search time: "+str(psearch_toc - psearch_tic)
    return per


#def oldcalc_per(plen,mcs,ber):
#    vit_dec = RCPC()
#    vit_dec.rate = mcs2rate(mcs)
#    per = vit_dec.per(plen,ber)
#    return per

def main():

    snr=range(3,30)
    Mod=['BPSK','QPSK'] 
    tmp= 'calc_ber_'+Mod[1]
    ber= eval(tmp)(snr)
    print ber

if __name__=="__main__":
   main()
