#! /usr/bin/env python

from numpy import average
from helper import *
from error_rates import *
from spatialmux import *
from spatialmap import *
from hwpred import HoltsWinter
import time


class BaseRA:

    def __init__(self,card_type,constraint,predon=False):
        self.MCS = None
        self.chanmag = None
        self.rxpwr = None
        self.ntx = None
        self.nrx = None
        self.npow = None
        self.plen = None
        self.mode = None
        self.snr={}
        self.ber={}
        self.per={}
        self.card_type = card_type
        self.econstraint = constraint
        self.pred_flag = predon
        self.pred_first_time = True

        self.max_ntx = 3
        self.max_nrx = 3
        self.max_sc = 30
        if predon is True: 
            # self.predictor = HoltsWinter()
            self.predictor = []
            for tx_i in range(0, self.max_ntx):
                txp = []
                for rx_i in range(0, self.max_nrx):
                    rxp = []
                    for sc_i in range(0, self.max_sc): 
                        rxp.append(HoltsWinter())
                    txp.append(rxp)
                self.predictor.append(txp)
        else: 
            self.predictor = None
        # print self.predictor

    def extract_relevant_info(self,pkt):
        self.chanmag = pkt.ChanMag
        self.rxpwr = pkt.RxPwr
        self.npow = pkt.Noise 
        self.ntx = pkt.Ntx
        self.nrx = pkt.Nrx
        self.plen = pkt.length
        self.mode = pkt.Mode
	#print pkt
        # channel prediction should be perfomred here
        if self.pred_flag is True:
            # if self.pred_first_time is True:
            #    self.predictor.setup_a(self.chanmag)
            #    self.predictor.setup_b(self.chanmag)
            #    self.pred_first_time = False
            # pred_chan = self.predictor.get_next_pred(self.chanmag)
            # self.chanmag = pred_chan
            for tx_i in range(0, self.ntx):
                for rx_i in range(0, self.nrx):
                    for sc_i in range(0, self.max_sc):
                        new_measurement = self.chanmag[tx_i, rx_i, sc_i]
                        hw_pred = self.predictor[tx_i][rx_i][sc_i]
                        self.chanmag[tx_i, rx_i, sc_i] = hw_pred.pred
                        hw_pred.update(new_measurement)


    def select_applicable_snrs(self,snr_vals,config,t,r):

        ant_config = self.mode.split()[2]
        tx = ant_config[0]
        rx = ant_config[1]
        fnct = eval('self.ant_config'+str(t))
        fncr = eval('self.ant_config'+str(r))
        for row in fnct(tx):
            for col in fncr(rx):
                key = config+" "+str(row)+str(col)
                self.snr[key] = snr_vals[key]
        
    def calc_snrs(self):

        self.snr={}
        #Spatial Multiplexing Cases:1x1,1x2,1x3,2x2,2x3,3x3
        [M,N,S] = self.chanmag.shape
        #M = self.get_ntx_from_key(self.mode)
        #N = self.get_nrx_from_key(self.mode)
        if M > 0:
           if N > 0:
              snr1by1=calc_snr_sm1by1(self.chanmag)
              #self.select_applicable_snrs(snr1by1,"sm 1by1",1,1)
              self.snr.update(snr1by1)
           if N > 1:
              snr1by2=calc_snr_sm1by2(self.chanmag)
              self.snr.update(snr1by2)
              #self.select_applicable_snrs(snr1by2,"sm 1by2",1,2)
           if N > 2:
              snr1by3=calc_snr_sm1by3(self.chanmag)
              self.snr.update(snr1by3)
              #self.select_applicable_snrs(snr1by3,"sm 1by3",1,3)
        if M > 1:
           if N > 1:
              snr2by2=calc_snr_sm2by2(self.chanmag)
              self.snr.update(snr2by2)
              #self.select_applicable_snrs(snr2by2,"sm 2by2",2,2)
           if N > 2:
              snr2by3=calc_snr_sm2by3(self.chanmag)
              self.snr.update(snr2by3)
              #self.select_applicable_snrs(snr2by3,"sm 2by3",2,3)
        if M > 2 and N > 2:
           snr3by3=calc_snr_sm3by3(self.chanmag)
           self.snr.update(snr3by3)
           #self.select_applicable_snrs(snr3by3,"sm 3by3",3,3)

        #Mapping Cases: STBC:2x1,2x2,3x2, CDD:3x1
