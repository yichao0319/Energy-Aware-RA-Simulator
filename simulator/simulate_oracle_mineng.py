#! /usr/bin/env python

#import common
import os
dir=os.getcwd()
import sys
sys.path.append(dir+'simulator')
from trace_chan import TraceChan
from receiver import Receiver
from transmitter import Transmitter
from oracle_minengra import OracleMinEngRA
from rxoracle import RxOracle

def main():

    if len(sys.argv) == 6:
       filename = sys.argv[1]
       card_type = sys.argv[2]
       energy_constraint = sys.argv[3]
       chan_pred = False
       increment = eval(sys.argv[5])
       print "filename: "+str(filename)
    else:
        print "Correct usage: python simulate_effsnr.py trace_file card_type tx/rx pred(True/False)"
        sys.exit(1)

    nrx=3
    # Create a tx
    ntx=3
    ta = None
    transmitter = Transmitter(ntx,ta)
    # Create a channel
    
    chan = TraceChan(filename, increment)
    length = chan.create_chan(transmitter.Ntx,nrx)
 
    ta = OracleMinEngRA(card_type,energy_constraint,chan)
    transmitter.set_transmit_ra(ta)
    extname=ta.name+"_"+filename.split('/')[-1].split('.')[0]+"_"+card_type+"_"+energy_constraint+"_pred"+str(chan_pred)+"_inc"+str(increment)
    receiver = Receiver(RxOracle(card_type,energy_constraint),nrx,extname)

    if length > 10000: length = 10000
    #length =10
    for num in range(0,length):
        pkt = transmitter.transmit_pkt()
        chan.apply_channel(pkt)
        #print chan.curr_chan
        #print pkt
        
        # Create receiver
        receiver.receive_pkt(pkt)
        ack_pkt = receiver.get_feedback_pkt()
        
        transmitter.process_ack(ack_pkt)


if __name__=="__main__":
   main()
