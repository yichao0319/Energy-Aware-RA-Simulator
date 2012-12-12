#! /usr/bin/env python

from numpy import average
from basera import BaseRA
from helper import *
from error_rates import *
from energy import *


class OracleRA(BaseRA):

    def __init__(self,card_type,eng_cnst,chan):
        BaseRA.__init__(self,card_type,eng_cnst)
        assert chan != None, "Oracle must have channel ref at time of instantiation"
        self.chan = chan
        self.name = 'Oracle'

    def set_relevant_info(self,pkt):
        self.chanmag = self.chan.peek_next_channel()
        self.plen = pkt.length

    def calc_tput(self):

        self.tput={}
        keys = self.per.keys()
        Nsub = 52
        for key in keys:
            tput_val=[]
            Nss = self.get_nss_from_key(key)
            for mcs in range(0,8):
                BpS = Nsub*mcs2nbpsc(mcs)*Nss/8.0
                num_ofdm_sym = 1.0*self.plen/BpS
                tput_val.append(8*self.plen*(1.0-self.per[key][mcs])/(num_ofdm_sym*4.0))
            self.tput[key] =tput_val
        #print self.tput

    def process_feedback(self,ack_pkt):
        ack = ack_pkt # just a redundant statement for completeness

    def select_rate(self,pkt):
        self.set_relevant_info(pkt)
        self.calc_snrs()
        self.calc_bers()
        self.calc_pers()
        self.calc_tput()

        keys = self.tput.keys()
        mcs=0
        maxtput=0
        mode=None
        for key in keys:
            tput = max(self.tput[key])
            tmpmcs = self.tput[key].index(tput)
            if tput > maxtput:
               maxtput =tput
               mcs = tmpmcs
               mode = key

        ntx = self.get_ntx_from_key(mode)
        nss = self.get_nss_from_key(mode)
        nrx = self.get_nrx_from_key(mode)
        card_energy = self.card_type+'_'+self.econstraint+'_energy'
        energyfnc = eval(card_energy)
        if self.econstraint == 'tx': nant = ntx
        elif self.econstraint == 'rx': nant = nrx
        else: assert 0 ,'invalid energy constraint selection'
        eng = energyfnc(nant,nss,self.plen,mcs,self.per[mode][mcs])

        #eng = rx_energy(nrx,nss,self.plen,mcs,self.per[mode][mcs])

        trace = {'mcs':mcs,'mode':mode,'tput':maxtput,'energy':eng}
        print trace
        #self.file.write(str(trace)+str('\n'))

        return [mcs,mode]
