#!/usr/bin/python
#-----------------------------------------------------------------------------
# File       : configure.py
# Created    : 2020-01-22
# Last update: 2020-01-22
#-----------------------------------------------------------------------------
# Description: 
#-----------------------------------------------------------------------------
# This file is part of the 'atca-timing-fanout-init'. It is subject to 
# the license terms in the LICENSE.txt file found in the top-level directory 
# of this distribution and at: 
#    https://confluence.slac.stanford.edu/display/ppareg/LICENSE.html. 
# No part of the 'atca-timing-fanout-init', including this file, may be 
# copied, modified, propagated, or distributed except according to the terms 
# contained in the LICENSE.txt file.
#-----------------------------------------------------------------------------

#import sys
import os
#import re
#import collections
#import string
import subprocess
#import commands
import argparse
import time

# Set the argument parser
parser = argparse.ArgumentParser()

# Add arguments

parser.add_argument(
    "--shm", 
    type=str,
    default='shm-b084-sp15',
#    required=True,
    help="Shelf manager name",
)

parser.add_argument(
    "--slot", 
    type=int,
    default=7,
#    required=True,
    help="Slot number",
)

# Get the arguments
args     = parser.parse_args()

# Set the constants
slot     = args.slot

path     = os.getcwd()+'/../build/wrappers/bin/x86_64-linux-dbg/'

cmds = [ 'tfo_tmr_config --freqsyn %s/%d 1 0x3e 0x35 0x6e0 0xd75',
         'tfo_tmr_config --channel %s/%d 0 1 1 3 1',
         'tfo_tmr_config --channel %s/%d 1 0 1 3 1',
         'tfo_tmr_config --channel %s/%d 2 0 1 3 1',
         'tfo_tmr_config --channel %s/%d 3 0 1 3 1',
         'tfo_xpt_config --set %s/%d 0 2 2 2 2',
         'tfo_xpt_config --set %s/%d 1 0 0 0 0',
         'tfo_xpt_config --commit %s/%d 0', ]

for cmd in cmds:
    subprocess.check_call( ( path+cmd % (args.shm,slot) ), shell=True)
    time.sleep(0.1)

# Check the result
p = subprocess.Popen( path+'tfo_dump --tmr %s/%d' % (args.shm,slot), shell=True, stdout=subprocess.PIPE)
p.wait()
for line in p.stdout.readlines():
    if 'FP0' in line:
        if 'N/N' in line:
            print( "SUCCESSFULLY locked to timing input" )
            exit(0)
        else:
            print( line )

print ( "FAILED to lock to timing input" )
