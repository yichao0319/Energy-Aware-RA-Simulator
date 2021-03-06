#! /usr/bin/env python

import os
dir_one_up = os.getcwd().rsplit('/',2)[0]
import sys
sys.path.append(dir_one_up+'/simulator')
from energy import *
from helper_file import *

def find_ett_ppr(mod,Nss,plen,ber):

     rate={'BPSK':13.0e6,'QPSK':26.0e6,'QAM16':52.0e6,'QAM64':78.0e6}
     n = get_retx_count(ber) # re-tx count is dependant on ber
     overhead = ((28.0 + 22.0/8)*8.0)/rate[mod] + 32.0e-6 + (4.0e-6*Nss)
     ett =  n*overhead + (plen*8/(rate[mod]*Nss))*(1- ber**n)/(1-ber)

     ett = ett*1e3
     return ett



def calc_tput(mode,modulation,ber,pktsize,recv_data):
    data_delivered = 8*sum(recv_data)   # data_delivered in bits
    rate={'BPSK':13.0e6,'QPSK':26.0e6,'QAM16':52.0e6,'QAM64':78.0e6}

    total_time = 0
    for mod,key in zip(modulation,mode):
        Nss = get_nss_from_key(key)
        #txtime = ((28.0 + 22.0/8)*8.0)/rate[mod] + (pktsize*8)/(rate[mod]*Nss) + 32.0e-6 + (4.0e-6*Nss)
        txtime = ((28.0 + 22.0/8)*8.0)/rate[mod] + (pktsize*8)/(rate[mod]*Nss) + 32.0e-6 + (4.0e-6*Nss) + (9.0e-6*7.5)
        total_time = total_time + txtime
    tput = 1.0*data_delivered/total_time
    return tput

def calc_energy(mode,modulation,ber,card,trv,pktsize,recv_data):

    if trv=='tx':
        nant = [get_ntx_from_key(m) for m in mode]
    elif trv=='rx':
        nant = [get_nrx_from_key(m) for m in mode]
    elif trv == 'tx_rx':
        nant = [(get_ntx_from_key(m),get_nrx_from_key(m)) for m in mode]
    else:
        print "this should never happen"
    nss = [get_nss_from_key(m) for m in mode]
    energyfnc = eval(card+'_'+trv+'_'+'energy_ppr')
    energy_vals = [energyfnc(ant,ss,1000,m,b) for ant,ss,m,b in zip(nant,nss,modulation,ber)]
    data_delivered = 8*sum(recv_data)
    if data_delivered == 0:
       return 1.0e6
    else:
       #return 1.0*sum(energy_vals)
       return 1.0*sum(energy_vals)/data_delivered


MODULATION=['BPSK','QPSK','QPSK','QAM16','QAM16','QAM64','QAM64','QAM64']
def mcs2mod(mcs): return MODULATION[mcs%8]

def eval_protocol(file,card,trv):

    data = parsefile(file)

    recv_data = [line['data'] for line in data]
    mcs = [line['mcs'] for line in data]   
    mode = [line['mode'] for line in data]   
    modulation=[mcs2mod(m) for m in mcs]

    pktsize = 1000 #Bytes
    ber=[1.0 - (rdata/pktsize) for rdata in recv_data]
    tput = calc_tput(mode,modulation,ber,pktsize,recv_data)

    # energy needs to be calculated
    # eng_per_bit = calc_energy(mode,modulation,ber,card,trv,pktsize,recv_data)
    # return {'tput':tput, 'eng':eng_per_bit}
    eng_per_bit_rx = calc_energy(mode, modulation, ber, card, 'rx', pktsize, recv_data)
    eng_per_bit_tx = calc_energy(mode, modulation, ber, card, 'tx', pktsize, recv_data)
    eng_per_bit_sum = eng_per_bit_rx + eng_per_bit_tx

    return {'tput':tput, 'eng':eng_per_bit_sum, 'eng_rx': eng_per_bit_rx, 'eng_tx': eng_per_bit_tx}


def get_file_data(path,filename,card,trv):

    try:
       #print filename
       f = open(path+filename,'r')
       data = eval_protocol(f,card, trv)
       f.close()
    except IOError as e:
       print "Error: "+str(e)
    return data


