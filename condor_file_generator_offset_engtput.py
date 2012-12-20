# /usr/bin/env python

import os

def generate_file(count,scheme,fchan_name,card_type,constraint,pred,thresh, increment):

    file = open("auto_gen_"+str(scheme)+"_"+str(fchan_name)+"_"+str(card_type)+str(constraint)+str(pred)+str(thresh)+str(increment)+".cnd","w")
    print file
    file.write("+Group = \"GRAD\"\n")
    file.write("+Project = \"NETWORKING_MULTIMEDIA\"\n")
    file.write("+ProjectDescription = \"simulation of network performance with CSI on each subcarrier\"\n\n")

    file.write("Universe = vanilla\n\n")
 
    file.write("executable = /lusr/bin/python\n")
    file.write("arguments = \"simulator/simulate_"+str(scheme)+".py ChanTraces/"+str(fchan_name)+" "+str(card_type)+" "+str(constraint)+" "+str(pred)+" "+str(thresh)+" "+str(increment)+"\"\n")
    file.write("Requirements = Memory >= 64\n")
    file.write("Rank = Memory >= 128\n\n")

    file.write("Error = err/err."+str(scheme)+"_"+str(fchan_name)+"_"+str(card_type)+str(constraint)+str(pred)+str(thresh)+str(increment)+"\n")
    file.write("Output = out/out."+str(scheme)+"_"+str(fchan_name)+"_"+str(card_type)+str(constraint)+str(pred)+str(thresh)+str(increment)+"\n")
    file.write("Log = log/log."+str(scheme)+"_"+str(fchan_name)+"_"+str(card_type)+str(constraint)+str(pred)+str(thresh)+str(increment)+"\n\n")

#    file.write("Error = err/"+str(scheme)+"/err."+str(scheme)+"_"+str(fchan_name)+"_"+str(card_type)+str(constraint)+str(pred)+str(thresh)+"\n")
#    file.write("Output = out/"+str(scheme)+"/out."+str(scheme)+"_"+str(fchan_name)+"_"+str(card_type)+str(constraint)+str(pred)+str(thresh)+"\n")
#    file.write("Log = log/"+str(scheme)+"/log."+str(scheme)+"_"+str(fchan_name)+"_"+str(card_type)+str(constraint)+str(pred)+str(thresh)+"\n\n")

    file.write("Queue 1")
    file.close()


def main():

    curdir = os.getcwd()
    # list_items = os.listdir(curdir+"/ChanTraces")
    # list_items = ['static1.mat', 'static2.mat', 'static3.mat', 'facespeed1.mat', 'facespeed2.mat', 'facespeed3.mat', 'sidespeed1.mat', 'sidespeed2.mat']
    # list_items = ['sender1_lap1_seg1.mat', 'sender1_lap1_seg2.mat', 'sender1_lap1_seg3.mat', 'sender1_lap1_seg4.mat', 'sender1_lap2_seg1.mat', 'sender1_lap2_seg2.mat', 'sender1_lap2_seg3.mat', 'sender1_lap2_seg4.mat', 'sender1_lap3_seg1.mat', 'sender1_lap3_seg2.mat', 'sender1_lap3_seg3.mat', 'sender1_lap3_seg4.mat', 'sender2_lap1_seg1.mat', 'sender2_lap1_seg2.mat', 'sender2_lap1_seg3.mat', 'sender2_lap1_seg4.mat', 'sender2_lap2_seg1.mat', 'sender2_lap2_seg2.mat', 'sender2_lap2_seg3.mat', 'sender2_lap2_seg4.mat', 'sender2_lap3_seg1.mat', 'sender2_lap3_seg2.mat', 'sender2_lap3_seg3.mat', 'sender2_lap3_seg4.mat', 'sender3_lap1_seg1.mat', 'sender3_lap1_seg2.mat', 'sender3_lap1_seg3.mat', 'sender3_lap1_seg4.mat', 'sender3_lap2_seg1.mat', 'sender3_lap2_seg2.mat', 'sender3_lap2_seg3.mat', 'sender3_lap2_seg4.mat', 'sender3_lap3_seg1.mat', 'sender3_lap3_seg2.mat', 'sender3_lap3_seg3.mat', 'sender3_lap3_seg4.mat']
    # list_items = ['mob_recv1_run1_0.mat', 'mob_recv2_run1_0.mat', 'mob_recv3_run1_0.mat', 'mob_recv4_run1_0.mat']
    list_items = ['sender1_lap1_seg1_mix.mat', 'sender1_lap1_seg2_mix.mat', 'sender1_lap1_seg3_mix.mat', 'static_sender2_3tx_run1.mat', 'static_sender2_3tx_run2.mat', 'static_sender2_3tx_run3.mat']


    pred = ['True', 'False']
    # pred= ['False']
    # scheme = ["mineng", "maxtput", "engtput", "effsnr", "samplerate", "oracle"]
    # scheme = ["oracle_pprengtput"]
    # scheme = ["engtput"]
    scheme = ["engtput", "pprengtput"]
    # scheme = ["oracle_engtput", "oracle_pprengtput"]
    card_types = ["intel", "atheros"]
    constraint =["tx", "rx", "tx_rx"]
    thresholds =[1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
    #increment = [1, 4, 10]
    increment = [1]

    for s in scheme:
        for i,l in zip(range(0,len(list_items)),list_items):
            for t in card_types:
                for c in constraint:
                    for p in pred:
                        for ths in thresholds:
                            for inc in increment:
                                generate_file(i,s,l,t,c,p,ths,inc)


if __name__ =="__main__":
   main()
