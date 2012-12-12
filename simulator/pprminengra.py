#! /usr/bin/env python

from numpy import average
from basera import BaseRA
from helper import *
from error_rates import *
from energy import *
import time

class PPrMinEngRA(BaseRA):

    def __init__(self,card_type,eng_cnst,predon=False):
        BaseRA.__init__(self,card_type,eng_cnst,predon)
        self.tput=None
        #self.file = open('Trace/max_tput_trace.dat','w')
        self.name = 'PPrMinEng'
        self.MODS=['BPSK','QPSK','QAM16','QAM64']
        self.rate={'BPSK':13.0e6,'QPSK':26.0e6,'QAM16':52.0e6,'QAM64':78.0e6}

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
            else: assert 0 ,'invalid energy constraint selection'
            mod_eng={}
            for mod in self.MODS:
                mod_eng[mod]= energyfnc(nant,nss,plen,mod,self.ber[key][mod])
            self.est_energy[key] = mod_eng


    def calc_tput(self,mod,key):

        Nss = self.get_nss_from_key(key)
        ber = self.ber[key][mod]
        n = get_retx_count(ber) # re-tx count is dependant on ber
        data_delivered = 8*self.plen*(1.0 - ber**n)
        #print "key: "+str(key)+"ber: "+str(ber)+" n: "+str(n)+" data: "+str(data_delivered)
        overhead = ((28.0 + 22.0/8)*8.0)/self.rate[mod] + 32.0e-6 + (4.0e-6*Nss)
        time_taken =  n*overhead + (self.plen*8/(self.rate[mod]*Nss))*(1- ber**n)/(1-ber)
        #print 'overhead: '+str(overhead)+'time: '+str(time_taken)
        tput_val = data_delivered/time_taken
        return tput_val
        #print self.tput

    def select_rate(self,pkt):
        self.extract_relevant_info(pkt)
        self.calc_snrs()
        self.calc_bers()
        self.calc_energy()


        keys = self.est_energy.keys()
        mineng = 1.0e6
        minmodu = -1
        minmode = 0
        for key in keys:
            for mod in self.MODS:
                eng = self.est_energy[key][mod]
                #FIXME: ber th should match per value of 0.1
                #if (eng < mineng) and (self.ber[key][mod] < 1.0e-3): # PER constrained at 0.1
                if (eng < mineng): # PER constrained at 0.1
                    mineng = eng
                    minmodu = mod
                    minmode = key



        if minmodu == 'BPSK': mcs = 0
        elif minmodu == 'QPSK': mcs = 2
        elif minmodu == 'QAM16': mcs = 4
        elif minmodu == 'QAM64': mcs = 7

        ber=self.ber[minmode][minmodu] 
        tput = self.calc_tput(minmodu,minmode)
        trace = {'mod':minmodu,'mode':minmode,'tput':tput,'energy':mineng,'ber':ber}
        print trace
        #self.file.write(str(trace)+str('\n'))

        return {'mcs':mcs, 'mode':minmode}
