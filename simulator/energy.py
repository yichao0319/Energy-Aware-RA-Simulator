#! /usr/bin/env python

from helper import *

def old_find_ett(mcs,Nss,plen):
    Nsub=52
    BpS = Nsub*mcs2nbpsc(mcs)*Nss/8.0
    num_ofdm_sym = 1.0*plen/BpS
    return 4.0e-6*num_ofdm_sym

def find_ett(mcs,Nss,plen,per):

     rate = [6.5e6, 13.0e6, 19.5e6, 26.0e6, 39.0e6, 52.0e6, 58.5e6, 65.0e6]
     #rate = [6.0e6, 12.0e6, 18.0e6, 24.0e6, 36.0e6, 48.0e6, 54.0e6, 60.0e6]
     ett = ((28.0 + 22.0/8)*8.0)/rate[mcs] + (plen*8)/(rate[mcs]*Nss) + 32.0e-6 + (4.0e-6*Nss)

     per = per - 1.0e-6
     #ett = ett*1e3/(1.0 - per)
     ett = ett*1e3
     return ett

# the energy being computed is for 1000 pkts

def intel_tx_energy(ntx,Nss,plen,mcs,per):
    ett = find_ett(mcs,Nss,plen,per)
    stbc = ntx - Nss
    if ntx > 1: mimo = 1
    else: mimo = 0 
    est_energy = (0.24*ntx + 0.425*mimo + 1.02 )*ett + (0.045*ntx + 0.108)
    #est_energy = (0.062*ntx + 0.65*Nss + 0.51)*ett + (0.05*ntx + 0.103)
    return est_energy

def intel_rx_energy(nrx,Nss,plen,mcs,per):

    ett = find_ett(mcs,Nss,plen,per)
    est_energy = (0.30*nrx + 0.61)*ett + (0.064*nrx + 0.167) 
    return est_energy

def intel_tx_rx_energy(nant,Nss,plen,mcs,per):

    ntx = nant[0]
    nrx = nant[1]
    energy_tx = intel_tx_energy(ntx,Nss,plen,mcs,per)
    energy_rx = intel_rx_energy(nrx,Nss,plen,mcs,per)

    est_energy = energy_tx + energy_rx
    return est_energy


def atheros_tx_energy(ntx,Nss,plen,mcs,per):

    ett = find_ett(mcs,Nss,plen,per)
    stbc = ntx - Nss
    est_energy = (0.38*ntx + 0.108)*ett + (0.04*ntx + 0.062)
    return est_energy

def atheros_rx_energy(nrx,Nss,plen,mcs,per):

    ett = find_ett(mcs,Nss,plen,per)
    est_energy  =( 0.142*nrx + 0.30)*ett + ( 0.048*nrx + 0.106) 
    return est_energy

def atheros_tx_rx_energy(nant,Nss,plen,mcs,per):

    ntx = nant[0]
    nrx = nant[1]
    energy_tx = atheros_tx_energy(ntx,Nss,plen,mcs,per)
    energy_rx = atheros_rx_energy(nrx,Nss,plen,mcs,per)

    est_energy = energy_tx + energy_rx
    return est_energy




def find_ett_ppr(mod,Nss,plen,ber):

     rate={'BPSK':13.0e6,'QPSK':26.0e6,'QAM16':52.0e6,'QAM64':78.0e6}
     n = get_retx_count(ber) # re-tx count is dependant on ber
     overhead = ((28.0 + 22.0/8)*8.0)/rate[mod] + 32.0e-6 + (4.0e-6*Nss)
     ett =  n*overhead + (plen*8/(rate[mod]*Nss))*(1- ber**n)/(1-ber)

     ett = ett*1e3
     return ett


def intel_tx_energy_ppr(ntx,Nss,plen,mcs,ber):
    ett = find_ett_ppr(mcs,Nss,plen,ber)

    if ntx > 1: mimo = 1
    else: mimo = 0 
    est_energy = (0.24*ntx + 0.425*mimo + 1.02 )*ett + (0.045*ntx + 0.108)
    #est_energy = (0.062*ntx + 0.65*Nss + 0.51)*ett + (0.05*ntx + 0.103)
    return est_energy

def intel_rx_energy_ppr(nrx,Nss,plen,mcs,ber):

    ett = find_ett_ppr(mcs,Nss,plen,ber)
    est_energy = (0.30*nrx + 0.61)*ett + (0.064*nrx + 0.167) 
    return est_energy

def intel_tx_rx_energy_ppr(nant,Nss,plen,mcs,ber):

    ntx = nant[0]
    nrx = nant[1]
    energy_tx = intel_tx_energy_ppr(ntx,Nss,plen,mcs,ber)
    energy_rx = intel_rx_energy_ppr(nrx,Nss,plen,mcs,ber)

    est_energy = energy_tx + energy_rx
    return est_energy

def atheros_tx_energy_ppr(ntx,Nss,plen,mcs,ber):

    ett = find_ett_ppr(mcs,Nss,plen,ber)
    est_energy = (0.38*ntx + 0.108)*ett + (0.04*ntx + 0.062)
    return est_energy

def atheros_rx_energy_ppr(nrx,Nss,plen,mcs,ber):

    ett = find_ett_ppr(mcs,Nss,plen,ber)
    est_energy  =( 0.142*nrx + 0.30)*ett + ( 0.048*nrx + 0.106) 
    return est_energy


def atheros_tx_rx_energy_ppr(nant,Nss,plen,mcs,ber):

    ntx = nant[0]
    nrx = nant[1]
    energy_tx = atheros_tx_energy_ppr(ntx,Nss,plen,mcs,ber)
    energy_rx = atheros_rx_energy_ppr(nrx,Nss,plen,mcs,ber)

    est_energy = energy_tx + energy_rx
    return est_energy



def simple_test():

# 1 ant at 13Mbps, pkt len 750Bytes
  energy1= rx_energy(1,1,750,1)
  print "energy1: "+str(energy1)

# 3 ants at 6.5Mbps, pkt len 750Bytes

  energy3= rx_energy(3,2,750,0)
  print "energy3: "+str(energy3)


def main():
    simple_test()


if __name__=="__main__":
   main()
