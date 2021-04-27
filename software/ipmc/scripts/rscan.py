#!/usr/bin/python
#-----------------------------------------------------------------------------
# File       : test.py
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
    default='shm-b084-sp17',
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

parser.add_argument(
    "--steps", 
    type=lambda x: int(x,0),
    nargs=3,
    required=True,
    help="R value steps (min, max, stepsize)",
)

path     = os.getcwd()+'/../build/wrappers/bin/x86_64-linux-dbg/'

# Get the arguments
args     = parser.parse_args()

# Set the constants
slot     = args.slot

print('steps {}'.format(args.steps))

for r in range(args.steps[0], args.steps[1], args.steps[2]):

    try:
        # Program the new setting
        p = subprocess.Popen( path+'tfo_tmr_config -f %s/%d 1 0x3e 0x35 0x6e0 %d' % (args.shm,slot,r), shell=True, stdout=subprocess.PIPE)
        p.wait()
 
    # Check the result
        p = subprocess.Popen( path+'tfo_dump --tmr %s/%d' % (args.shm,slot), shell=True, stdout=subprocess.PIPE)
        p.wait()
        for line in p.stdout.readlines():
            if 'FP0' in line:
                if 'N/N' in line:
                    print( "0x%x : SUCCESS" % r )
                else:
                    print( "0x%x : FAIL" % r )

    except:
        print('Caught exception')
