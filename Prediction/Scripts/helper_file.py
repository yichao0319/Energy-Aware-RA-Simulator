#! /usr/bin/env python

import ast

##VARIABLES
Rates = [6.5e6, 13.0e6, 19.5e6, 26.0e6, 39.0e6, 52.0e6, 58.5e6, 65.0e6]

##METHODS
def parsefile(file):
    data=[]
    for line in file:
        data.append(ast.literal_eval(line))
    return data


def get_nss_from_key(key):
    k = key.split()
    newkey = k[0]+' '+k[1]
    table={'sm 1by1':1, 'sm 1by2':1, 'sm 1by3':1,'sm 2by2':2, 'sm 2by3':2, 'sm 3by3':3, 'map 2by1':1, 'map 2by2':1, 'map 3by1':1, 'map 3by2':2, 'map 3by3':1}
    return table[newkey] 


def get_nss_from_11n_mcs(mcs): return ((mcs/8)+1)


def map_to_11n_mcs(Mode,Mcs):
    return [mcs + (get_nss_from_key(mode)-1)*8 for mode,mcs in zip(Mode,Mcs)]

def get_nrx_from_key(key):
    k = key.split()
    newkey = k[0]+' '+k[1]
    table={'sm 1by1':1, 'sm 1by2':2, 'sm 1by3':3,'sm 2by2':2, 'sm 2by3':3, 'sm 3by3':3, 'map 2by1':1, 'map 2by2':2, 'map 3by1':1, 'map 3by2':2, 'map 3by3':3}
    return table[newkey] 

def get_ntx_from_key(key):
    k = key.split()
    newkey = k[0]+' '+k[1]
    table={'sm 1by1':1, 'sm 1by2':1, 'sm 1by3':1,'sm 2by2':2, 'sm 2by3':2, 'sm 3by3':3, 'map 2by1':2, 'map 2by2':2, 'map 3by1':3, 'map 3by2':3, 'map 3by3':3}
    return table[newkey] 

def th_map(protocol):

    table={'10':'1.0', '09':'0.9', '08':'0.8', '07':'0.7', '06':'0.6', '05':'0.5', '04':'0.4', '03':'0.3', '02':'0.2', '01':'0.1'}
    if 'EngTput' not in protocol:
        print "Error. This method should not be called.\n\n\n\n\n\n\n"

    key = protocol[-2:]
    return table[key]
