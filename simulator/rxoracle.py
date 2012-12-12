#! /usr/bin/env python
from energy import *
from basera import BaseRA

class RxOracle(BaseRA):

    def __init__(self,card_type,eng_cnst):
        BaseRA.__init__(self,card_type,eng_cnst)
        self.name = 'RxOracle'


    def select_rate(self,pkt):
        self.extract_relevant_info(pkt)
        mode = pkt.Mode
        mcs = pkt.MCS
        ntx = self.get_ntx_from_key(mode)
        nss = self.get_nss_from_key(mode)
        nrx = self.get_nrx_from_key(mode)
        per = 0.0 # per is no longer used by energy
        card_energy = self.card_type+'_'+self.econstraint+'_energy'
        energyfnc = eval(card_energy)
        if self.econstraint == 'tx': nant = ntx
        elif self.econstraint == 'rx': nant = nrx
        else: assert 0 ,'invalid energy constraint selection'
        eng = energyfnc(nant,nss,self.plen,mcs,per)
        #eng = rx_energy(nrx,nss,self.plen,mcs,per)
        succ = pkt.succ
 
        trace = {'mcs':mcs,'mode':mode,'succ':succ,'energy':eng}
#        print trace
        return {'mcs':0, 'mode':'sm 1by1 AA'}