def main():
    curr_dir = os.getcwd()
    curr_dir_d1 = curr_dir.rsplit('/',1)
    dir = curr_dir_d1[0]

    # chan_type='PPRMobileTrace'
    # chan_type='PPRMobileTrace2'
    chan_type='PPRMobileTrace3'
    # channames = ['facespeed11', 'sidespeed11','facespeed21',\
    #              'facespeed14', 'sidespeed14','facespeed24',\
    #              'facespeed110', 'sidespeed110','facespeed210']
    # channames = ['facespeed11', 'facespeed21', 'facespeed31', 'sidespeed11', 'sidespeed21']
    # channames = ['sender1_lap1_seg11', 'sender1_lap1_seg21', 'sender1_lap1_seg31', 'sender1_lap1_seg41', 'sender1_lap2_seg11', 'sender1_lap2_seg21', 'sender1_lap2_seg31', 'sender1_lap2_seg41', 'sender1_lap3_seg11', 'sender1_lap3_seg21', 'sender1_lap3_seg31', 'sender1_lap3_seg41', 'sender2_lap1_seg11', 'sender2_lap1_seg21', 'sender2_lap1_seg31', 'sender2_lap1_seg41', 'sender2_lap2_seg11', 'sender2_lap2_seg21', 'sender2_lap2_seg31', 'sender2_lap2_seg41', 'sender2_lap3_seg11', 'sender2_lap3_seg21', 'sender2_lap3_seg31', 'sender2_lap3_seg41', 'sender3_lap1_seg11', 'sender3_lap1_seg21', 'sender3_lap1_seg31', 'sender3_lap1_seg41', 'sender3_lap2_seg11', 'sender3_lap2_seg21', 'sender3_lap2_seg31', 'sender3_lap2_seg41', 'sender3_lap3_seg11', 'sender3_lap3_seg21', 'sender3_lap3_seg31', 'sender3_lap3_seg41']
    # channames = ['mob_recv1_run1_01', 'mob_recv2_run1_01', 'mob_recv3_run1_01', 'mob_recv4_run1_01']
    channames = ['sender1_lap1_seg1_mix1', 'sender1_lap1_seg2_mix1', 'sender1_lap1_seg3_mix1']

    protocols =['PPrMaxTput','PPrMinEng','PPrEngTput10','PPrEngTput09','PPrEngTput08','PPrEngTput07','PPrEngTput06','PPrEngTput05','PPrEngTput04','PPrEngTput03','PPrEngTput02','PPrEngTput01']
    # protocols = ['OraclePPrMaxTput', 'OraclePPrMinEng','OraclePPrEngTput10','OraclePPrEngTput09','OraclePPrEngTput08','OraclePPrEngTput07','OraclePPrEngTput06','OraclePPrEngTput05','OraclePPrEngTput04','OraclePPrEngTput03','OraclePPrEngTput02','OraclePPrEngTput01']
    card_type=['intel','atheros']
    eng_cnstrnt=['tx', 'rx', 'tx_rx']
    prediction = ['False', 'True']  # ,'False'

    finaldata={}
    trace_path = dir+'/Data/'+chan_type+'/'
    for chan in channames:
        for protocol in protocols:
            for card in card_type:
                for c in eng_cnstrnt:
                    for pred in prediction:
                        # if 'facespeed1' in chan: lchan = 'facespeed1'
                        # elif 'facespeed2' in chan: lchan = 'facespeed2'
                        # elif 'facespeed3' in chan: lchan = 'facespeed3'
                        # elif 'sidespeed1' in chan: lchan = 'sidespeed1'
                        # elif 'sidespeed2' in chan: lchan = 'sidespeed2'
                        lchan = chan[:-1]

                        refname = '_'+lchan+'_'+card+'_'+c+'_pred'+pred
                        # if 'facespeed2' in chan:
                        #     inc = chan.split('2',1)[1]
                        # else:
                        #     inc = chan.split('1',1)[1]
                        inc = '1'


                        if 'EngTput' in protocol:
                            et_th = th_map(protocol)
                            prtcl = protocol[:-2]

                            if 'Oracle' in protocol:
                                if pred == 'True':
                                    continue

                                filename = 'RxOracle_' + prtcl + refname + 'th' + str(et_th) + '_inc1.dat'

                            else:
                                # filename = 'RxOracle_'+prtcl+refname+'th'+str(et_th)+'_inc'+inc+'.dat'
                                filename = prtcl + refname + 'th' + str(et_th) + '_inc1.dat'

                        elif protocol == 'SampleRate':
                            filename = protocol+refname+'_inc'+inc+'.dat'

                        elif 'Oracle' in protocol:
                            if pred == 'True':
                                continue

                            filename = 'RxOracle_' + protocol + refname + '_inc1.dat'

                        else:
                            # filename = 'RxOracle_'+protocol+refname+'_inc'+inc+'.dat'
                            filename = protocol+refname+'_inc'+inc+'.dat'

                        print filename
                        processed_data=get_file_data(trace_path,filename,card,c)
                        processed_file = os.path.join(dir,'PPrProcessedData',chan,card,c,protocol+pred)+'.dat'
                        print processed_file
                        pfile = open(processed_file,'w')
                        pfile.write(str(processed_data)+str('\n'))
                        pfile.close()
                        print processed_data


if __name__ == "__main__":
    main()
