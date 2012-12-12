#! /usr/bin/env python
import os
dir_one_up = os.getcwd().rsplit('/',1)[0]
import sys
sys.path.append(dir_one_up+'/common')
