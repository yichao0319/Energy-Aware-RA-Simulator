from scipy import linalg
import numpy
from helper import *
from matplotlib import pylab


def apply_Q_matrix(curr_chan):

    [M,N]=curr_chan.shape
    if M==1: return curr_chan

    if M==2: sm = sm_2_20
    elif M==3: sm = sm_3_20
 
    H = numpy.dot(curr_chan.T,sm).T
    print H
    return H

def calc_snr_map2by1(chan):

    [M,N,S] = chan.shape
    assert M >= 2 , "Channel ntx values cannot be less than calc values"

    curr_chan = chan/numpy.sqrt(2)

    snr={}
    for m in range(0,nchoosek(M,2)):
        for n in range(0,N):
            key='map 2by1 '+str(ant2[m])+str(ant1[n])
            snr[key]=[]
            for num in range(0,S):
                h11=curr_chan[m%2,n,num]
                h12=curr_chan[min(m+1,2),n,num]
                subchan = numpy.array([h11,h12])
                snr[key].append([sum(abs(subchan)**2)])
    return snr

def calc_snr_map2by2(chan):

    [M,N,S] = chan.shape
    assert M >= 2 , "Channel ntx values cannot be less than calc values"
    assert N >= 2 , "Channel nrx values cannot be less than calc values"

    curr_chan = chan/numpy.sqrt(2)

    snr={}
    for m in range(0,nchoosek(M,2)):
        for n in range(0,nchoosek(N,2)):
            key='map 2by2 '+str(ant2[m])+str(ant2[n])
            snr[key]=[]
            for num in range(0,S):
                h11=curr_chan[m%2,n%2,num]
                h12=curr_chan[min(m+1,2),n%2,num]
                h21 = curr_chan[m%2,min(n+1,2),num]
                h22 = curr_chan[min(m+1,2),min(n+1,2),num]
                subchan = numpy.array([[h11,h12],[h21,h22]])
                snr[key].append([sum(sum(abs(subchan)**2))])
    return snr

def calc_snr_map3by1(chan):

     [M,N,S] = chan.shape
     Nfft=64
     delay=numpy.array([0,8,4,2])
     sub=numpy.array([1,2,4,7,9,10,13,15,17,18,19,21,24,26,27,28,36,38,39,41,43,46,47,49,51,53,55,57,60,62])
     phi0 = numpy.exp(-1j*2*numpy.pi*delay[0]*sub/Nfft);
     phi1 = numpy.exp(-1j*2*numpy.pi*delay[1]*sub/Nfft);
     phi2 = numpy.exp(-1j*2*numpy.pi*delay[2]*sub/Nfft);

     curr_chan = chan/numpy.sqrt(db2linear(4.5))
     snr={}
     for n in range(0,N):
         key='map 3by1 '+'G'+str(ant1[n])
         snr[key]=[]
         for num in range(0,S):
             h11 = curr_chan[0,n,num]*phi0[num]
             h12 = curr_chan[1,n,num]*phi1[num]
             h13 = curr_chan[2,n,num]*phi2[num]
             H = (h11+h12+h13)/numpy.sqrt(db2linear(4.5))
             snr[key].append([abs(H)**2])
     return snr

def calc_snr_map3by2(chan):

     [M,N,S] = chan.shape
     assert M is 3 , "Channel ntx values cannot be less than calc values"
     assert N >= 2 , "Channel nrx values cannot be less than calc values"

     curr_chan = chan/numpy.sqrt(db2linear(4.5))

     snr={}
     for n in range(0,nchoosek(N,2)):
         key='map 3by2 '+'G'+str(ant2[n])
         snr[key]=[]

         for num in range(0,S):
             h11 = curr_chan[0,n%2,num];   h21 = curr_chan[0,min(n+1,2),num];
             h12 = curr_chan[1,n%2,num];   h22 = curr_chan[1,min(n+1,2),num];
             h13 = curr_chan[2,n%2,num];   h23 = curr_chan[2,min(n+1,2),num];
    
             H = numpy.array([[h11,h12,h13,0+0j],[h12.conj(),-h11.conj(),0+0j,h13.conj()],\
                        [h21,h22,h23,0+0j],[h22.conj(),-h21.conj(),0+0j,h23.conj()]])
    
             M = linalg.inv(numpy.dot(H.conj().T,H) + numpy.eye(4))
             diagM=numpy.diag(M)
             revvals = numpy.array([diagM[0],diagM[2]])
             mag = 1/revvals -1
             snr[key].append(mag.real)
     return snr



