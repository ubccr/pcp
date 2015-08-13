#!/usr/bin/env python
#
# Copyright (c) 2015 Martins Innus.  All Rights Reserved.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#

from pcp import pmapi
from pcp import pmi
import cpmapi as c_api
from ctypes import c_char, c_int, c_uint, c_long, c_char_p, c_void_p

import sys, math, datetime, getopt, time, socket
import re

import pprint

import string

use_config_file = 0
hostname = socket.getfqdn()
nowtime = time.time()
logname = datetime.datetime.fromtimestamp( nowtime ).strftime("%Y%m%d.%H.%M")

outdir = "./"
prefix = ""

usage = '%s [-s] [-p name_prefix] [-n hostname] [-o outputname] [-d outdir] [-c <logger config> | <list of metrics>]' % sys.argv[0]

try:
    opts, args = getopt.getopt(sys.argv[1:],"shc:n:o:d:p:")
except getopt.GetoptError:
    print usage
    sys.exit(2)

for opt, arg in opts:
    if opt == '-h':
        print usage
        sys.exit()
    elif opt == '-c':
        config_file = arg
        use_config_file = 1
    elif opt == '-n':
        hostname = arg
    elif opt == '-o':
        logname = arg
    elif opt == '-d':
        outdir = arg
    elif opt == '-s':
        # Add seconds into the date field
        logname = datetime.datetime.fromtimestamp( nowtime ).strftime("%Y%m%d.%H.%M.%S")
    elif opt == '-p':
        prefix = arg

logname = prefix + logname

nameA = []

# Need either a list of metrics on the command line or parse out a pmlogger config
if not use_config_file and len(args) >= 1 and args[0] != '':
    nameA = args
elif use_config_file:
    infile = open( config_file )
    for line in infile:
        # Drop comments anywhere in line
        line = line.split("#")[0]
        line = line.strip()
        if '{' in line or '}' in line:
            continue
        if 'access' in line or 'allow' in line:
            continue
        if line != '':
            nameA.append(line)
else:
    print usage
    sys.exit(2)

# local host context
try:
    context = pmapi.pmContext(c_api.PM_CONTEXT_HOST, "local:")
except pmapi.pmErr as error:
    print "Couldn't get context"
    sys.exit(2)

# Expand any nonleaf names
leafNodes = []
def getLeafNodes( leafnode ):
    leafNodes.append( leafnode )

for name in nameA:
    try:
        context.pmTraversePMNS( name, getLeafNodes )
    except pmapi.pmErr as error:
        # Just skip invalid names
        pass

nameA = leafNodes;

# Remove duplicates
nameA = list(set(nameA))

# Get metric IDs
try:
    metric_ids = context.pmLookupName(nameA, relaxed = 1)
except pmapi.pmErr as error:
    # Probably can only exit here. Deal with the PM_ID_NULL case
    # below, which should not end up here.
    print "Unhandled pmLookupName exception\n"
    sys.exit(2)


# Check for unresolveable names, will have PM_ID_NULL as metric id
badidx = [idx for idx, pmid in enumerate(metric_ids) if pmid == c_api.PM_ID_NULL]

descs = []

# Deal with any entries in badidx already, and add new ones that pmLookupDesc fails to resolve
pmidGOOD = []
for i in range( len(nameA) ):
    if i not in badidx:
        # Also make sure we can get the desc before adding as a good metric
        # Python API errors out as soon as one error is seen so can't check all at once
        try:
            desc = context.pmLookupDesc(metric_ids[i])
            descs.append(desc)
            pmidGOOD.append(metric_ids[i])
        except pmapi.pmErr as error:
            # Couldn't get the desc so just drop this metric
            badidx.append(i)
    else:
        # Skip errors and dump this metric below
        # We already handled nonleaf metrics above
        pass

# Rebuild the list of metrics
# All should be good at this point
metric_ids = (c_uint * len(pmidGOOD))(*pmidGOOD)

# Remove bad ones from the list of metrics we know about
for idx in sorted(badidx, reverse=True):
    del nameA[idx]

# Need to deal with errors with Fetch in some way
results = context.pmFetch(metric_ids)

time = results.contents.timestamp

filelabel = outdir + "/" + logname

log = pmi.pmiLogImport( filelabel )
log.pmiSetHostname( hostname )

# Only add instances once
inst_dict = {}

for i in range(results.contents.numpmid):
    type = descs[i].contents.type

    insts = []
    inames = []

    try:
        insts, inames = context.pmGetInDom( descs[i] )
    except pmapi.pmErr as error:
        if "PM_ERR_INDOM" in str(error):
            # Any better way to do this ?
            # Just want to figure out if this metric has an indom to use below
            pass
        else:
            raise

    # Temporary hack for bad perfctr metric names
    # Need to fix in the perfctr pmda
    # The pmi API seems to be the only spot this is enforced
    putname = re.sub(r'[-=]', '_', nameA[i])

    # Skip Event Types for now
    if( type == c_api.PM_TYPE_EVENT ):
        continue

    # Add the Metric Definition
    log.pmiAddMetric( putname, metric_ids[i], type, descs[i].contents.indom, descs[i].contents.sem, descs[i].contents.units )

    for j in range( results.contents.get_numval(i) ):
        atom = context.pmExtractValue(results.contents.get_valfmt(i),
            results.contents.get_vlist(i, j),
            type, type)

        val = atom.dref(type);

        if( len(insts)):
            inst_id = results.contents.get_inst(i, j)
            inst_name = ""

            if inst_id in insts:
                inst_name = inames[ insts.index( inst_id ) ]
            else:
                # Instance disappeared, just skip it
                print "i,j,name,inst_id : %d, %d, %s, %d missing\n" % (i,j,nameA[i],inst_id)
                continue
                
            # Check to make sure we don't add the instance more than once across different metrics
            # "indom:inst_name" should be unique
            inst_key = "%s:%s" %(descs[i].contents.indom, inst_name)

            if inst_key not in inst_dict:
                log.pmiAddInstance(descs[i].contents.indom, inst_name, inst_id)
                inst_dict[inst_key] = 1
            log.pmiPutValue( putname, inst_name, "%s" % val )
        else:
            log.pmiPutValue( putname, "", "%s" % val )

timetuple = math.modf(time)
useconds = int(timetuple[0] * 1000000)
seconds = int(timetuple[1])
log.pmiWrite( seconds, useconds)
