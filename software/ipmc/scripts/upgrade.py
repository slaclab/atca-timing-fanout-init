#!/usr/bin/python
#-----------------------------------------------------------------------------
# File       : upgrade.py
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
import commands
import argparse
import time

# Set the argument parser
parser = argparse.ArgumentParser()

# Add arguments

parser.add_argument(
    "--fru", 
    type=str,
    default='../images/pc_379_396_18_c04.bin',
    #    required=True,
    help="path to FRU (.BIN) file",
    )

parser.add_argument(
    "--tag", 
    type=str,
    required=True,
    help="Product Asset Tag",
    )

parser.add_argument(
    "--fw", 
    type=str,
    default='../images/ipmc_tfo_fw.img',
    #    required=True,
    help="path to FRU (.BIN) file",
    )

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
fruName  = os.path.splitext(os.path.basename(args.fru))[0].lower()

# Check FRU's file extension 
if ( not args.fru.endswith('.bin') ):
    raise ValueError, "Invalid file extension (%s).  Should be .bin file extension." % (args.fru)

# Load the FRU file
subprocess.check_call( ( "cba_fru_init -s %s/%d -f %s --tag %s" % (args.shm,slot,args.fru,args.tag) ) , shell=True)
time.sleep(0.1)

#subprocess.check_call( ("bash set_threholds.bash -s %s -n %d" % (args.shm,slot) ) , shell=True)
#time.sleep(0.1)

# Get the value
retVar = commands.getstatusoutput("cba_fru_init -d %s/%d" % (args.shm,slot))
time.sleep(0.1)
print ( retVar[1] )
if ( fruName not in retVar[1]): 
    raise ValueError, "Invalid FRU detected.  Does not match with FRU's filename" % (fruName, retVar[1])

# Check FW's file extension 
if ( not args.fw.endswith('.img') ):
    raise ValueError, "Invalid fw file extension (%s).  Should be .img file extension." % (args.fw)

# Load the FW file
subprocess.check_call( ( "ipmitool -I lan -H %s -t 0x%x -b 0 -A NONE hpm upgrade %s activate all" % (args.shm,0x80+2*slot,args.fw) ) , shell=True)
time.sleep(0.1)

# Print that the configuration of IPMC passed.
subprocess.check_call( ( "cba_cold_data_reset %s/%d" % (args.shm,slot) ) , shell=True)   

print ( "\nSUCESSFULLY LOADED IPMC CONFIGURATION!\n" )

