#! /usr/bin/env python

from numpy import average
from qinv import Qinverse
from basera import BaseRA
from helper import *
from error_rates import *
from energy import *


class OracleEffSnrRA(BaseRA):

    def __init__(self,card_type,eng_cnst,chan):
        BaseRA.__init__(self,card_type,eng_cnst)
        assert chan != None, "Oracle must have channel ref at time of instantiation"
        self.chan = chan
        self.eff_snr= None
        self.mcs = None
        self.tput = None
        self.q = Qinverse()
        #self.th=[3,6.5,8,12.5,14.5,18,21,22.5]
        #self.th=[3, 5.36, 8.4, 12.06, 15.08, 19.9, 21.45, 23.17] #Tput
        self.th = [2.96, 5.96, 8.8, 12.4, 15.5, 20.22, 21.43, 23.08]  # 90% DR
        #self.file = open('Trace/eff_snr_trace.dat','w')
        self.name = 'OracleEffSnr'

    def set_relevant_info(self,pkt):
        self.chanmag = self.chan.peek_next_channel()
        self.plen = pkt.length

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
            if linear2db(eff_snr['QAM64']) > self.th[7]: self.mcs[key]=7
            elif linear2db(eff_snr['QAM64']) > self.th[6]: self.mcs[key]=6
            elif linear2db(eff_snr['QAM64']) > self.th[5]: self.mcs[key]=5
            elif linear2db(eff_snr['QAM16']) > self.th[4]: self.mcs[key]=4
            elif linear2db(eff_snr['QAM16']) > self.th[3]: self.mcs[key]=3
            elif linear2db(eff_snr['QPSK']) > self.th[2]: self.mcs[key]=2
            elif linear2db(eff_snr['QPSK']) > self.th[1]: self.mcs[key]=1
            elif linear2db(eff_snr['BPSK']) > self.th[0]: self.mcs[key]=0
            else: self.mcs[key]=-1
        #print self.mcs

    def calc_tput(self):
        self.tput={}
        keys = self.mcs.keys()
        Nsub = 52
        rate = [6.5e6, 13.0e6, 19.5e6, 26.0e6, 39.0e6, 52.0e6, 58.5e6, 65.0e6]
        for key in keys:
            mcs = self.mcs[key]
            if mcs == -1: self.tput[key]=0
            else:
               plen = self.plen
               Nss = self.get_nss_from_key(key)
               ett = ((28.0 + 22.0/8)*8.0)/rate[mcs] + (plen*8)/(rate[mcs]*Nss) + 32.0e-6 + (4.0e-6*Nss)
               #print mcs, key, ett*1.0e6
               self.tput[key] = 8*self.plen/ett
               #self.tput[key] = 8*self.plen*(1.0 - self.per[key][mcs])/(num_ofdm_sym*4.0)
        #print self.tput


    def process_feedback(self,ack_pkt):
        ack = ack_pkt # just a redundant statement for completeness

    def select_rate(self,pkt):
        self.set_relevant_info(pkt)
        self.calc_snrs()
        self.calc_bers()
        self.calc_effsnr()
        self.pick_mcs()
        self.calc_tput()

        maxtput=0
        maxsnr=0
        for key in self.tput.keys():
            if self.tput[key] > maxtput:
                maxtput = self.tput[key]
                mode = key
                mcs = self.mcs[key]
                maxsnr = self.eff_snr[key][mcs2mod(mcs)]
            elif self.tput[key] == maxtput and self.eff_snr[key][mcs2mod(self.mcs[key])]> maxsnr:
                maxtput = self.tput[key]
                mode = key
                mcs = self.mcs[key]
                maxsnr = self.eff_snr[key][mcs2mod(mcs)]


        ntx = self.get_ntx_from_key(mode)
        nss = self.get_nss_from_key(mode)
        nrx = self.get_nrx_from_key(mode)
        card_energy = self.card_type+'_'+self.econstraint+'_energy'
        energyfnc = eval(card_energy)
        if self.econstraint == 'tx': nant = ntx
        elif self.econstraint == 'rx': nant = nrx
        else: assert 0 ,'invalid energy constraint selection'
        eng = energyfnc(nant,nss,self.plen,mcs, 0.0)

        #eng = rx_energy(nrx,nss,self.plen,mcs,self.per[mode][mcs])

        trace = {'mcs':mcs,'mode':mode,'tput':maxtput,'energy':eng}
        print trace
        #self.file.write(str(trace)+str('\n'))

        return {'mcs':mcs,'mode':mode}