#        if M > 1:
#           if N > 0:
#              snrm2by1=calc_snr_map2by1(self.chanmag)
#              self.snr.update(snrm2by1)
#              #self.select_applicable_snrs(snrm2by1,"map 2by1",2,1)
#           if N > 1:
#              snrm2by2=calc_snr_map2by2(self.chanmag)
#              self.snr.update(snrm2by2)
#              #self.select_applicable_snrs(snrm2by2,"map 2by2",2,2)
#        if M > 2:
#           if N > 0:
#              snrm3by1=calc_snr_map3by1(self.chanmag)
#              self.snr.update(snrm3by1)
#              #self.select_applicable_snrs(snrm3by1,"map 3by1",3,1)
#           if N > 1:
#              snrm3by2=calc_snr_map3by2(self.chanmag)
#              self.snr.update(snrm3by2)
#              #self.select_applicable_snrs(snrm3by2,"map 3by2",3,2)

        #print self.snr

    def old_calc_snrs(self):
        for ntx in range(1,self.ntx+1):
            for nrx in range(ntx,self.nrx+1):
                key='ppsm'+str(ntx)+'by'+str(nrx)
                self.snr[key] = calc_snr_sm(self.chanmag,ntx,nrx)

        self.snr['ppmap2by1']=calc_snr_2by1(self.chanmag)
        self.snr['ppmap2by2']=calc_snr_2by2(self.chanmag)
        self.snr['ppmap3by1']=calc_snr_3by1(self.chanmag)
        self.snr['ppmap3by2']=calc_snr_3by2(self.chanmag)
        # Spatial mapping snr calculation
#        for ntx in range(2,self.ntx+1):
#            for nrx in range(1,ntx+1):
#               key='ppmap'+str(ntx)+'by'+str(nrx)
#               print key
#               self.snr[key] = calc_snr_map(self.chanmag,ntx,nrx)

        #print self.snr

    def calc_bers(self):
        self.ber={}
        keys = self.snr.keys()

        for key in keys:
            mod={}
            #bpsk_tic = time.clock()
            mod['BPSK']=average([average(calc_ber_BPSK(s)) for s in self.snr[key]])
            mod['QPSK']=average([average(calc_ber_QPSK(s)) for s in self.snr[key]])
            mod['QAM16']=average([average(calc_ber_QAM16(s)) for s in self.snr[key]])
            mod['QAM64']=average([average(calc_ber_QAM64(s)) for s in self.snr[key]])
            self.ber[key] = mod
            #bpsk_toc = time.clock()
            #print "bpsk time ->"+str(bpsk_toc -bpsk_tic)
        #print self.ber['sm 2by2 DE']
        #print self.ber['sm 2by3 DG']
        #print self.ber

    def calc_pers(self):
        self.per={}
        keys = self.ber.keys()
        MCS=range(0,8)

        for key in keys:
            self.per[key]=[calc_per(self.plen,mcs,self.ber[key][mcs2mod(mcs)]) for mcs in MCS]
        #print self.per

    def ant_config1(self, ant):
        table={'A':['A'], 'B':['B'], 'C':['C'], 'D':['A','B'], 'E':['B','C'], 'F':['A','C'], 'G':['A','B','C']}
        return table[ant]

    def ant_config2(self, ant):
        table={'D':['D'], 'E':['E'], 'F':['F'], 'G':['D','E','F']}
        return table[ant]

    def ant_config3(self, ant):
        table={'G':['G']}
        return table[ant]

    def get_nss_from_key(self,key):
        k = key.split()
        newkey = k[0]+' '+k[1]
        table={'sm 1by1':1, 'sm 1by2':1, 'sm 1by3':1,'sm 2by2':2, 'sm 2by3':2, 'sm 3by3':3, 'map 2by1':1, 'map 2by2':1, 'map 3by1':1, 'map 3by2':2, 'map 3by3':1}
        return table[newkey] 

    def get_dup_from_key(self,key):
        table={'sm1by1':0, 'sm2by2':0, 'sm3by3':0, 'stbc2by2':0, 'hybrid3by3':0}
        return table[key] 

    def get_nrx_from_key(self,key):
        k = key.split()
        newkey = k[1]
        table={'1by1':1, '1by2':2, '1by3':3,'2by2':2, '2by3':3, '3by3':3, '2by1':1, '2by2':2, '3by1':1, '3by2':2, '3by3':3}
        return table[newkey] 

    def get_ntx_from_key(self,key):
        k = key.split()
        newkey = k[1]
        table={'1by1':1, '1by2':1, '1by3':1,'2by2':2, '2by3':2, '3by3':3, '2by1':2, '2by2':2, '3by1':3, '3by2':3, '3by3':3}
        return table[newkey] 

    def select_rate(self):
        return 0
