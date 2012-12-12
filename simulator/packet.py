#! /usr/bin/env python


class Packet:

    def __init__(self):
        self.__length = None
        self.__MCS = None
        self.__STBC = None
        self.__CBW = None
        self.__ChanMag = None
        self.__txpower = None
        self.__rxpower = None
        self.__ntx= None
        self.__nrx= None
        self.__noise= None
        self.__mode= None
        self.__succ = None

    CBW = property(fget=lambda self: self.__CBW, fset=lambda self,s: self.set_CBW(s) )
    MCS = property(fget=lambda self: self.__MCS, fset=lambda self,s: self.set_MCS(s) )
    STBC = property(fget=lambda self: self.__STBC, fset=lambda self,s: self.set_STBC(s) )
    length = property(fget=lambda self: self.__length, fset=lambda self,s: self.set_length(s) )
    TxPwr = property(fget=lambda self: self.__txpower, fset=lambda self,s: self.set_txpower(s) )
    ChanMag = property(fget=lambda self: self.__ChanMag, fset=lambda self,s: self.set_chan_mag(s))
     
    RxPwr = property(fget=lambda self: self.__rxpower, fset=lambda self,s: self.set_rxpower(s) )
    Ntx = property(fget=lambda self: self.__ntx, fset=lambda self,s: self.set_ntx(s) )
    Nrx = property(fget=lambda self: self.__nrx, fset=lambda self,s: self.set_nrx(s) )
    Noise = property(fget=lambda self: self.__noise, fset=lambda self,s: self.set_noise(s) )
    Mode = property(fget=lambda self: self.__mode, fset=lambda self,s: self.set_mode(s) )
    
    succ = property(fget=lambda self: self.__succ, fset=lambda self,s: self.set_succ(s) )

    def set_CBW(self,CBW): self.__CBW = CBW
    def set_MCS(self,MCS): self.__MCS = MCS
    def set_length(self,length): self.__length = length
    def set_STBC(self,STBC): self.__STBC = STBC
    def set_txpower(self,txpower): self.__txpower = txpower
    def set_rxpower(self,rxpower): self.__rxpower = rxpower
    def set_ntx(self,ntx): self.__ntx = ntx
    def set_nrx(self,nrx): self.__nrx = nrx
    def set_noise(self,noise): self.__noise = noise
    def set_mode(self,mode): self.__mode = mode
    def set_succ(self,succ): self.__succ = succ

    def set_chan_mag(self,chan): self.__ChanMag = chan

    def __str__(self):
        vals={'CBW':self.CBW, 'MCS':self.MCS, 'STBC':self.STBC, 'TxPwr':self.TxPwr, 'length':self.length,'ChanMag':self.ChanMag,'RxPwr':self.RxPwr,'mode':self.Mode, 'ntx':self.Ntx, 'nrx':self.Nrx}
        vals={'CBW':self.CBW, 'MCS':self.MCS, 'STBC':self.STBC, 'TxPwr':self.TxPwr, 'length':self.length,'RxPwr':self.RxPwr,'mode':self.Mode, 'ntx':self.Ntx, 'nrx':self.Nrx}
        return str(vals)
        

