#! /usr/bin/env python

from scipy.misc import factorial
import numpy
from numpy import pi

def linear2db(xlinear):
    """Convert a linear value to decibels.

    :param xlinear: Value(s) in linear scale.

    :returns: 10*log10(`xlinear`)
    """
    yval = []
    xval = xlinear
    isiter = hasattr(xlinear, '__iter__')
    if not isiter: xval = [xlinear]
    for x in xval:
        if   (x>0): y = 10*numpy.log10(x)
        elif (x<0): y = numpy.nan
        else: y = -numpy.inf
        yval.append(y)
    y = numpy.array(yval)
    if not isiter: y = yval[0]
    return y

def db2linear(xdb):
    """Convert a decibel value to a linear scale.

    :param xdb: Value(s) in decibels.

    :returns: 10^(`xdb`/10)
    """
    return 10.0**(xdb/10.0)

def nchoosek(n,k): return int(factorial(n)/(factorial(k)*factorial(n-k)))


ant1=['A','B','C'] # A=ant1, B=ant2, C=ant3
ant2=['D','E','F'] # D=ants1,2, E=ants2,3, F=ants1,3



MODULATION=['BPSK','QPSK','QPSK','QAM16','QAM16','QAM64','QAM64','QAM64']
CODERATE=['1/2','1/2','3/4','1/2','3/4','2/3','3/4','5/6']
NBPSC= [0.5, 1, 1.5, 2, 3, 4, 4.5, 5]


def mcs2mod(mcs): return MODULATION[mcs%8]
def mcs2rate(mcs): return CODERATE[mcs%8]
def mcs2nbpsc(mcs): return NBPSC[mcs%8]

def get_retx_count(ber):

    if ber < 1.0e-4: n=1
    elif ber < 1.0e-3: n=2
    elif ber < 1.0e-2: n=3
    elif ber < 0.1: n=4
    else: n = 5

    # FIXME: Just a hack to see how it performs
    n = 1
    return n

def str2val(str):
    ppstr = str.replace(" ",",")
    return eval(ppstr)


sm_1 = 1;

sm_2_20 = numpy.array([[1,1],[1,-1]])/numpy.sqrt(2);

sm_3_20 =numpy.array([[-2*pi/16 ,    -2*pi/(80/33),  2*pi/(80/3)], [2*pi/(80/23),  2*pi/(48/13),  2*pi/(240/13)], [-2*pi/(80/13), 2*pi/(240/37), 2*pi/(48/13)]])
sm_3_20 = numpy.exp(1)**(1j*sm_3_20)/ numpy.sqrt(3)

