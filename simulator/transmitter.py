#! /usr/bin/env python

from txvector import Txvector
from packet import Packet
from sampleratera import SampleRate


class Transmitter:

    def __init__(self,ntx,ta=None):
        self.Ntx = ntx
        self.txv = Txvector() 
        self.initialize_txv(ntx)
        self.ta = ta

    def set_transmit_ra(self,ta): self.ta = ta

    def initialize_txv(self,ntx):
        self.txv.Ntx = ntx
        self.txv.MCS = 7
        self.txv.Mode = 'sm 3by3 GG'
        self.txv.length = 1000
        self.txv.STBC = 0
        self.txv.Nsts = ntx
        self.txv.BW = 20e6 # can be 20 and 40Mhz

    def update_txv(self,ack_pkt):

        self.txv.MCS = ack_pkt.mcs
        self.txv.Mode = ack_pkt.mode
        mode = ack_pkt.mode.split()
        ntxbynrx = mode[1]
        self.txv.Ntx = int(ntxbynrx[0])

        #self.txv.Ntx = int(ack_pkt.mode[len(ack_pkt.mode)-4])

    def transmit_pkt(self):
        pkt = Packet()

        pkt.TxPwr = 16.02 #dBm
        pkt.length = self.txv.length
        pkt.CBW = self.txv.BW
        pkt.STBC = self.txv.STBC

        if self.ta is None:
           pkt.MCS = self.txv.MCS
           pkt.Ntx = self.txv.Ntx
           pkt.Mode = self.txv.Mode
        else:
           selected_rate = self.ta.select_rate(pkt)
           pkt.MCS = selected_rate['mcs']
           pkt.Mode = selected_rate['mode']
           mode = pkt.Mode.split()
           ntxbynrx = mode[1]
           pkt.Ntx = int(ntxbynrx[0])
        return pkt

    def process_ack(self,ack_pkt):

        if self.ta is None:
           self.update_txv(ack_pkt)
        else:
           self.ta.process_feedback(ack_pkt)

def main():
    txv= Txvector()
    tx = Transmitter(txv)

if __name__=="__main__":
   main()
