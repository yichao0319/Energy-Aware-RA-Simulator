# !/usr/bin/env python

from scipy import io
from read_bf_file import *
class TraceChan:

    def __init__(self,file=None,inc=1,id=0):
        self.id = id
        self.chan_trace = None
        self.curr_loc = -1
        self.curr_chan = None
        self.delay= 0
	self.incr = inc
        self.type = None
        if file is None:
           self.file = 'csi_trace.mat'
        else:
           self.file = file

    def create_chan(self,ntx,nrx):
        #file='csi_trace.mat'
        #file='tracetx3.mat'
        chan_length = self.read_trace(self.file)
        chan_length = chan_length/self.incr
        return chan_length

    def read_trace(self,file):
        self.type = file.split('.')[-1]
        if self.type == 'mat': data = io.loadmat(file)
        elif self.type == 'dat': data = process_data(file)
        else: assert False, " Only mat and dat options are valid"


        if 'csi' in data: self.chan_trace = data['csi']
        elif 'CSI' in data:self.chan_trace = data['CSI']
        else: assert False, " Trace file doesnot have a valid csi/CSI key"
        print self.chan_trace.shape
        [C,M,N,S] = self.chan_trace.shape
        return C

    def peek_next_channel(self):
        if self.delay+1==1:
           return self.chan_trace[self.curr_loc + self.incr]
        else:
           return self.chan_trace[self.curr_loc]

    def get_next_channel(self):
        self.delay = self.delay + 1
        if self.delay == 1:
           self.curr_loc = self.curr_loc + self.incr
           self.delay = 0
        self.curr_chan = self.chan_trace[self.curr_loc]

    def apply_channel(self,pkt):
        self.get_next_channel()
        pkt.ChanMag = self.curr_chan
