#! /usr/bin/env python

from numpy import average
from basera import BaseRA
from helper import *
from error_rates import *
from energy import *
import time

class PPrMaxTputRA(BaseRA):

    def __init__(self,card_type,eng_cnst,predon=False):
        BaseRA.__init__(self,card_type,eng_cnst,predon)
        self.tput=None
        #self.file = open('Trace/max_tput_trace.dat','w')
        self.name = 'PPrMaxTput'
        self.MODS=['BPSK','QPSK','QAM16','QAM64']
        self.rate={'BPSK':13.0e6,'QPSK':26.0e6,'QAM16':52.0e6,'QAM64':78.0e6}


    def calc_tput(self):

        self.tput={}
        keys = self.ber.keys()
        for key in keys:
            tput_val=[]
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
                tput_val.append(data_delivered/time_taken)
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
        tput_tic = time.clock() 
        self.calc_tput()
        tput_toc = time.clock() 

        #print "time-> snr:"+str(snr_toc-snr_tic)+" ber:"+str(ber_toc-ber_tic)+" tput:"+str(tput_toc - tput_tic)

        keys = self.tput.keys()
        mcs=0
        maxtput=0
        mode=None
        for key in keys:
            tput = max(self.tput[key])
            tmpmcs = self.tput[key].index(tput)
            if tput > maxtput:
               maxtput =tput
               mcsi = tmpmcs
               mode = key

        #mcsi varies from 0 to 3 depending on modulation
        if mcsi == 0: mcs = 0
        elif mcsi == 1: mcs = 2
        elif mcsi == 2: mcs = 4
        elif mcsi == 3: mcs = 7

        ntx = self.get_ntx_from_key(mode)
        nss = self.get_nss_from_key(mode)
        nrx = self.get_nrx_from_key(mode)
        card_energy = self.card_type+'_'+self.econstraint+'_energy_ppr'
        energyfnc = eval(card_energy)
        if self.econstraint == 'tx': nant = ntx
        elif self.econstraint == 'rx': nant = nrx
        else: assert 0 ,'invalid energy constraint selection'
        modulation = MODULATION[mcs]
        ber = self.ber[mode][modulation]
        eng = energyfnc(nant,nss,self.plen,modulation,ber)
        #eng = rx_energy(nrx,nss,self.plen,mcs,self.per[mode][mcs])
        
        trace = {'mod':modulation,'mode':mode,'tput':maxtput,'energy':eng,'ber':ber}
        print trace
        #self.file.write(str(trace)+str('\n'))

        return {'mcs':mcs,'mode':mode}
