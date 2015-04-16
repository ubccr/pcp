#!/usr/bin/env python2.6
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


import math
import time
import re
from pcp import pmi
from pcp import pmapi
import cpmapi as c_api

# Get the generic mappings where we can query pcp for the metadata


context = pmapi.pmContext(c_api.PM_CONTEXT_HOST, "local:")

"""
mappingfile = open('pcp_mapping.txt', 'r')
mapping = {}

for line in mappingfile:
    fields = line.split(' ')
    # Skip any mappings that are not filled in
    if(len(fields) == 3):

        taccstats_type = fields[0]
        taccstats_metric = fields[1]
        pcp_metric = fields[2].rstrip()

        if taccstats_type not in mapping:
            mapping[taccstats_type] = {}

        mapping[taccstats_type][taccstats_metric] = pcp_metric

mappingfile.close()

print "from pcp import pmi"

print "pcpmappingdict = {"

for type in sorted(mapping):
    print "\t'%s': {" % type
    for metric in sorted(mapping[type]):
        
        pcp_metric = mapping[type][metric]

        pmids = context.pmLookupName( pcp_metric )
        descs = context.pmLookupDescs(pmids)

        print "\t\t'%s': {" % metric
        print "\t\t\t'name': '%s'," % pcp_metric
        print "\t\t\t'pmid': %d,\t#%s" % ( descs[0].contents.pmid , context.pmIDStr(descs[0].contents.pmid) )
        print "\t\t\t'type': %d,\t#%s" % ( descs[0].contents.type , context.pmTypeStr(descs[0].contents.type) )
        print "\t\t\t'sem': %d," % descs[0].contents.sem
        print "\t\t\t'units': '%s'," % context.pmUnitsStr( descs[0].contents.units )
        if( descs[0].contents.indom != c_api.PM_IN_NULL):
            # (inst, iname) = context.pmGetInDom( descs[0] )
            # print "Inames: ", inst, iname
            #
            # All the special cased indoms
            #
            # Special cases:
            #   ps load_1, load_5, load_15 are special cased as instances from tacc_stats individual metrics
            #   cpu instance names are constructed from a "cpu%d" type conversion
            #   mem/numa metrics have a "node%d" instance
            #   perfevents that have X/Y tacc_stats instances: X->instance, Y->%d in metric name
            #
            # Also, create lambdas for data conversion
            if type == "ps":
                # Inst Name
                inst = int(metric.split('_')[1])
                print "\t\t\t'inst': '%s'," % inst
                iname = "%d minute" % inst
                print "\t\t\t'iname': '%s'," % iname
                # Lambda
                print "\t\t\t'valconv': lambda x: x / 100.0,"
            elif type == "cpu":
                # Inst Name
                print "\t\t\t'inst_pattern': '%d',"
                print "\t\t\t'iname_pattern': 'cpu%d',"
                # Lambda
                print "\t\t\t'valconv': lambda x: x * 10,"
            # All the tacc_stats mem metrics are numa based
            elif type == "mem" or type == "numa":
                print "\t\t\t'inst_pattern': '%d',"
                print "\t\t\t'iname_pattern': 'node%d',"
            elif(type == "ib_sw" and ( metric == "rx_bytes" or metric == "tx_bytes") ):
                # Lambda
                print "\t\t\t'valconv': lambda x: x * 4,"
            elif(type == "block" and (metric == "rd_sectors" or metric == "wr_sectors" )):
                # Lambda
                print "\t\t\t'valconv': lambda x: x * 2,"
                
            print "\t\t\t'indom': %d},\t#%s" % ( descs[0].contents.indom, context.pmInDomStr( descs[0] ) )

        else:
            print "\t\t\t'indom': -1},"
    print "\t},"

# Grab the perfevent mappings where we give generated pmids and indoms

"""

perfmappingfile = open('tacc-pcp-map.txt', 'r')

num_metric = 0

perfmapping = {}

for line in perfmappingfile:
    fields = line.split(' ')
    # Skip any mappings that are not filled in
    if(len(fields) == 3):

        taccstats_type = fields[0]
        taccstats_metric = fields[1]
        pcp_metric = fields[2].rstrip()

        if taccstats_type not in perfmapping:
            perfmapping[taccstats_type] = {}

        perfmapping[taccstats_type][taccstats_metric] = pcp_metric

perfmappingfile.close()

for type in sorted(perfmapping):
    print "\t'%s': {" % type
    for metric in sorted(perfmapping[type]):
        
        pcp_metric = perfmapping[type][metric]

        pmid = "pmi.pmiLogImport.pmiID(127, %d, 0)" % (int(num_metric) + 1)
        indom = "pmi.pmiLogImport.pmiInDom(127, %d)" % num_metric

        print "\t\t'%s': {" % metric
        # Replace all - with _ for now
        print "\t\t\t'name': 'perfevent.hwcounters.%s.value'," % re.sub(r'[-=]', '_', pcp_metric)
        print "\t\t\t'pmid': %s," % pmid
        print "\t\t\t'type': 3,"
        print "\t\t\t'sem': 1,"
        print "\t\t\t'units': '',"
        # Inst Name
        print "\t\t\t'inst_pattern': '%d',"
        print "\t\t\t'iname_pattern': 'cpu%d',"
        print "\t\t\t'indom': %s}," % indom

        num_metric += 1
    print "\t},"

print "}"
