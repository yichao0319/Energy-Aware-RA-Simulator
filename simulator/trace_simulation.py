#! /usr/bin/env python

#import common
from trace_chan import TraceChan
from receiver import Receiver
from transmitter import Transmitter
from maxtputra import MaxTputRA
from minengra import MinEngRA
from engtputra import EngTputRA
from effsnrra import EffSnrRA
from sampleratera import SampleRate
from rxsamplerate import RxSampleRate
from oraclera import OracleRA
from rxoracle import RxOracle

def main():
    nrx=3
    # Create a tx
    ntx=3
    ta = None
    #ta = SampleRate()
    transmitter = Transmitter(ntx,ta)
    # Create a channel
    
    chan = TraceChan()
    num_chans=1
    length = chan.create_chan(transmitter.Ntx,nrx)

    #ta = OracleRA(chan)
    #transmitter.set_transmit_ra(ta)
    #receiver = Receiver(MaxTputRA(),nrx)
    #receiver = Receiver(MinEngRA(),nrx)
    receiver = Receiver(EngTputRA(),nrx)
    #receiver = Receiver(EffSnrRA(),nrx)
    #receiver = Receiver(RxSampleRate(),nrx)
    #receiver = Receiver(RxOracle(),nrx)

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
