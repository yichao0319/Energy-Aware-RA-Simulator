#! /usr/bin/env python


class Feedback:

    def __init__(self):
        self.__mode = None
        self.__mcs = None
        self.__succ = None
        self.__plen = None

    mode = property(fget=lambda self: self.__mode, fset=lambda self,s: self.set_mode(s) )
    mcs = property(fget=lambda self: self.__mcs, fset=lambda self,s: self.set_mcs(s) )
    succ = property(fget=lambda self: self.__succ, fset=lambda self,s: self.set_succ(s) )
    plen = property(fget=lambda self: self.__plen, fset=lambda self,s: self.set_plen(s) )


    def set_mode(self,mode): self.__mode = mode
    def set_mcs(self,mcs): self.__mcs = mcs
    def set_succ(self,succ): self.__succ = succ
    def set_plen(self,plen): self.__plen = plen
