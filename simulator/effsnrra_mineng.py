#! /usr/bin/env python

from basera import BaseRA
from qinv import Qinverse
from numpy import average
from error_rates import *
from helper import *
from energy import *

class EffSnrRAEng(BaseRA):

    def __init__(self,card_type,eng_cnst,predon=False):
        BaseRA.__init__(self,card_type,eng_cnst,predon)
        self.eff_snr= None
        self.mcs = None
        self.tput = None
        self.q = Qinverse()
        #self.th=[3,6.5,8,12.5,14.5,18,21,22.5]
        #self.th=[3, 5.36, 8.4, 12.06, 15.08, 19.9, 21.45, 23.17] #Tput
        self.th=[2.96, 5.96, 8.8, 12.4, 15.5, 20.22, 21.43, 23.08]  # 90% DR
        #self.file = open('Trace/eff_snr_trace.dat','w')
        self.name = 'EffSnrEng'


    def berinv_bpsk(self,x): return (self.q.Qinv(x)**2)/2.0
    def berinv_qpsk(self,x): return self.q.Qinv(x)**2
    def berinv_qam16(self,x): return 5.0*(self.q.Qinv((x*4.0/3)))**2
    def berinv_qam64(self,x): return 21.0*(self.q.Qinv((x*12.0/7)))**2

    def calc_effsnr(self):
        self.eff_snr={}
        keys = self.ber.keys()
        for key in keys:
            mod={}
            mod['BPSK'] = self.berinv_bpsk(self.ber[key]['BPSK'])
            mod['QPSK'] = self.berinv_qpsk(self.ber[key]['QPSK'])
            mod['QAM16'] = self.berinv_qam16(self.ber[key]['QAM16'])
            mod['QAM64'] = self.berinv_qam64(self.ber[key]['QAM64'])
            self.eff_snr[key] = mod
        #print self.eff_snr


    def calc_bers(self):
        self.ber={}
        keys = self.snr.keys()
        for key in keys:
            mod={}
            mod['BPSK']=average([average(calc_effber_BPSK(s)) for s in self.snr[key]])
            mod['QPSK']=average([average(calc_effber_QPSK(s)) for s in self.snr[key]])
            mod['QAM16']=average([average(calc_effber_QAM16(s)) for s in self.snr[key]])
            mod['QAM64']=average([average(calc_effber_QAM64(s)) for s in self.snr[key]])
            self.ber[key] = mod
        #print self.ber


    def pick_mcs(self):
        self.mcs={}
        keys = self.eff_snr.keys()
        # for each key pick the mcs which has the minimum energy and can be supported
        mineng = 1.0e6
        minmcs = -1
        minmode = 0
        for key in keys:
            for mcs,eng in zip(range(0,8),self.est_energy[key]):
                if (eng < mineng) and (linear2db(self.eff_snr[key][mcs2mod(mcs)]) > self.th[mcs]):
                    mineng = eng
                    minmcs = mcs
                    minmode = key
        return {'eng':mineng, 'mcs': minmcs, 'mode':minmode}
        #print self.mcs

    def calc_tput(self,key,mcs):

        Nsub = 52
        Nss = self.get_nss_from_key(key)
        BpS = Nsub*mcs2nbpsc(mcs)*Nss/8.0
        num_ofdm_sym = 1.0*self.plen/BpS
        tput = 8*self.plen*(1.0)/(num_ofdm_sym*4.0)
        return tput

    def calc_energy(self):
        self.est_energy={} 
        keys = self.eff_snr.keys()

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

        #print "eng: "+str(self.est_energy)

          

    def select_rate(self,pkt):
        self.extract_relevant_info(pkt)
        self.calc_snrs()
        self.calc_bers()
        self.calc_effsnr()
        self.calc_energy()
        picked_rate = self.pick_mcs()
        tput = self.calc_tput(picked_rate['mode'],picked_rate['mcs'])

        mcs = picked_rate['mcs']
        mode = picked_rate['mode']
        mineng = picked_rate['eng']

        trace = {'mcs':mcs,'mode':mode,'tput':tput,'energy':mineng, 'succ':pkt.succ}
        print trace
        #self.file.write(str(trace)+str('\n'))

        return [mode,mcs]
