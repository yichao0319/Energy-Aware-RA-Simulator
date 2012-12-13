#! /usr/bin/env python

import os
dir_one_up = os.getcwd().rsplit('/',2)[0]
import sys
sys.path.append(dir_one_up+'/simulator')
from energy import *
from helper_file import *

def calc_per(succ): return (1.0 - 1.0*sum(succ)/len(succ))

def calc_tput(mode,mcs,succ,pktsize):
    data_delivered = 8*pktsize*sum(succ)    # data_delivered in bits
    mapped_mcs = map_to_11n_mcs(mode,mcs)

    index=0; pkts_for_mcs={}
    for mp_mcs in mapped_mcs:
        if mp_mcs not in pkts_for_mcs:
           pkts_for_mcs[mp_mcs]=[]
        pkts_for_mcs[mp_mcs].append(succ[index])
        index = index +1
    mcs_values = pkts_for_mcs.keys()
    total_time=0
    for m in mcs_values:
        pkt_cnt = len(pkts_for_mcs[m])
        Nss = get_nss_from_11n_mcs(m)
        txtime = ((28.0 + 22.0/8)*8.0)/Rates[m%8] + (pktsize*8)/(Rates[m%8]*Nss) + 32.0e-6 + (4.0e-6*Nss) + (9.0e-6*7.5)
        #txtime = ((28.0 + 22.0/8)*8.0)/Rates[m%8] + (pktsize*8)/(Rates[m%8]*Nss) + 32.0e-6 + (4.0e-6*Nss)
        total_time = total_time + (pkt_cnt*txtime)

    tput = 1.0*data_delivered/total_time
    return tput

def calc_energy(mode,mcs,succ,card,trv,pktsize):

    if trv=='tx':
        nant = [get_ntx_from_key(m) for m in mode]
    elif trv=='rx':
        nant = [get_nrx_from_key(m) for m in mode]
    else:
        print "this should never happen"

    nss = [get_nss_from_key(m) for m in mode]
    energyfnc = eval(card+'_'+trv+'_'+'energy')
    energy_vals = [energyfnc(ant,ss,1000,m,0.0) for ant,ss,m in zip(nant,nss,mcs)]
    data_delivered = 8*pktsize*sum(succ)
    if data_delivered == 0:
       return 1.0e6
    else:
       #return 1.0*sum(energy_vals)
       return 1.0*sum(energy_vals)/data_delivered


def eval_protocol(file,card,trv):

    data = parsefile(file)
 
    succ = [line['succ'] for line in data]
    mcs = [line['mcs'] for line in data]   
    mode = [line['mode'] for line in data]   

    pktsize = 1000 #Bytes
    # energy needs to be calculated
    eng_per_bit = calc_energy(mode,mcs,succ,card,trv,pktsize)

    per = calc_per(succ)
    tput = calc_tput(mode,mcs,succ,pktsize)
    return {'tput':tput, 'eng':eng_per_bit}

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

    # chan_type='MobileTrace'
    # chan_type='MobileTrace2'
    chan_type='MobileTrace3'
    # channames = ['facespeed11', 'sidespeed11','facespeed21',\
    #              'facespeed14', 'sidespeed14','facespeed24',\
    #              'facespeed110', 'sidespeed110','facespeed210']
    # channames = ['facespeed11', 'facespeed21', 'facespeed31', 'sidespeed11', 'sidespeed21']
    # channames = ['sender1_lap1_seg11', 'sender1_lap1_seg21', 'sender1_lap1_seg31', 'sender1_lap1_seg41', 'sender1_lap2_seg11', 'sender1_lap2_seg21', 'sender1_lap2_seg31', 'sender1_lap2_seg41', 'sender1_lap3_seg11', 'sender1_lap3_seg21', 'sender1_lap3_seg31', 'sender1_lap3_seg41', 'sender2_lap1_seg11', 'sender2_lap1_seg21', 'sender2_lap1_seg31', 'sender2_lap1_seg41', 'sender2_lap2_seg11', 'sender2_lap2_seg21', 'sender2_lap2_seg31', 'sender2_lap2_seg41', 'sender2_lap3_seg11', 'sender2_lap3_seg21', 'sender2_lap3_seg31', 'sender2_lap3_seg41', 'sender3_lap1_seg11', 'sender3_lap1_seg21', 'sender3_lap1_seg31', 'sender3_lap1_seg41', 'sender3_lap2_seg11', 'sender3_lap2_seg21', 'sender3_lap2_seg31', 'sender3_lap2_seg41', 'sender3_lap3_seg11', 'sender3_lap3_seg21', 'sender3_lap3_seg31', 'sender3_lap3_seg41']
    # channames = ['mob_recv1_run1_01', 'mob_recv2_run1_01', 'mob_recv3_run1_01', 'mob_recv4_run1_01']
    channames = ['sender1_lap1_seg1_mix1', 'sender1_lap1_seg2_mix1', 'sender1_lap1_seg3_mix1']

    #channames = ['static1']
    # protocols=['OracleEffSnr', 'OracleMinEng','OracleMaxTput','SampleRate','OracleEngTput10',\
                # 'OracleEngTput09','OracleEngTput08','OracleEngTput07','OracleEngTput06']
    # protocols =['EffSnr','MaxTput','MinEng','EngTput10','EngTput09','EngTput08','EngTput07','EngTput06']
    # protocols =['EffSnr','MaxTput','MinEng']
    # protocols =['EffSnr','MaxTput','MinEng','EngTput10','EngTput09','EngTput08','EngTput07','EngTput06','EngTput05','EngTput04','EngTput03','EngTput02','EngTput01','SampleRate']
    protocols = ['OracleEffSnr', 'OracleMaxTput', 'OracleMinEng', 'OracleEngTput10', 'OracleEngTput09', 'OracleEngTput08', 'OracleEngTput07', 'OracleEngTput06', 'OracleEngTput05', 'OracleEngTput04', 'OracleEngTput03', 'OracleEngTput02', 'OracleEngTput01']
    card_type=['intel','atheros']
    #card_type=['intel']
    eng_cnstrnt=['tx','rx']
    prediction=['False','True'] #,'False'

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
                                filename = prtcl+refname+'th'+str(et_th)+'_inc'+inc+'.dat'

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
                        processed_file = os.path.join(dir,'ProcessedData',chan,card,c,protocol+pred)+'.dat'
                        pfile = open(processed_file,'w')
                        pfile.write(str(processed_data)+str('\n'))
                        pfile.close()
                        print processed_data


if __name__ == "__main__":
    main()
