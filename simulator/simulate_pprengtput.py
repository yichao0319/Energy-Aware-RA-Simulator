#! /usr/bin/env python

#import common
import os
dir=os.getcwd()
import sys
sys.path.append(dir+'simulator')
from trace_chan import TraceChan
#from conftrace_chan import TraceChan
from ppr_receiver import PPrReceiver
from transmitter import Transmitter
from pprengtputra import PPrEngTputRA
import time

def main():
    if len(sys.argv) == 7:
       filename = sys.argv[1]
       card_type = sys.argv[2]
       energy_constraint = sys.argv[3]
       chan_pred = eval(sys.argv[4])
       threshold = eval(sys.argv[5])
       increment = eval(sys.argv[6])
       print "filename: "+str(filename)
    else:
        print "Correct usage: python simulate_maxtput.py trace_file card_type tx/rx pred(True/False)"
        sys.exit(1) 

    nrx=3
    # Create a tx
    ntx=3
    ta = None
    transmitter = Transmitter(ntx,ta)
    # Create a channel
    
    chan = TraceChan(filename)
    num_chans=1
    length = chan.create_chan(transmitter.Ntx,nrx)

    extname=filename.split('/')[-1].split('.')[0]+"_"+card_type+"_"+energy_constraint+"_pred"+str(chan_pred)+"th"+str(threshold)+"_inc"+str(increment)
    #print extname
    receiver = PPrReceiver(PPrEngTputRA(card_type,energy_constraint,chan_pred,threshold),nrx,extname)

    if length > 10000: length = 10000
    #length = 2
   
    for num in range(0,length):
        itr_tic = time.clock() 
        pkt = transmitter.transmit_pkt()
        chan.apply_channel(pkt)
        #print chan.curr_chan
        #print pkt
        
        # Create receiver
        receiver.receive_pkt(pkt)
        ack_pkt = receiver.get_feedback_pkt()
        
        transmitter.process_ack(ack_pkt)
        itr_toc = time.clock() 
        #print "one itr: "+str(itr_toc - itr_tic)


if __name__=="__main__":
   main()
