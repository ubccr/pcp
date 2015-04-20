#!/usr/bin/env python
import datetime, errno, glob, numpy, os, sys, time, gzip
from subprocess import Popen, PIPE
import amd64_pmc, intel_snb
import re
import string

import pprint

import logging

if sys.version.startswith("3"):
    import io
    io_method = io.BytesIO
else:
    import cStringIO
    io_method = cStringIO.StringIO
    #import io
    #io.BufferedIOBase
verbose = os.getenv('TACC_STATS_VERBOSE')

if not verbose:
    numpy.seterr(over='ignore')
else:
    logging.basicConfig(level=logging.DEBUG)

prog = os.path.basename(sys.argv[0])
if prog == "":
    prog = "***"

def trace(fmt, *args):
    if verbose:
        msg = fmt % args
        sys.stderr.write(prog + ": " + msg)

def error(fmt, *args):
    msg = fmt % args
    sys.stderr.write(prog + ": " + msg)

SF_SCHEMA_CHAR = '!'
SF_DEVICES_CHAR = '@'
SF_COMMENT_CHAR = '#'
SF_PROPERTY_CHAR = '$'
SF_MARK_CHAR = '%'

def schema_fixup(type_name, desc):
    """ This function implements a workaround for a known issue with incorrect schema """
    """ definitions for irq, block and sched tacc_stats metrics. """

    if type_name == "irq":
        # All of the irq metrics are 32 bits wide
        res = ""
        for token in desc.split():
            res += token.strip() + ",W=32 "
        return res

    elif type_name == "sched":
        # Most sched counters are 32 bits wide with 3 exceptions
        res = ""
        sixtyfourbitcounters = [ "running_time,E,U=ms", "waiting_time,E,U=ms", "pcount,E" ]
        for token in desc.split():
            if token in sixtyfourbitcounters:
                res += token.strip() + " "
            else:
                res += token.strip() + ",W=32 "
        return res
    elif type_name == "block":
        # Most block counters are 64bits wide with a few exceptions
        res = ""
        thirtytwobitcounters = [ "rd_ticks,E,U=ms", "wr_ticks,E,U=ms", "in_flight", "io_ticks,E,U=ms", "time_in_queue,E,U=ms" ]
        for token in desc.split():
            if token in thirtytwobitcounters:
                res += token.strip() + ",W=32 "
            else:
                res += token.strip() + " "
        return res
    elif type_name == "panfs":
        # The syscall_*_(n+)s stats are not events
        res = ""
        for token in desc.split():
            token = token.strip()
            if token.startswith("syscall_") and ( token.endswith("_s,E,U=s") or token.endswith("_ns,E,U=ns")):
                res += string.replace(token, "E,", "") + " "
            else:
                res += token + " "
        return res
    elif type_name == "ib":
        res = ""
        for token in desc.split():
            token = token.strip()
            if not token.endswith(",W=32"):
                res += token.strip() + ",W=32 "
            else:
                res += token.strip() + " "
        return res

    return desc

