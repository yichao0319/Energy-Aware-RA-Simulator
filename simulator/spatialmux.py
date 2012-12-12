from scipy import linalg
import numpy
from helper import *
from matplotlib import pylab


def calc_snr_sm1by1(chan):

    [M,N,S] = chan.shape
    snr={}
    for m in range(0,M):
        for n in range(0,N):
            key='sm 1by1 '+str(ant1[m])+str(ant1[n])
            snr[key]=[]
            for num in range(0,S):
                subchan = chan[m,n,num]
                snr[key].append([abs(subchan)**2])
    return snr

def calc_snr_sm1by2(chan):

    [M,N,S] = chan.shape
    assert N >= 2 , "Channel nrx values cannot be less than calc values"

    snr={}
    for m in range(0,M):
        for n in range(0,nchoosek(N,2)):
            key='sm 1by2 '+str(ant1[m])+str(ant2[n])
            snr[key]=[]
            for num in range(0,S):
                h11=chan[m,n%2,num]
                h21=chan[m,min(n+1,2),num]
                subchan = numpy.array([h11,h21])
                snr[key].append([sum(abs(subchan)**2)])
    return snr

def calc_snr_sm1by3(chan):

    [M,N,S] = chan.shape
    snr={}
    for m in range(0,M):
        key='sm 1by3 '+str(ant1[m])+'G'
        snr[key]=[]
        for num in range(0,S):
            subchan = chan[m,:,num]
            snr[key].append([sum(abs(subchan)**2)])
    return snr

def calc_snr_sm2by2(chan):

    [M,N,S] = chan.shape
    assert M >= 2 , "Channel ntx values cannot be less than calc values"
    assert N >= 2 , "Channel nrx values cannot be less than calc values"

    curr_chan = chan/numpy.sqrt(2)
    snr={}
    for m in range(0,nchoosek(M,2)):
        for n in range(0,nchoosek(N,2)):
            key='sm 2by2 '+str(ant2[m])+str(ant2[n])
            snr[key]=[]
            for num in range(0,S):
                h11 = curr_chan[m%2,n%2,num]
                h12 = curr_chan[min(m+1,2),n%2,num]
                h21 = curr_chan[m%2,min(n+1,2),num]
                h22 = curr_chan[min(m+1,2),min(n+1,2),num]
                sub_chan = numpy.array([[h11,h12],[h21,h22]])
                intd_val = numpy.diag(linalg.inv(numpy.dot(sub_chan.conj().T,sub_chan)+numpy.eye(2)))
                smvals=1/intd_val -1
                smvals = (smvals.real)
                snr[key].append(smvals)
    return snr

def calc_snr_sm2by3(chan):

    [M,N,S] = chan.shape
    assert M >= 2 , "Channel ntx values cannot be less than calc values"
    assert N is 3 , "Channel nrx values cannot be less than calc values"

    curr_chan = chan/numpy.sqrt(2)
    snr={}
    for m in range(0,nchoosek(M,2)):
        key='sm 2by3 '+str(ant2[m])+'G'
        snr[key]=[]
        for num in range(0,S):
            h1 = curr_chan[m%2,:,num]
            h2 = curr_chan[min(m+1,2),:,num]
            sub_chan = numpy.array([h1,h2])
            intd_val = numpy.diag(linalg.inv(numpy.dot(sub_chan.conj(),sub_chan.T)+numpy.eye(2)))
            smvals=1/intd_val -1
            smvals = (smvals.real)
            snr[key].append(smvals)
    return snr


def calc_snr_sm3by3(chan):

    [M,N,S] = chan.shape

    assert M is 3 , "Channel ntx values cannot be less than calc values"
    assert N is 3, "Channel nrx values cannot be less than calc values"
     
    #establish scaling
    curr_chan = chan/numpy.sqrt(db2linear(4.5))

    smvalsdB= numpy.zeros((S,3))
    #snr = numpy.zeros((S,3))
    snr={}
    key='sm 3by3 '+'GG'
    snr[key]=[]
    for num in range(0,S):
        sub_chan = curr_chan[0:3,0:3,num] # 0:3 picks 0,1,2
        intd_val = numpy.diag(linalg.inv(numpy.dot(sub_chan.conj(),sub_chan.T)+numpy.eye(3)))
        smvals=1/intd_val -1
        smvals = (smvals.real)
        #smvalsdB.append(10*numpy.log10(smvals))
        smvalsdB[num]=10*numpy.log10(smvals)
        snr[key].append(smvals)
    #for p in range(min(m,n)):
    #    pylab.plot([ s[p] for s in smvalsdB])
    #pylab.show()

    return snr



def old_calc_snr_sm(chan,m,n):

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
    snr = numpy.zeros((S,min(m,n)))
    for num in range(0,S):
        #sub_chan = self.curr_chan[:,:,num]
        sub_chan = curr_chan[0:m,0:n,num]
        #sub_chan = curr_chan[0:m,:,num]
        #intd_val = numpy.diag(linalg.inv(numpy.dot(sub_chan.conj().T,sub_chan)+numpy.eye(n)))
        intd_val = numpy.diag(linalg.inv(numpy.dot(sub_chan.conj(),sub_chan.T)+numpy.eye(min(m,n))))
        smvals=1/intd_val -1
        smvals = (smvals.real)
        #smvalsdB.append(10*numpy.log10(smvals))
        smvalsdB[num]=10*numpy.log10(smvals)
        snr[num] = smvals
    #for p in range(min(m,n)):
    #    pylab.plot([ s[p] for s in smvalsdB])
    #pylab.show()

    return snr