def calc_snr_2by1(chan):

     [M,N,S] = chan.shape
     snr = numpy.zeros((S,1))
     curr_chan = chan/numpy.sqrt(2)
     for num in range(0,S):
         sub_chan = curr_chan[0:2,0,num]
         snr[num] = sum(abs(sub_chan)**2)
     return snr

def calc_snr_2by2(chan):

     [M,N,S] = chan.shape
     snr = numpy.zeros((S,1))
     curr_chan = chan/numpy.sqrt(2)
     for num in range(0,S):
         sub_chan = curr_chan[0:2,0:2,num]
         snr[num] = sum(sum(abs(sub_chan)**2))
     return snr

def calc_snr_3by1(chan):

     [M,N,S] = chan.shape
     Nfft=64
     delay=numpy.array([0,8,4,2])
     sub=numpy.array([1,2,4,7,9,10,13,15,17,18,19,21,24,26,27,28,36,38,39,41,43,46,47,49,51,53,55,57,60,62])
     phi0 = numpy.exp(-1j*2*numpy.pi*delay[0]*sub/Nfft);
     phi1 = numpy.exp(-1j*2*numpy.pi*delay[1]*sub/Nfft);
     phi2 = numpy.exp(-1j*2*numpy.pi*delay[2]*sub/Nfft);

     snr = numpy.zeros((S,1))
     for num in range(0,S):
         h11 = chan[0,0,num]*phi0[num]
         h12 = chan[1,0,num]*phi1[num]
         h13 = chan[2,0,num]*phi2[num]
         H = (h11+h12+h13)/numpy.sqrt(db2linear(4.5))
         snr[num] = abs(H)**2
     return snr


def calc_snr_3by2(chan):

     [M,N,S] = chan.shape
     snr = numpy.zeros((2,S))

     for num in range(0,S):
         h11 = chan[0,0,num];   h21 = chan[0,1,num];
         h12 = chan[1,0,num];   h22 = chan[1,1,num];
         h13 = chan[2,0,num];   h23 = chan[2,1,num];

         H = numpy.array([[h11,h12,h13,0+0j],[h12.conj(),-h11.conj(),0+0j,h13.conj()],\
                    [h21,h22,h23,0+0j],[h22.conj(),-h21.conj(),0+0j,h23.conj()]])

         M = linalg.inv(numpy.dot(H.conj().T,H) + numpy.eye(4))
         diagM=numpy.diag(M)
         revvals = numpy.array([diagM[0],diagM[2]])
         mag = 1/revvals -1
         snr[:,num] = mag.real
     return snr

def calc_snr_map(chan,m,n):

    [M,N,S] = chan.shape

    #assert M is 3, "Only supports Ntx=3 channel" # Support should be added later
    #assert N is 3, "Only supports Nrx=3 channel" # Ditto
    assert m <= M , "Channel ntx values cannot be less than calc values"
    assert n <= M, "Channel nrx values cannot be less than calc values"
     
    #establish scaling
    if m==3: curr_chan = chan/numpy.sqrt(db2linear(4.5))
    if m==2: curr_chan = chan/numpy.sqrt(2)
    if m==1: curr_chan = chan

    smvalsdB= numpy.zeros((S,min(m,n)))
    for num in range(0,S):
        #sub_chan = self.curr_chan[:,:,num]
        sub_chan = apply_Q_matrix(curr_chan[0:m,0:n,num])
        #sub_chan = curr_chan[0:m,:,num]
        #intd_val = numpy.diag(linalg.inv(numpy.dot(sub_chan.conj().T,sub_chan)+numpy.eye(n)))
        intd_val = numpy.diag(linalg.inv(numpy.dot(sub_chan.conj(),sub_chan.T)+numpy.eye(m)))
        smvals=1/intd_val -1
        smvals = (smvals.real)
        print smvals
        #smvalsdB.append(10*numpy.log10(smvals))
        smvalsdB[num]=10*numpy.log10(smvals)
    #for p in range(min(m,n)):
    #    pylab.plot([ s[p] for s in smvalsdB])
    #pylab.show()

    return smvals

