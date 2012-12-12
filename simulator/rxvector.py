#! /usr/bin/env python


class Rxvector:

    def __init__(self):
       self.__Nsts = None
       self.__MCS = None
       self.__STBC = None
       self.__length = None
       self.__BW = None
       self.__mode = None

    Nsts = property(fget=lambda self: self.__Nsts, fset=lambda self,s: self.set_Nsts(s) )
    BW = property(fget=lambda self: self.__BW, fset=lambda self,s: self.set_BW(s) )
    MCS = property(fget=lambda self: self.__MCS, fset=lambda self,s: self.set_MCS(s) )
    STBC = property(fget=lambda self: self.__STBC, fset=lambda self,s: self.set_STBC(s) )
    length = property(fget=lambda self: self.__length, fset=lambda self,s: self.set_length(s) )
    Mode = property(fget=lambda self: self.__mode, fset=lambda self,s: self.set_mode(s) )

    def set_Nsts(self,Nsts): self.__Nsts = Nsts
    def set_MCS(self,MCS): self.__MCS = MCS
    def set_STBC(self,STBC): self.__STBC = STBC
    def set_length(self,length): self.__length = length
    def set_BW(self,BW): self.__BW = BW
    def set_mode(self,mode): self.__mode = mode

