#! /usr/bin/env python

from numpy import average
from basera import BaseRA
from helper import *
from error_rates import *
from energy import *
import time

class PPrEngTputRA(BaseRA):

    def __init__(self,card_type,eng_cnst,predon,threshold):
        BaseRA.__init__(self,card_type,eng_cnst,predon)
        self.tput=None
        #self.file = open('Trace/max_tput_trace.dat','w')
        self.name = 'PPrEngTput'
        self.MODS=['BPSK','QPSK','QAM16','QAM64']
        self.rate={'BPSK':13.0e6,'QPSK':26.0e6,'QAM16':52.0e6,'QAM64':78.0e6}
        self.threshold = threshold

    def calc_energy(self):
        self.est_energy={} 
        keys = self.ber.keys()

        for key in keys: 
            ntx = self.get_ntx_from_key(key)
            nss = self.get_nss_from_key(key)
            plen = self.plen
            nrx = self.get_nrx_from_key(key)
            card_energy = self.card_type+'_'+self.econstraint+'_energy_ppr'
            energyfnc = eval(card_energy)
            if self.econstraint == 'tx': nant = ntx
            elif self.econstraint == 'rx': nant = nrx
            elif self.econstraint == 'tx_rx': nant = (ntx,nrx)
            else: assert 0 ,'invalid energy constraint selection'
            mod_eng={}
            for mod in self.MODS:
                mod_eng[mod]= energyfnc(nant,nss,plen,mod,self.ber[key][mod])
            self.est_energy[key] = mod_eng

    def calc_tput(self):

        self.tput={}
        keys = self.ber.keys()
        for key in keys:
            tput_val={}
            Nss = self.get_nss_from_key(key)
            for mod in self.MODS:
                # calculate tput for each modulation
                ber = self.ber[key][mod]
                n = get_retx_count(ber) # re-tx count is dependant on ber
                data_delivered = 8*self.plen*(1.0 - ber**n)
                #print "key: "+str(key)+"ber: "+str(ber)+" n: "+str(n)+" data: "+str(data_delivered)
                overhead = ((28.0 + 22.0/8)*8.0)/self.rate[mod] + 32.0e-6 + (4.0e-6*Nss)
                time_taken =  n*overhead + (self.plen*8/(self.rate[mod]*Nss))*(1- ber**n)/(1-ber)
                #print 'overhead: '+str(overhead)+'time: '+str(time_taken)
                tput_val[mod]=data_delivered/time_taken
            self.tput[key] =tput_val

    def find_max_tput(self):

        keys = self.ber.keys()

        maxtput=0.0
        maxtput_mod = -1
        maxtput_key = None
        for key in keys:
            for mod in self.MODS:
                val = self.tput[key][mod]
                if val > maxtput:
                   maxtput = val
                   maxtput_mod = mod
                   maxtput_key = key

        return {'tput': maxtput, 'key':maxtput_key, 'mod':maxtput_mod} 

    def search_rate(self,maxtput_info):

        tput_th = self.threshold*maxtput_info['tput']

        keys = self.ber.keys()

        min_eng_mod = maxtput_info['mod']
        min_eng_key = maxtput_info['key']
        min_energy = self.est_energy[min_eng_key][min_eng_mod]
        sel_tput = maxtput_info['tput']
        for key in keys:
            for mod in self.MODS:
                #if (self.tput[key][mod] >= tput_th) and (self.est_energy[key][mod] < min_energy) and (self.ber[key][mod] < 1.0e-3):
                if (self.tput[key][mod] >= tput_th) and (self.est_energy[key][mod] < min_energy):
                    sel_tput = self.tput[key][mod]
                    min_energy = self.est_energy[key][mod]
                    min_eng_mod = mod
                    min_eng_key = key

        return {'eng':min_energy, 'mod':min_eng_mod, 'key':min_eng_key, 'tput':sel_tput}

    def select_rate(self,pkt):
        self.extract_relevant_info(pkt)
        self.calc_snrs()
        self.calc_bers()
        self.calc_energy()
        self.calc_tput()

        maxtput_info = self.find_max_tput()
        rate_sel = self.search_rate(maxtput_info)
	
        minmodu = rate_sel['mod']

        if minmodu == 'BPSK': mcs = 0
        elif minmodu == 'QPSK': mcs = 2
        elif minmodu == 'QAM16': mcs = 4
        elif minmodu == 'QAM64': mcs = 7

        mode = rate_sel['key']

        ber=self.ber[rate_sel['key']][rate_sel['mod']] 
        trace = {'mod':rate_sel['mod'],'mode':rate_sel['key'],'tput':rate_sel['tput'],'energy':rate_sel['eng'],'ber':ber}
        print trace
        #self.file.write(str(trace)+str('\n'))


        return {'mcs':mcs,'mode':mode}
