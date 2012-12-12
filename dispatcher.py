#! /usr/bin/env python

import os

def main():

    curr_dir = os.getcwd()
    dir_list = os.listdir(curr_dir)
    cnd_list=[]

    for dl in dir_list:
        dl_split = dl.split('.')
        if dl_split[-1] == 'cnd':
           cnd_list.append(dl)

    for cnd in cnd_list:
        cmd ='condor_submit '+str(cnd)
        print cmd
        os.system(cmd)

if __name__ == "__main__":
   main()
