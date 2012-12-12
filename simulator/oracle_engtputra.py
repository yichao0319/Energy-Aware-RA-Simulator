#! /usr/bin/env python

from numpy import average
from basera import BaseRA
from helper import *
from error_rates import *
from energy import *


class OracleEngTputRA(BaseRA):

    def __init__(self,card_type,eng_cnst,chan,threshold):
        BaseRA.__init__(self,card_type,eng_cnst)
        assert chan != None, "Oracle must have channel ref at time of instantiation"
        self.chan = chan
        self.tput= None
        self.threshold = threshold
        self.name = 'OracleEngTput'

    def set_relevant_info(self,pkt):
        self.chanmag = self.chan.peek_next_channel()
        self.plen = pkt.length

    def calc_energy(self):
        self.est_energy={} 
        keys = self.per.keys()

        for key in keys: 
            ntx = self.get_ntx_from_key(key)
            nss = self.get_nss_from_key(key)
            nrx = self.get_nrx_from_key(key)
            plen = self.plen
            card_energy = self.card_type+'_'+self.econstraint+'_energy'
            energyfnc = eval(card_energy)
            if self.econstraint == 'tx': nant = ntx
            elif self.econstraint == 'rx': nant = nrx
            else: assert 0 ,'invalid energy constraint selection'
            self.est_energy[key] = [energyfnc(nant,nss,plen,mcs,0.0) for mcs in range(0,8)]

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
            self.tput[key] = tput_val
            #print "key: "+str(key)+" -> "+str(self.tput[key])

    def find_max_tput(self):

        keys = self.per.keys()

        maxtput=0.0
        maxtput_mcs = -1
        maxtput_key = None
        for key in keys:
            val = max(self.tput[key])
            if val > maxtput:
               maxtput = val
               maxtput_mcs = self.tput[key].index(val)
               maxtput_key = key

        return {'tput': maxtput, 'key':maxtput_key, 'mcs':maxtput_mcs} 

    def search_rate(self,maxtput_info):

        tput_th = self.threshold*maxtput_info['tput']

        keys = self.per.keys()

        min_eng_mcs = maxtput_info['mcs']
        min_eng_key = maxtput_info['key']
        min_energy = self.est_energy[min_eng_key][min_eng_mcs]
        sel_tput = maxtput_info['tput']
        for key in keys:
            for mcs in range(0,8):
                if (self.tput[key][mcs] >= tput_th) and (self.est_energy[key][mcs] < min_energy) and (self.per[key][mcs] < 0.1):
                    sel_tput = self.tput[key][mcs]
                    min_energy = self.est_energy[key][mcs]
                    min_eng_mcs = mcs
                    min_eng_key = key

        return {'eng':min_energy, 'mcs':min_eng_mcs, 'key':min_eng_key, 'tput':sel_tput}


    def process_feedback(self,ack_pkt):
        ack = ack_pkt # just a redundant statement for completeness

    def select_rate(self,pkt):
        self.set_relevant_info(pkt)
        self.calc_snrs()
        self.calc_bers()
        self.calc_pers()
        self.calc_energy()
        self.calc_tput()

        maxtput_info = self.find_max_tput()
        #min_energy = self.find_min_energy()
        #print maxtput_info
        rate_sel = self.search_rate(maxtput_info)
        #print rate_sel 

        trace = {'mcs':rate_sel['mcs'],'mode':rate_sel['key'],'tput':rate_sel['tput'],'energy':rate_sel['eng']}
        print trace
        #self.file.write(str(trace)+str('\n'))

        mode = rate_sel['key']
        mcs = rate_sel['mcs']
        return {'mcs':mcs,'mode':mode}
