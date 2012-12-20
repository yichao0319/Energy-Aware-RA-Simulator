#! /usr/bin/env python

from basera import BaseRA
from helper import *
from error_rates import *
from energy import *

# The RA protocol maintains a per of atleast 90%

class MinEngRA(BaseRA):

    def __init__(self,card_type,eng_cnst,predon=False):
        BaseRA.__init__(self,card_type,eng_cnst,predon)
        self.subset_pers = None
        self.est_energy = None
        #self.file = open('Trace/min_energy_trace.dat','w')
        self.name = 'MinEng'
        

#    def select_per_subset(self,perth=0.1):
#
#        self.subset_pers={}
#        keys = self.per.keys()
#
#        for key in keys:
#            self.subset_pers[key] = [ (mcs,per) for mcs,per in zip(range(0,8),self.per[key]) if per < perth]
#            if self.subset_pers[key] == []: del(self.subset_pers[key])
#        #print self.subset_pers


#    def calc_energy(self):
#        self.est_energy={} 
#        keys = self.subset_pers.keys()
#
#        for key in keys: 
#            ntx = self.get_ntx_from_key(key)
#            nss = self.get_nss_from_key(key)
#            plen = self.plen
#            nrx = self.get_nrx_from_key(key)
#            card_energy = self.card_type+'_'+self.econstraint+'_energy'
#            energyfnc = eval(card_energy)
#            if self.econstraint == 'tx': nant = ntx
#            elif self.econstraint == 'rx': nant = nrx
#            else: assert 0 ,'invalid energy constraint selection'
#            self.est_energy[key] = [(mcs,energyfnc(nant,nss,plen,mcs[0],mcs[1])) for mcs in self.subset_pers[key]]
#
#            #self.est_energy[key] = [(mcs,rx_energy(nrx,nss,plen,mcs[0],mcs[1])) for mcs in self.subset_pers[key]]
##        #print "eng: "+str(self.est_energy)

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
            elif self.econstraint == 'tx_rx': nant = (ntx,nrx)
            else: assert 0 ,'invalid energy constraint selection'
            self.est_energy[key] = [energyfnc(nant,nss,plen,mcs,0.0) for mcs in range(0,8)]


    def calc_tput(self,key,mcs):

        Nsub = 52
        Nss = self.get_nss_from_key(key)
        BpS = Nsub*mcs2nbpsc(mcs)*Nss/8.0
        num_ofdm_sym = 1.0*self.plen/BpS
        #tput = 8*self.plen*(1.0-self.per[key][mcs])/(num_ofdm_sym*4.0)
        tput = 8*self.plen*(1.0)/(num_ofdm_sym*4.0)
        return tput

    def select_rate(self,pkt):
        self.extract_relevant_info(pkt)
        self.calc_snrs()
        self.calc_bers()
        self.calc_pers()
        #self.select_per_subset()
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

        #If this called it means that there is no configuration with per < 0.1
        if minmode == 0:            
            minmode = 'sm 1by1 AA'
            minmcs = 0
            mineng = self.est_energy[minmode][minmcs]

        tput = self.calc_tput(minmode,minmcs)

        trace = {'mcs':minmcs,'mode':minmode,'tput':tput,'energy':mineng}
        print trace
        #self.file.write(str(trace)+str('\n'))

        return {'mcs':minmcs,'mode':minmode}

#        mineng = 10000 
#        for k in keys:
#            (tmpmcs, eng)=min(self.est_energy[k], key=lambda x: x[1])
#
#            if eng < mineng:
#               mineng =eng
#               mcs = tmpmcs
#               mode = k
#
#        tput = self.calc_tput(mode,mcs[0])
#        trace = {'mcs':mcs[0],'mode':mode,'tput':tput,'energy':mineng, 'succ':pkt.succ}
#        print trace
#        #self.file.write(str(trace)+str('\n'))
#
#        return [mode,mcs[0]]
