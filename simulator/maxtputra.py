#! /usr/bin/env python

from numpy import average
from basera import BaseRA
from helper import *
from error_rates import *
from energy import *
import time

class MaxTputRA(BaseRA):

    def __init__(self,card_type,eng_cnst,predon=False):
        BaseRA.__init__(self,card_type,eng_cnst,predon)
        self.tput=None
        #self.file = open('Trace/max_tput_trace.dat','w')
        self.name = 'MaxTput'


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

    def select_rate(self,pkt):
        self.extract_relevant_info(pkt)
        snr_tic = time.clock() 
        self.calc_snrs()
        snr_toc = time.clock() 
        ber_tic = time.clock() 
        self.calc_bers()
        ber_toc = time.clock() 
        per_tic = time.clock() 
        self.calc_pers()
        per_toc = time.clock() 
        tput_tic = time.clock() 
        self.calc_tput()
        tput_toc = time.clock() 

        print "time-> snr:"+str(snr_toc-snr_tic)+" ber:"+str(ber_toc-ber_tic)+" per:"+str(per_toc - per_tic)+" tput:"+str(tput_toc - tput_tic)

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
        elif self.econstraint == 'tx_rx': nant = (ntx,nrx)
        else: assert 0 ,'invalid energy constraint selection'
        eng = energyfnc(nant,nss,self.plen,mcs,self.per[mode][mcs])
        #eng = rx_energy(nrx,nss,self.plen,mcs,self.per[mode][mcs])

        trace = {'mcs':mcs,'mode':mode,'tput':maxtput,'energy':eng,'succ':pkt.succ}
        print trace
        #self.file.write(str(trace)+str('\n'))

        return {'mcs':mcs,'mode':mode}
