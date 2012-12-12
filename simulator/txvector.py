#! /usr/bin/env python


class Txvector:

    def __init__(self):
       self.__Nsts = None
       self.__Nss = None
       self.__MCS = None
       self.__BW = None
       self.__STBC = None
       self.__length = None
       self.__Ntx= None
       self.__mode = None

    Nsts = property(fget=lambda self: self.__Nsts, fset=lambda self,s: self.set_Nsts(s) )
    BW = property(fget=lambda self: self.__BW, fset=lambda self,s: self.set_BW(s) )
    MCS = property(fget=lambda self: self.__MCS, fset=lambda self,s: self.set_MCS(s) )
    STBC = property(fget=lambda self: self.__STBC, fset=lambda self,s: self.set_STBC(s) )
    length = property(fget=lambda self: self.__length, fset=lambda self,s: self.set_length(s) )
    Ntx = property(fget=lambda self: self.__Ntx, fset=lambda self,s: self.set_Ntx(s) )
    Mode = property(fget=lambda self: self.__mode, fset=lambda self,s: self.set_mode(s) )

    Nss = property(fget=lambda self: self.__Nss)

    def set_BW(self,BW): self.__BW = BW
    def set_MCS(self,MCS): self.__MCS = MCS
    def set_length(self,length): self.__length = length
    def set_Ntx(self,Ntx): self.__Ntx = Ntx
    def set_mode(self,mode): self.__mode = mode

    def set_Nsts(self,Nsts): 
        self.__Nsts = Nsts
        self.calc_Nss()

    def set_STBC(self,STBC): 
        self.__STBC = STBC
        self.calc_Nss()


    def calc_Nss(self): self.__Nss = Nsts - STBC

