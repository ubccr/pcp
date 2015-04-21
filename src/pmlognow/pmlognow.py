#!/usr/bin/env python

from pcp import pmapi
from pcp import pmi
import cpmapi as c_api
from ctypes import c_char, c_int, c_uint, c_long, c_char_p, c_void_p

import sys, math, datetime, getopt, time, socket

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

try:
    # Ignore missing and handle ourselves below
    metric_ids = context.pmLookupName(nameA, relaxed = 1)
except pmapi.pmErr as error:
    # Can get both types of returns, sent report to list
    metric_ids = error[1]


# Can't get both the exception and the pmIDs back if some fail so we do the check ourselves
badidx = [idx for idx, pmid in enumerate(metric_ids) if pmid == c_api.PM_ID_NULL]

if len(badidx):
    # Rebuild the ctypes array of pmids
    num_good = len(nameA) - len(badidx)
    num_copied = 0
    pmidGOOD = (c_uint * num_good)()
    for i in range( len(nameA) ):
        if i not in badidx:
            pmidGOOD[num_copied] = metric_ids[i]
            num_copied += 1

    metric_ids = pmidGOOD

    # Remove from the list of metrics we know about
    for idx in sorted(badidx, reverse=True):
        del nameA[idx]


descs = context.pmLookupDescs(metric_ids)
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
            # Just want to ignore if NULL indom
            #print >> sys.stderr, "No instance for %s" % nameA[i]
            pass
        else:
            raise

    # Add the Metric Definition
    log.pmiAddMetric( nameA[i], metric_ids[i], type, descs[i].contents.indom, descs[i].contents.sem, descs[i].contents.units )

    for j in range( results.contents.get_numval(i) ):
        atom = context.pmExtractValue(results.contents.get_valfmt(i),
            results.contents.get_vlist(i, j),
            type, type)

        val = atom.dref(type);

        # Is this the correct index, or do I need to look for results.contents.get_inst(i, j) in insts to get the index into iname
        # Seems to work
        if( len(insts)):
            inst_key = "%s:%s" %(descs[i].contents.indom, inames[j])
            if inst_key not in inst_dict:
                log.pmiAddInstance(descs[i].contents.indom, inames[j], insts[j])
                inst_dict[inst_key] = 1
            log.pmiPutValue( nameA[i], inames[j], "%s" % val )
        else:
            log.pmiPutValue( nameA[i], "", "%s" % val )

timetuple = math.modf(time)
useconds = int(timetuple[0] * 1000000)
seconds = int(timetuple[1])
log.pmiWrite( seconds, useconds)
