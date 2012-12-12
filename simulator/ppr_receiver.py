#! /usr/bin/env python

from numpy import *
from helper import *
from rxvector import Rxvector
from error_rates import *
from spatialmux import *
from spatialmap import *
from feedback import Feedback

# PPR receiver differs from standard receiver in that it does not
# calculate PER and does not establish if the packet was received
# correctly or not.
# Approximations:
# PPR should have re-txs. Since they are not supported by the 
# simulator, the receiver will simply calculated the ber.
# It is more of a place holder for future support. The PPR rate
# selection code will calculate all snr and ber and analytically 
# establish the number of re-txs needed for a given rate and overall
# tput. On the basis of the calculations, it will select the next rate.


class PPrReceiver:

    rx_pkt = None
    NOISE_FIGURE = 10.0

    def __init__(self,ra=None,nrx=1,extname=""):
        self.ra = ra
        self.rxv = Rxvector()
        self.mode = None  # SM, STBC
        self.npow = None
        self.nrx = nrx
        self.succ = None
        self.mode = None
        self.mcs = None
        self.pkt_count = 0
        self.file = open('Trace/'+self.ra.name+'_'+str(extname)+'.dat','w')

    def calc_snr(self,pkt):
        # calculate snr

        mode =pkt.Mode.split()
        snr_fnc=eval("calc_snr_"+mode[0]+mode[1])
        ppsnr = snr_fnc(pkt.ChanMag)

        if ppsnr==[]:
           print "snr not computed correctly"

        return ppsnr[pkt.Mode]

    def receive_pkt(self,pkt):
        self.pkt_count = self.pkt_count + 1
        self.update_rxvector(pkt)
        self.nrx = pkt.Mode.split()[1][-1] # pkt Nrx is based on mode

        # FIXME:
        # The pkt.Nrx should based of pkt.Mode not nrx
        # If pkt.Nrx > self.nrx, reception should fail
        # but for lack of time lets go with it
        pkt.Nrx = int(self.nrx) # almost a hack

        ppsnr= self.calc_snr(pkt)
        #print "SNR: "+str(ppsnr)
        pkt.Noise = self.npow
        data_delivered = self.decode(pkt,ppsnr)
        pkt.succ = -1
        trace = {'mcs':pkt.MCS,'mode':pkt.Mode,'data': data_delivered}
        print "Receiver: "+str(trace)
        self.file.write(str(trace)+str('\n'))
        self.select_next_rate(pkt)
        
    def calc_data_received(self,ber):

        n = get_retx_count(ber) # re-tx count is dependant on ber
        data_delivered = self.rxv.length*(1.0 - ber**n)
        return data_delivered

    def decode(self,pkt,ppsnr):
        #Calculate ber and per
        ber_fnc = eval("calc_ber_"+mcs2mod(self.rxv.MCS))
        #[S, Nss] = ppsnr.shape
        ber = [ber_fnc(snum) for snum in ppsnr]
        avg_ber = average([average(berm) for berm in ber])
        data_delivered = self.calc_data_received(avg_ber)
        return data_delivered 

    def update_rxvector(self,pkt): 
        self.rxv.BW = pkt.CBW
        self.rxv.MCS = pkt.MCS
        self.rxv.STBC = pkt.STBC
        self.rxv.length = pkt.length
        self.rxv.Mode = pkt.Mode
        
    def select_next_rate(self,pkt):
        rate_selected = self.ra.select_rate(pkt)
        self.mode = rate_selected['mode']
        self.mcs = rate_selected['mcs']

        #if self.pkt_count%10 == 0 and self.mode!='sm 3by 3 GG':
        #    print 'Test pkt called'
        #    self.mode = 'sm 3by3 GG'
        #    self.mcs = 0

    def get_feedback_pkt(self):

        fd_pkt = Feedback()
        fd_pkt.mode = self.mode
        fd_pkt.mcs = self.mcs
        fd_pkt.succ = self.succ
        fd_pkt.plen = self.rxv.length
        return fd_pkt

