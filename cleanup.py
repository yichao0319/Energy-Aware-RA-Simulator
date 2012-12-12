#! /usr/bin/env python

# The file deletes the followings files:
# 1) *.dat files in Trace folder.
# 2) err.* files in err folder.
# 3) out.* files in out folder.
# 4) log.* files in log folder.


import os

Trace = True
Err = True
Log = True
Out = True
Cnd = True

def main():

    curr_dir = os.getcwd()

    if Trace == True:
        trace_cmd = 'rm '+str(curr_dir)+'/Trace/*.dat'
        try:
            os.system(trace_cmd)
            print "Trace files deleted"   
        except:
            print "Trace files not deleted"

    if Err == True:
        err_cmd = 'rm '+str(curr_dir)+'/err/err.*'
        try:
            os.system(err_cmd)
            print "err files deleted"   
        except:
            print "err files not deleted"

    if Out == True:
        out_cmd = 'rm '+str(curr_dir)+'/out/out.*'
        try:
            os.system(out_cmd)
            print "out files deleted"   
        except:
            print "out files not deleted"

    if Log == True:
        log_cmd = 'rm '+str(curr_dir)+'/log/log.*'
        try:
            os.system(log_cmd)
            print "log files deleted"   
        except:
            print "log files not deleted"

    if Cnd == True:
        cnd_cmd = 'rm '+str(curr_dir)+'/*.cnd'
        try:
            os.system(cnd_cmd)
            print "cnt files deleted"   
        except:
            print "cnt files not deleted"



if __name__ == "__main__":
    main()