class SchemaEntry(object):
    __slots__ = ('key', 'index', 'is_control', 'is_event', 'width', 'mult', 'unit')

    def __init__(self, i, s):
        opt_lis = s.split(',')
        self.key = opt_lis[0]
        self.index = i
        self.is_control = False
        self.is_event = False
        self.width = None
        self.mult = None
        self.unit = None
        for opt in opt_lis[1:]:
            if len(opt) == 0:
                continue
            elif opt[0] == 'C':
                self.is_control = True
            elif opt[0] == 'E':
                self.is_event = True
            elif opt[0:2] == 'W=':
                self.width = int(opt[2:])
            elif opt[0:2] == 'U=':
                j = 2
                while j < len(opt) and opt[j].isdigit():
                    j += 1
                if j > 2:
                    self.mult = numpy.uint64(opt[2:j])
                if j < len(opt):
                    self.unit = opt[j:]
                if self.unit == "KB":
                    self.mult = numpy.uint64(1024)
                    self.unit = "B"
            else:
                # XXX
                raise ValueError("unrecognized option `%s' in schema entry spec `%s'\n", opt, s)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
               all(self.__getattribute__(attr) == other.__getattribute__(attr) \
                   for attr in self.__slots__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        lis = [] # 'index=%d' % self.index
        if self.is_event:
            lis.append('is_event=True')
        elif self.is_control:
            lis.append('is_control=True')
        if self.width:
            lis.append('width=%d' % int(self.width))
        if self.mult:
            lis.append('mult=%d' % int(self.mult))
        if self.unit:
            lis.append('unit=%s' % self.unit)
        return '(' + ', '.join(lis) + ')'


class Schema(dict):
    def __init__(self, desc):
        dict.__init__(self)
        self.desc = desc
        self._key_list = []
        self._value_list = []
        for i, s in enumerate(desc.split()):
            e = SchemaEntry(i, s)
            dict.__setitem__(self, e.key, e)
            self._key_list.append(e.key)
            self._value_list.append(e)

    def __iter__(self):
        return self._key_list.__iter__()

    def __repr__(self):
        return '{' + ', '.join(("'%s': %s" % (k, repr(self[k]))) \
                               for k in self._key_list) + '}'

    def _notsup(self, s):
        raise TypeError("'Schema' object does not support %s" % s)

    def __delitem__(self, k, v):
        self._notsup('item deletion')

    def pop(self, k, d=None):
        self._notsup('removal')

    def popitem(self):
        self._notsup('removal')

    def setdefault(self, k, d=None):
        self._notsup("item assignment")

    def update(self, **args):
        self._notsup("update")

    def items(self):
        return zip(self._key_list, self._value_list)

    def iteritems(self):
        for k in self._key_list:
            yield (k, dict.__getitem__(self, k))

    def iterkeys(self):
        return self._key_list.__iter__()

    def itervalues(self):
        return self._value_list.__iter__()

    def keys(self):
        return self._key_list

    def values(self):
        return self._value_list

# ------------------------------------------------------------------


# PCP mappings

def gen_conv():
    print "do something"

pcpmapping = {
    'mem': {
        'MemTotal': {
            'name': "foo.bar",
            'pmid': 100,
            'type': 200,
            'indom': 300,
            'sem': 400,
            'units': 500},
        'MemFree': {
            'name': "foo.bar",
            'pmid': 100,
            'type': 200,
            'indom': 300,
            'units': 500}
    },
    'cpu': {
        'User': {
            'name': "foo.bar",
            'pmid': 100,
            'sem': 400,
            'units': 500,
            'conv': gen_conv}
    }
}


class Host(object):
    def __init__(self, job):
        self.job = job

        self.times = []
        self.raw_stats = {}
        self.marks = {}

        self.timestamp = None
        self.filename = None
        self.fileline = None

    def trace(self, fmt, *args):
        logging.debug( fmt % args )

    def error(self, fmt, *args):
        self.job.error('%s: ' + fmt, self.name, *args)

    def read_stats_file_header(self, fp):
        file_schemas = {}
        for line in fp:
            self.fileline += 1
            try:
                c = line[0]
                if c == SF_SCHEMA_CHAR:
                    type_name, schema_desc = line[1:].split(None, 1)
                    schema = self.job.get_schema(type_name, schema_desc)
                    if schema:
                        file_schemas[type_name] = schema
                    else:
                        self.error("file `%s', type `%s', schema mismatch desc `%s'\n",
                                   fp.name, type_name, schema_desc)
                elif c == SF_PROPERTY_CHAR:
                    pass
                elif c == SF_COMMENT_CHAR:
                    pass
                else:
                    break
            except Exception as exc:
                self.error("file `%s', caught `%s' discarding line `%s'\n",
                           fp.name, exc, line)
                break
        return file_schemas


    def read_stats_file(self, fp):

        self.filename = fp.name
        self.fileline = 0

        self.file_schemas = self.read_stats_file_header(fp)
        if not self.file_schemas:
            self.error("file `%s' bad header on line %s\n", self.filename, self.fileline)
            return

        for line in fp:
            self.fileline += 1
            self.parse(line.strip())


    def parse(self, line):
        if len(line) < 1:
            return

        ch = line[0]

        if ch.isdigit():
            self.processtimestamp(line)
        elif ch.isalpha():
            self.processdata(line)
        elif ch == SF_COMMENT_CHAR:
            pass
        elif ch == SF_MARK_CHAR:
            #print "Skipping mark for now"
            pass
        else:
            print "Unregognised character \"{}\"".format(line)
            pass

    def processtimestamp(self,line):
        recs = line.strip().split(" ")
        self.timestamp = float(recs[0])
        jobs = recs[1].strip().split(",")
        #print "Adding time : %f" %  self.timestamp
        self.times.append( self.timestamp )
        self.job.times.append( self.timestamp )

    def processdata(self,line):
        type_name, dev_name, rest = line.split(None, 2)
        schema = self.file_schemas.get(type_name)
        if not schema:
            self.error("file `%s', unknown type `%s', discarding line `%s'\n",
                    self.filename, type_name, self.fileline)
            return

        vals = numpy.fromstring(rest, dtype=numpy.uint64, sep=' ')
        if vals.shape[0] != len(schema):
            self.error("file `%s', type `%s', expected %d values, read %d, discarding line `%s'\n",
                   self.filename, type_name, len(schema), vals.shape[0], self.fileline)
            return

        type_stats = self.raw_stats.setdefault(type_name, {})
        dev_stats = type_stats.setdefault(dev_name, [])
        dev_stats.append((self.timestamp, vals))

    def gather_stats(self):
        try:
            with gzip.open("tacc/1424239201.gz") as file:
                self.read_stats_file(file)
        except IOError as ioe:
            self.error("read error for file %s\n", path)

        return self.raw_stats

    def get_stats(self, type_name, dev_name, key_name):
        """Host.get_stats(type_name, dev_name, key_name)
        Return the vector of stats for the given type, dev, and key.
        """
        schema = self.job.get_schema(type_name)
        index = schema[key_name].index
        return self.stats[type_name][dev_name][:, index]


class Job(object):
    # TODO errors/comments
    __slots__ = ('savehost', 'schemas', 'times')

    def __init__(self):
        self.schemas = {}
        self.times = []

    def trace(self, fmt, *args):
        trace('%s: ' + fmt, *args)

    def error(self, fmt, *args):
        error('%s: ' + fmt, self.id, *args)

    def get_schema(self, type_name, desc=None):
        schema = self.schemas.get(type_name)
        if schema:
            if desc and schema.desc != schema_fixup(type_name,desc):
                # ...
                return None
        elif desc:
            desc = schema_fixup(type_name, desc)
            schema = self.schemas[type_name] = Schema(desc)
        return schema

    def gather_stats(self):
        host = Host(self)
        host.gather_stats()
        self.savehost = host
        return True

    def process_dev_stats(self, host, type_name, schema, dev_name, raw):
        def trace(fmt, *args):
            return self.trace("host `%s', type `%s', dev `%s': " + fmt,
                              host.name, type_name, dev_name, *args)
        def error(fmt, *args):
            return self.error("host `%s', type `%s', dev `%s': " + fmt,
                              host.name, type_name, dev_name, *args)
        # raw is a list of pairs with car the timestamp and cdr a 1d
        # numpy array of values.
        m = len(host.times)
        n = len(schema)
        A = numpy.zeros((m, n), dtype=numpy.uint64) # Output.

        k = len(raw)
        # len(raw) may not be equal to m, so we fill out A from 0
        # And keep track of this metric/instance time series
        #print "%s , %s: raw: %d, times: %d" % (type_name, dev_name, len(raw), m)
        timekey = "%s%s" % (type_name, dev_name)
        self.savehost.metrictime[timekey]=[]
        for i in xrange(0, k):
            A[i] = raw[i][1]
            self.savehost.metrictime[timekey].append( raw[i][0])

        # convert units.
        for e in schema.itervalues():
            j = e.index
            # Keep this for now
            if e.mult:
                for i in range(0, m):
                    A[i, j] *= e.mult
        return A

    def process_stats(self):
        self.savehost.stats = {}
        self.savehost.metrictime = {}
        #print "pretime"
        #pprint.pprint(self.times)
        #print "posttime"
        for type_name, raw_type_stats in self.savehost.raw_stats.iteritems():
            stats = self.savehost.stats[type_name] = {}
            schema = self.schemas[type_name]
            for dev_name, raw_dev_stats in raw_type_stats.iteritems():
                stats[dev_name] = self.process_dev_stats(self.savehost, type_name, schema,
                                                             dev_name, raw_dev_stats)
        del self.savehost.raw_stats
        amd64_pmc.process_job(self)
        intel_snb.process_job(self)
        # Clear mult, width from schemas. XXX
        for schema in self.schemas.itervalues():
            for e in schema.itervalues():
                e.width = None
                e.mult = None

        #pprint.pprint( self.savehost.stats )
        #pprint.pprint( self.savehost.times )
        #pprint.pprint( self.schemas )    
        #pprint.pprint( pcpmapping )    

        return True
    
    def get_stats(self, type_name, dev_name, key_name):
        """Job.get_stats(type_name, dev_name, key_name)
        Return a dictionary with keys host names and values the vector
        of stats for the given type, dev, and key.
        """
        schema = self.get_schema(type_name)
        index = schema[key_name].index
        host_stats = {}
        for host_name, host in self.hosts.iteritems():
            host_stats[host_name] = host.stats[type_name][dev_name][:, index]
        return host_stats


def get_data():
    job = Job()
    job.gather_stats() and job.process_stats()
    # generate a pcp mapping
    
    for name, schema in job.schemas.iteritems():
        for e in schema.itervalues():
            print "%s %s" % (name, e.key)


    
if __name__ == '__main__':
    get_data();
