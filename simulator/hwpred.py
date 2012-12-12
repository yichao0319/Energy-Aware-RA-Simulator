#! /usr/bin/env python

import numpy
from numpy  import *
from trace_chan import TraceChan

class HoltsWinter:

    def __init__(self):
        self.a_prev = 0
        self.b_prev = 0
        self.pred = 0
        self.alpha = 0.6
        self.beta = 0.1

    def update(self, new_data):
        new_a = self.alpha * new_data + (1 - self.alpha) * (self.a_prev + self.b_prev);
        new_b = self.beta * (new_a - self.a_prev) + (1 - self.beta) * self.b_prev;
        self.pred = new_a + new_b
        self.a_prev = new_a
        self.b_prev = new_b



def main():

    #####
    ## constant
    PREDICTOR_DEBUG = 0


    #####
    ## variabes
    # filename = "/v/filer4b/v27q002/ut-wireless/yichao/csi_measurement/task01_parse_data/OUTPUT/face.speed3.data.mat"
    # filename = "/v/filer4b/v27q002/ut-wireless/yichao/csi_measurement/task01_parse_data/OUTPUT/card2.6m.data.mat"
    filename = "/v/filer4b/v27q002/ut-wireless/yichao/csi_measurement/task01_parse_data/OUTPUT/l1.dat.mat"
    
    num_sc = 30
    ntx = 3
    nrx = 3
    increment = 1


    #####
    ## initialization
    ## each subcarrier of each steam has one predictor
    hw_preds = []
    # for x in range(1, ntx * nrx * num_sc):
    #     hw_preds.append(HoltsWinter())
    for tx_i in range(0, ntx):
        txp = []
        for rx_i in range(0, nrx):
            rxp = []
            for sc_i in range(0, num_sc): 
                rxp.append(HoltsWinter())
            txp.append(rxp)
        hw_preds.append(txp)
    print "here " + str(len(hw_preds[1][1]))


    #####
    ## holt-winters debug
    if PREDICTOR_DEBUG == 1:
        hw_pred = HoltsWinter()
        for x in xrange(1, 10):
            new_measurement = x * 2 + 1 * 1j
            print "measurement=" + str(new_measurement) + ", pred=" + str(hw_pred.pred) + ", diff=" + str(abs(new_measurement - hw_pred.pred))
            hw_pred.update(new_measurement)


    #####
    ## main start here

    ## read CSI file
    chan = TraceChan(filename, increment)
    num_measurements = chan.create_chan(ntx, nrx)

    for m_i in range(0, num_measurements):
        ## format: [tx, rx, subcarrier]
        chan.get_next_channel()
        Hint = chan.curr_chan
        # print "size=" + str(Hint.shape)

        # for tx_i in range(0, ntx):
        for tx_i in range(0, 1):
            # for rx_i in range(0, nrx):
            for rx_i in range(0, 1):
                # for sc_i in range(0, num_sc):
                for sc_i in range(0, 1):
                    new_measurement = Hint[tx_i, rx_i, sc_i]
                    # print Hint[tx_i, rx_i, sc_i]

                    hw_pred = hw_preds[tx_i][rx_i][sc_i]

                    print "measurement=" + str(new_measurement) + ", pred=" + str(hw_pred.pred) + ", diff=" + str(abs(new_measurement - hw_pred.pred))
                    hw_pred.update(new_measurement)






    # hwpred = HoltsWinter()
    # chan = TraceChan()
    # chan_len = chan.create_chan(3,3)

    # chan.get_next_channel()
    # Hint = chan.curr_chan
    # hwpred.setup_a(Hint)
    # hwpred.setup_b(Hint)

    # Hpred = Hint
    # Hprev = Hint
    # for c in range(0,100):
    #     H = chan.curr_chan
    #     print "pred:"+str(sum(sum(sum(abs(Hpred - H)))))
    #     print "diff:"+str(sum(sum(sum(abs(Hprev - H)))))
    #     Hpred = hwpred.get_next_pred(H)
    #     Hprev = H
    #     chan.get_next_channel()


if __name__ == "__main__":
   main()
