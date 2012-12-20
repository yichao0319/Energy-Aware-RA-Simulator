#! /usr/bin/env python

from energy import *
from basera import BaseRA

class RxSampleRate(BaseRA):

    def __init__(self,card_type,eng_cnst):
        BaseRA.__init__(self,card_type,eng_cnst)
        #self.file = open('Trace/samplerate_trace.dat','w')
        self.name = 'SampleRate'
        self.succ_hist=[]
        self.per = 0.0

    def update_per(self,succ):

          if len(self.succ_hist)<20:
              self.succ_hist.append(succ)
          else:
              self.succ_hist.pop(0)
              self.succ_hist.append(succ)

          per = 1.0*sum(self.succ_hist)/len(self.succ_hist)
          return per

    def select_rate(self,pkt):
          self.extract_relevant_info(pkt)
          mode = pkt.Mode
          mcs = pkt.MCS
          ntx = self.get_ntx_from_key(mode)
          nss = self.get_nss_from_key(mode)
          nrx = self.get_nrx_from_key(mode)
          per = self.update_per(pkt.succ) 
          card_energy = self.card_type+'_'+self.econstraint+'_energy'
          energyfnc = eval(card_energy)
          if self.econstraint == 'tx': nant = ntx
          elif self.econstraint == 'rx': nant = nrx
          elif self.econstraint == 'tx_rx': nant = (ntx,nrx)
          else: assert 0 ,'invalid energy constraint selection'
          eng = energyfnc(nant,nss,self.plen,mcs,per)

          #eng = rx_energy(nrx,nss,self.plen,mcs,per)
          succ = pkt.succ

          # calculate tput
  
          trace = {'mcs':mcs,'mode':mode,'succ':succ,'energy':eng}
          print trace
          #self.file.write(str(trace)+str('\n'))
          return {'mcs':0,'mode':0}
