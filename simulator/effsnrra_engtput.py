#! /usr/bin/env python

from basera import BaseRA
from qinv import Qinverse
from numpy import average
from error_rates import *
from helper import *
from energy import *

class EffSnrRAEngTput(BaseRA):

    def __init__(self,card_type,eng_cnst,predon=False, threshold=0.9):
        BaseRA.__init__(self,card_type,eng_cnst,predon)
        self.eff_snr= None
        self.mcs = None
        self.tput = None
        self.q = Qinverse()
        #self.th=[3,6.5,8,12.5,14.5,18,21,22.5]
        #self.th=[3, 5.36, 8.4, 12.06, 15.08, 19.9, 21.45, 23.17] #Tput
        self.th=[2.96, 5.96, 8.8, 12.4, 15.5, 20.22, 21.43, 23.08]  # 90% DR
        #self.file = open('Trace/eff_snr_trace.dat','w')
	self.threshold= threshold
        self.name = 'EffSnrEngTput'


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
        for key in keys:
            eff_snr  = self.eff_snr[key]
            self.mcs[key]=[]
            if linear2db(eff_snr['QAM64']) > self.th[7]: self.mcs[key].append(7)
            if linear2db(eff_snr['QAM64']) > self.th[6]: self.mcs[key].append(6)
            if linear2db(eff_snr['QAM64']) > self.th[5]: self.mcs[key].append(5)
            if linear2db(eff_snr['QAM16']) > self.th[4]: self.mcs[key].append(4)
            if linear2db(eff_snr['QAM16']) > self.th[3]: self.mcs[key].append(3)
            if linear2db(eff_snr['QPSK']) > self.th[2]: self.mcs[key].append(2)
            if linear2db(eff_snr['QPSK']) > self.th[1]: self.mcs[key].append(1)
            if linear2db(eff_snr['BPSK']) > self.th[0]: self.mcs[key].append(0)
        #print self.mcs

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
            self.est_energy[key] = [energyfnc(nant, nss, plen , mcs,0.0) for mcs in range(0,8)]

        #print "eng: "+str(self.est_energy)

    def calc_tput(self):

        self.tput={}
        keys = self.eff_snr.keys()
        Nsub = 52
        for key in keys:
            tput_val=[]
            Nss = self.get_nss_from_key(key)
            for mcs in range(0,8):
                BpS = Nsub*mcs2nbpsc(mcs)*Nss/8.0
                num_ofdm_sym = 1.0*self.plen/BpS
                tput_val.append(8*self.plen*(1.0)/(num_ofdm_sym*4.0))
            self.tput[key] = tput_val
            #print "key: "+str(key)+" -> "+str(self.tput[key])

    def find_max_tput(self):

        keys = self.tput.keys()

        maxtput=0.0
        maxtput_mcs = -1
        maxtput_key = None
        maxsnr = 0.0

        for key in keys:
            for mcs in self.mcs[key]:
                if self.tput[key][mcs] > maxtput:
                   maxtput = self.tput[key][mcs]
                   maxtput_mcs = mcs
                   maxtput_key = key
                   maxsnr = self.eff_snr[key][mcs2mod(mcs)]
                elif (self.tput[key][mcs] == maxtput) and (self.eff_snr[key][mcs2mod(mcs)] > maxsnr):
                   maxtput = self.tput[key][mcs]
                   maxtput_mcs = mcs
                   maxtput_key = key
                   maxsnr = self.eff_snr[key][mcs2mod(mcs)]

        return {'tput': maxtput, 'key':maxtput_key, 'mcs':maxtput_mcs} 

    def search_rate(self,maxtput_info):

        tput_th = self.threshold*maxtput_info['tput']

        keys = self.tput.keys()

        min_eng_mcs = maxtput_info['mcs']
        min_eng_key = maxtput_info['key']
        min_energy = self.est_energy[min_eng_key][min_eng_mcs]
        sel_tput = maxtput_info['tput']
        for key in keys:
            for mcs in self.mcs[key]:
                if self.tput[key][mcs] >= tput_th and self.est_energy[key][mcs] < min_energy:
                    sel_tput = self.tput[key][mcs]
                    min_energy = self.est_energy[key][mcs]
                    min_eng_mcs = mcs
                    min_eng_key = key

        return {'eng':min_energy, 'mcs':min_eng_mcs, 'key':min_eng_key, 'tput':sel_tput}


          
    def select_rate(self,pkt):
        self.extract_relevant_info(pkt)
        self.calc_snrs()
        self.calc_bers()
        self.calc_effsnr()
        self.calc_energy()
        self.calc_tput()
        self.pick_mcs()
        max_tput = self.find_max_tput()
        #print max_tput
        rate_sel = self.search_rate(max_tput)
       
        mineng=1.0e6 # Pick a very large to start
        maxsnr=0

        mode = rate_sel['key']
        mcs = rate_sel['mcs']
        
        trace = {'mcs':mcs,'mode':mode,'tput':rate_sel['tput'],'energy':rate_sel['eng'], 'succ':pkt.succ}
        print trace
        #self.file.write(str(trace)+str('\n'))

        return [mode,mcs]
