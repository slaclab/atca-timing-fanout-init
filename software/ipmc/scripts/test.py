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

path     = os.getcwd()+'/../build/wrappers/bin/x86_64-linux-dbg/'

# Get the arguments
args     = parser.parse_args()

# Set the constants
slot     = args.slot

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

