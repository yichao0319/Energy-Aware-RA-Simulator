#! /usr/bin/env python

from basera import BaseRA
from helper import *
from collections import deque

global_time=0

class SampleRate(BaseRA):

    def __init__(self):
        BaseRA.__init__(self,'intel','tx') # dummy parameters
        self.lltime = None
        self.lltable = None
        self.Rates = [6.0e6, 12.0e6, 18.0e6, 24.0e6, 36.0e6, 48.0e6, 54.0e6, 60.0e6]
        #self.modes = ['sm 3by3 GG','sm 2by3 DG','sm 2by2 DD','map 2by2 DD','sm 1by3 AG','map 2by1 DA','sm 1by2 AD','sm 1by1 AA']
        self.modes = ['sm 3by3 GG','sm 2by3 DG','sm 2by2 DD','sm 1by3 AG','sm 1by2 AD','sm 1by1 AA']
        self.calc_lossless_txtime()
        self.sort_lltime()

        self.curr_mcs= 7
        self.curr_mode= 'sm 3by3 GG'
        self.pkts_sent = 0

        self.avg_txtime = {}
        self.total_txtime = {}
        for mode in self.modes: self.avg_txtime[mode]=[-1 for m in range(0,8)]
        for mode in self.modes: self.total_txtime[mode]=[0 for m in range(0,8)]

        self.pkt_tries={}
        self.pkts_ackd={}
        self.consec_fails={}
        for mode in self.modes: self.pkt_tries[mode]=[0 for m in range(0,8)]
        for mode in self.modes: self.pkts_ackd[mode]=[0 for m in range(0,8)]
        for mode in self.modes: self.consec_fails[mode]=[0 for m in range(0,8)]

        # stale relevant variables
        self.stale_length = 100
        self.past_info = deque()

    def custom_sort(self,data):
     
        for itr in range(0,5):
            for index in range(0,len(data)-1):
                if data[index][0] == data[index+1][0]:
                   i1 = self.modes.index(data[index][1])
                   i2 = self.modes.index(data[index+1][1])
                   if i2 < i1:
                      tmp =data[index]
                      data[index] = data[index+1]
                      data[index+1] = tmp
        return data


    def sort_lltime(self):

        sorted_time=[]
        #for key in self.lltime.keys():
        for key in self.modes:
            for mcs in range(0,8):
                sorted_time.append((self.lltime[key][mcs],key,mcs))
        sorted_time.sort()
        self.lltable = self.custom_sort(sorted_time)

    def calc_lossless_txtime(self,plen=1000):
        self.lltime={}
        for mode in self.modes:
            ett=[]
            for mcs in range(0,8):
                Nss =  self.get_nss_from_key(mode)
                rate = self.Rates[mcs]
                ett.append(((28.0 + 22.0/8)*8.0)/rate + (plen*8)/(rate*Nss)+ 32.0e-6 + (4.0e-6*Nss))
            self.lltime[mode] = [1.0e6*t for t in ett]
            #print str(mode)+": "+str(self.lltime[mode])
        #print self.lltime

    def calc_txtime(self,plen,mode,mcs):
        # right now does not consider backoff and re-transmissions
        Nss =  self.get_nss_from_key(mode)
        rate = self.Rates[mcs]
        txtime = ((28.0 + 22.0/8)*8.0)/rate + (plen*8)/(rate*Nss)+ 32.0e-6 + (4.0e-6*Nss)
        return txtime*1.0e6


    def recalc_avg_txtime(self,k,m):
        if self.pkts_ackd[k][m] == 0:
           self.avg_txtime[k][m] = 1.0e8
        else:
           self.avg_txtime[k][m] = 1.0*self.total_txtime[k][m]/self.pkts_ackd[k][m]

    def find_min_avg_txtime(self):
        # set current bit rate to the one with smallest avg tx time
        # initialzed so that first tx is at highest rate
        mcs=7; mode='ppsm3by3'; mintime= 1e9 

        keys=self.avg_txtime.keys()
        for k in keys:
            for m in range(0,8):
                if self.avg_txtime[k][m] != -1:
                   if self.avg_txtime[k][m] < mintime:
                      mintime = self.avg_txtime[k][m]
                      mode = k
                      mcs = m
        return [mcs,mode]

    def apply_rate(self):

        if self.consec_fails[self.curr_mode][self.curr_mcs] == 4:
           # find the highest bit rate with no 4 successive failures
           loop=1; index=0
           while loop:
              [txtime,mode,mcs]= self.lltable[index] 
              if self.consec_fails[mode][mcs] < 4:
                 self.curr_mode = mode
                 self.curr_mcs = mcs
                 loop=0
              index = index + 1
              if index > len(self.lltable)-1: loop = 0

        # increment the pkts sent over the link
        self.pkts_sent = self.pkts_sent + 1      
        
        if self.pkts_sent%10 == 0:
           #Pick a rate with lltime less than curr rate avg txtime
           index=0; loop=1; llpicked=0
           while loop:
              [txtime,mode,mcs]= self.lltable[index] 
              if self.consec_fails[mode][mcs] < 4:
                 if self.lltime[mode][mcs] < self.avg_txtime[self.curr_mode][self.curr_mcs]:
                    self.curr_mode = mode
                    self.curr_mcs = mcs
                    loop=0
                    llpicked=1
                    
              index = index + 1
              if index > len(self.lltable)-1: loop = 0
                  
             
           #Otherwise, pick the rate with lowest avg txtime 
           if llpicked ==0:
              # find lowest avg tx time
              [mcs,mode] = self.find_min_avg_txtime()                
              self.curr_mode = mode
              self.curr_mcs = mcs


    def remove_stale_results(self):
        #Note: This implementation works on length
        #Note: Actual protocol works on time

        if len(self.past_info) >= self.stale_length:
           stale_data = self.past_info.popleft()

           # for the bitrate in stale data udpate total tx time
           stale_mode = stale_data['mode']
           stale_mcs = stale_data['mcs']
           stale_txtime = stale_data['txtime']
           self.total_txtime[stale_mode][stale_mcs]= self.total_txtime[stale_mode][stale_mcs] - stale_txtime

           # if pkt was succ, remove it from the bit rate count
           if stale_data['pkt_succ']==1:
              self.pkts_ackd[stale_mode][stale_mcs] = self.pkts_ackd[stale_mode][stale_mcs] - 1

           self.recalc_avg_txtime(stale_mode,stale_mcs)
           [self.curr_mcs,self.curr_mode] = self.find_min_avg_txtime()

        
    def process_feedback(self,si):

        global global_time
        global_time = global_time + 1

        mode = self.curr_mode
        mcs = self.curr_mcs

        #1. Calc tx time and update total tx time
        txtime = self.calc_txtime(si.plen,mode,mcs)
        self.total_txtime[mode][mcs] = self.total_txtime[mode][mcs] + txtime

        #2. If succ, update num_succ
        if si.succ == 1:
           self.pkts_ackd[mode][mcs] = self.pkts_ackd[mode][mcs] + 1
           self.consec_fails[mode][mcs] = 0
        else:
        #3. If fail, update consec_fails, otherwise reset
           self.consec_fails[mode][mcs] = self.consec_fails[mode][mcs] + 1

        #4. Re-calc avg tx time
        assert self.total_txtime[mode][mcs]!=0,"total txtime not assigned a value"
        if self.pkts_ackd[mode][mcs] == 0:
           self.avg_txtime[mode][mcs] = 1.0e8
        else:
           self.avg_txtime[mode][mcs] = 1.0*self.total_txtime[mode][mcs]/self.pkts_ackd[mode][mcs]

        #5. Set the bit-rate to one with min avg txtime
        [self.curr_mcs,self.curr_mode]=self.find_min_avg_txtime()
        

        #6. Append curr_time, pkt status, tx time and bit-rate to resutls
        info = {'curr_time':global_time, 'pkt_succ':si.succ, 'txtime':txtime, 'mcs':mcs, 'mode':mode}
        self.past_info.append(info)



    def select_rate(self,pkt):
        self.remove_stale_results()
        self.apply_rate()
        # return [self.curr_mcs,self.curr_mode]
        return {'mcs':self.curr_mcs,'mode':self.curr_mode}

def main():
    ra = SampleRate()

if __name__=="__main__":
   main()
