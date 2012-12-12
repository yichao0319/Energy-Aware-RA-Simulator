#! /usr/bin/env python

from numpy import average
from basera import BaseRA
from helper import *
from error_rates import *
from energy import *


class OracleMinEngRA(BaseRA):

    def __init__(self,card_type,eng_cnst,chan):
        BaseRA.__init__(self,card_type,eng_cnst)
        assert chan != None, "Oracle must have channel ref at time of instantiation"
        self.chan = chan
        self.name = 'OracleMinEng'

    def set_relevant_info(self,pkt):
        self.chanmag = self.chan.peek_next_channel()
        self.plen = pkt.length

    def calc_energy(self):
        self.est_energy={} 
        keys = self.per.keys()

        for key in keys: 
            ntx = self.get_ntx_from_key(key)
            nss = self.get_nss_from_key(key)
            plen = self.plen
            nrx = self.get_nrx_from_key(key)
            card_energy = self.card_type+'_'+self.econstraint+'_energy'
            energyfnc = eval(card_energy)
            if self.econstraint == 'tx': nant = ntx
            elif self.econstraint == 'rx': nant = nrx
            else: assert 0 ,'invalid energy constraint selection'
            self.est_energy[key] = [energyfnc(nant,nss,plen,mcs,0.0) for mcs in range(0,8)]


    def calc_tput(self,key,mcs):

        Nsub = 52
        Nss = self.get_nss_from_key(key)
        BpS = Nsub*mcs2nbpsc(mcs)*Nss/8.0
        num_ofdm_sym = 1.0*self.plen/BpS
        tput = 8*self.plen*(1.0)/(num_ofdm_sym*4.0)
        return tput


    def process_feedback(self,ack_pkt):
        ack = ack_pkt # just a redundant statement for completeness

    def select_rate(self,pkt):
        self.set_relevant_info(pkt)
        self.calc_snrs()
        self.calc_bers()
        self.calc_pers()
        self.calc_energy()

        keys = self.est_energy.keys()
        mineng = 1.0e6
        minmcs = -1
        minmode = 0
        for key in keys:
            for mcs in range(0,8):
                eng = self.est_energy[key][mcs]
                if (eng < mineng) and (self.per[key][mcs] < 0.1): # PER constrained at 0.1
                    mineng = eng
                    minmcs = mcs
                    minmode = key


        tput = self.calc_tput(minmode,minmcs)

        trace = {'mcs':minmcs,'mode':minmode,'tput':tput,'energy':mineng}
        print trace
        #self.file.write(str(trace)+str('\n'))

        return {'mcs':minmcs,'mode':minmode}
