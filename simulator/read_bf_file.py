#! /usr/bin/env python
import socket
import struct
import numpy
from helper import *
from scipy import io

def process_data(filename):

    file = open(filename,'rb')
    byte = file.read(2)
    # unpack conventions
    # ! indicates network i.e. big-endian
    # H indicates unsigned short
    # [0] is at the end because upack returns a tuple
    val = struct.unpack('!H',byte)[0]
    #print val
    i=1
    all_scaled_csi=[]
    print "Beginning to read from csi data file"
    print "Please be patient as it can take time"
    while 1:
        #print i
        bfee = read_csi(file)
        all_scaled_csi.append(get_scaled_csi(bfee))
        exread = file.read(2)
        if len(exread)==0:
            break
        #print 'exread value: %d'%(struct.unpack('!H',exread)[0])
        i = i+1
    file.close()

    print "Done reading csi data"
    L = len(all_scaled_csi)
    S=30; M=3; N=3;
    mat_chan = numpy.zeros((L,M,N,S))*1.0j
    for l in range(0,L):
        mat_chan[l,:,:,:] = all_scaled_csi[l]
    write_dict={'CSI': mat_chan}
    return write_dict
    #io.savemat('mobile_face1',write_dict)

def read_csi(file):

    fieldnames = ('timestamp_low', 'bfee_count','reserved', 'Nrx', 'Ntx', 'rssi_a', 'rssi_b', 'rssi_c', 'noise','agc', 'antenna_sel', 'len', 'fake_rate_n_flags')
    try:
        code = file.read(1)
        if struct.unpack('B',code)[0] == 187:
            data = file.read(20)
            values = struct.unpack('LHHBBBBBbBBHH',data)
            bfee = dict (zip(fieldnames,values))
            Nrx = bfee['Nrx']
            Ntx = bfee['Ntx']
            data_len = (30*(Nrx*Ntx*8*2 +3)+7)/8
            raw_csi = file.read(data_len)

            index = 0
            chan = numpy.zeros((Ntx,Nrx,30))*1.0j
            for count in range(0,30):
                index = index + 3
                remainder = index % 8
                for nrx in range(0,Nrx):
                    for ntx in range(0,Ntx):
                        index0  = struct.unpack('B',raw_csi[index/8])[0]
                        index1  = struct.unpack('B',raw_csi[index/8 +1])[0]
                        index2  = struct.unpack('B',raw_csi[index/8 +2])[0]
                        unsgn_real = index0>>remainder | index1<<(8-remainder) & 0xFF
                        unsgn_imag = index1>>remainder | index2<<(8-remainder) & 0xFF
                        if ~0x7f&unsgn_real != 0: real = -1*((~unsgn_real+1)&0xff)
                        else: real = 0x7f&unsgn_real
                        if ~0x7f&unsgn_imag != 0: imag = -1*((~unsgn_imag+1)&0xff)
                        else: imag = 0x7f&unsgn_imag
                        chan[ntx,nrx,count]= numpy.complex(real,imag)
                        index = index + 16
            bfee['csi'] = chan
            #print "Ntx: "+str(bfee['Ntx'])
    except EOFError:
        print "Reached end of file"

    return bfee

def get_total_rss(bfee):

    # Careful here: rssis could be zero
    rssi_mag = 0;
    if bfee['rssi_a'] != 0:
        rssi_mag = rssi_mag + db2linear(bfee['rssi_a']);

    if bfee['rssi_b'] != 0:
        rssi_mag = rssi_mag + db2linear(bfee['rssi_b']);

    if bfee['rssi_c'] != 0:
        rssi_mag = rssi_mag + db2linear(bfee['rssi_c']);
    
    ret = linear2db(rssi_mag) - 44 - bfee['agc'];

    return ret

def get_scaled_csi(bfee):

    csi = bfee['csi']
    # Calculate the scale factor between normalized CSI and RSSI (mW)
    csi_sq = csi * csi.conj()
    csi_pwr = sum(csi_sq[:])
    rssi_pwr = db2linear(get_total_rss(bfee))
    #   Scale CSI -> Signal power : rssi_pwr / (mean of csi_pwr)
    scale = rssi_pwr / (csi_pwr / 30);

    # Thermal noise might be undefined if the trace was
    # captured in monitor mode.
    # ... If so, set it to -92
    if (bfee['noise'] == -127): noise_db = -92
    else: noise_db = bfee['noise']

    thermal_noise_pwr = db2linear(noise_db)
    
    # Quantization error: the coefficients in the matrices are
    # 8-bit signed numbers, max 127/-128 to min 0/1. Given that Intel
    # only uses a 6-bit ADC, I expect every entry to be off by about
    # +/- 1 (total across real & complex parts) per entry.
    #
    # The total power is then 1^2 = 1 per entry, and there are
    # Nrx*Ntx entries per carrier. We only want one carrier's worth of
    # error, since we only computed one carrier's worth of signal above.
    quant_error_pwr = scale * (bfee['Nrx'] * bfee['Ntx'])

    # Total noise and error power
    total_noise_pwr = thermal_noise_pwr + quant_error_pwr

    # Ret now has units of sqrt(SNR) just like H in textbooks
    ret = csi * numpy.sqrt(scale / total_noise_pwr)
    if bfee['Ntx'] == 2: ret = ret * numpy.sqrt(2)
    elif bfee['Ntx'] == 3:
        # Note: this should be sqrt(3)~ 4.77 dB. But, 4.5 dB is how
        # Intel (and some other chip makers) approximate a factor of 3
        #
        # You may need to change this if your card does the right thing.
        ret = ret * numpy.sqrt(db2linear(4.5))

    return ret

def main():

    #bfee = read_csi('tmp.dat') 
    bfee = process_data('mobile_trace/face.speed1.data') 
    #bfee = process_data('tmp.dat') 
    #print scaled_csi

if __name__=="__main__":
    main()
