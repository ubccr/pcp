#
# Copyright (c) 2017 Martins Innus.  All Rights Reserved.
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

use strict;
use warnings;
use PCP::PMDA;

our $noval = PM_ERR_APPVERSION;

use vars qw( $pmda );

# Indom.  Will use port as instance
our  $omnipath_indom = 0;

our $OPAPMAQUERY_CMD = "opapmaquery";

# Configuration files for overriding the location of OPAPMAQUERY_CMD, etc, mostly for testing purposes
for my $file (pmda_config('PCP_PMDAS_DIR') . '/omnipath/omnipath.conf', 'omnipath.conf') {
        eval `cat $file` unless ! -f $file;
}

# Check env variable for OPAPMAQUERY_CMD to use.  Should be a cmd.  Easiest to use "echo test_file" for QA
if ( defined $ENV{"OPAPMAQUERY_CMD"} ) {
	$OPAPMAQUERY_CMD = $ENV{"OPAPMAQUERY_CMD"};
}

# The stats hash is keyed on port
our %h_omnipath = ();

sub omnipath_get_stats{
	open(OPAPMAQUERY, "$OPAPMAQUERY_CMD |") || die "Can't open pipe: $OPAPMAQUERY_CMD\n";

        # Not sure how errors are displayed, so just check if we have any ports reported
        my $port = -1;
	while (<OPAPMAQUERY>){
		my $line = $_;

                # New port ?
                if ($line =~ /^Port Number\h+(\d+)$/) {
                    $port = $1;
                    $h_omnipath{$port}={};
                    $h_omnipath{$port}->{'omnipath.port'} = $port;
                    next;
                }

                # Starts at 1
                if ($port < 1) {
                    next;
                }
                if ( $line =~ /^\h+Xmit Data\h+(\d+) MB \((\d+) Flits\)$/) {
                    # opapmaquery uses FLITS_PER_MB insted of 65 bits, so compute this ourselves
                    $h_omnipath{$port}->{'omnipath.xmit.bytes'} = int($2*65/8);
                    $h_omnipath{$port}->{'omnipath.xmit.flits'} = $2;
                } elsif ( $line =~ /^\h+Xmit Pkts\h+(\d+)$/) {
                    $h_omnipath{$port}->{'omnipath.xmit.pkts'} = $1;
                } elsif ( $line =~ /^\h+MC Xmt Pkts\h+(\d+)$/) {
                    $h_omnipath{$port}->{'omnipath.xmit.mcpkts'} = $1;
                } elsif ( $line =~ /^\h+Rcv Data\h+(\d+) MB \((\d+) Flits\)$/) {
                    # opapmaquery uses FLITS_PER_MB insted of 65 bits, so compute this ourselves
                    $h_omnipath{$port}->{'omnipath.rcv.bytes'} = int($2*65/8);
                    $h_omnipath{$port}->{'omnipath.rcv.flits'} = $2;
                } elsif ( $line =~ /^\h+Rcv Pkts\h+(\d+)$/) {
                    $h_omnipath{$port}->{'omnipath.rcv.pkts'} = $1;
                } elsif ( $line =~ /^\h+MC Rcv Pkts\h+(\d+)$/) {
                    $h_omnipath{$port}->{'omnipath.rcv.mcpkts'} = $1;
                } elsif ( $line =~ /^\h+Link Qual Indicator\h+(\d+) \(\w+\)$/) {
                    $h_omnipath{$port}->{'omnipath.error.link_quality'} = $1;
                } elsif ( $line =~ /^\h+Uncorrectable Errors\h+(\d+)$/) {
                    $h_omnipath{$port}->{'omnipath.error.uncorrectable'} = $1;
                } elsif ( $line =~ /^\h+Link Downed\h+(\d+)$/) {
                    $h_omnipath{$port}->{'omnipath.error.link_downed'} = $1;
                } elsif ( $line =~ /^\h+Rcv Errors\h+(\d+)$/) {
                    $h_omnipath{$port}->{'omnipath.error.rcv'} = $1;
                } elsif ( $line =~ /^\h+Exc. Buffer Overrun\h+(\d+)$/) {
                    $h_omnipath{$port}->{'omnipath.error.buffer_overrun'} = $1;
                } elsif ( $line =~ /^\h+FM Config Errors\h+(\d+)$/) {
                    $h_omnipath{$port}->{'omnipath.error.config'} = $1;
                } elsif ( $line =~ /^\h+Local Link Integ Err\h+(\d+)$/) {
                    $h_omnipath{$port}->{'omnipath.error.local_integrity'} = $1;
                } elsif ( $line =~ /^\h+Link Error Recovery\h+(\d+)$/) {
                    $h_omnipath{$port}->{'omnipath.error.recovery'} = $1;
                } elsif ( $line =~ /^\h+Rcv Rmt Phys Err\h+(\d+)$/) {
                    $h_omnipath{$port}->{'omnipath.error.rcv_phys'} = $1;
                } elsif ( $line =~ /^\h+Xmit Constraint\h+(\d+)$/) {
                    $h_omnipath{$port}->{'omnipath.error.xmit_constraint'} = $1;
                } elsif ( $line =~ /^\h+Rcv Constraint\h+(\d+)$/) {
                    $h_omnipath{$port}->{'omnipath.error.rcv_constraint'} = $1;
                } elsif ( $line =~ /^\h+Rcv Sw Relay Err\h+(\d+)$/) {
                    $h_omnipath{$port}->{'omnipath.error.rcv_relay'} = $1;
                } elsif ( $line =~ /^\h+Xmit Discards\h+(\d+)$/) {
                    $h_omnipath{$port}->{'omnipath.error.xmit_discards'} = $1;
                } elsif ( $line =~ /^\h+Congestion Discards\h+(\d+)$/) {
                    $h_omnipath{$port}->{'omnipath.congestion.discards'} = $1;
                } elsif ( $line =~ /^\h+Rcv FECN\h+(\d+)$/) {
                    $h_omnipath{$port}->{'omnipath.congestion.rcv_fecn'} = $1;
                } elsif ( $line =~ /^\h+Rcv BECN\h+(\d+)$/) {
                    $h_omnipath{$port}->{'omnipath.congestion.rcv_becn'} = $1;
                } elsif ( $line =~ /^\h+Mark FECN\h+(\d+)$/) {
                    $h_omnipath{$port}->{'omnipath.congestion.mark_fecn'} = $1;
                } elsif ( $line =~ /^\h+Xmit Time Congestion\h+(\d+)$/) {
                    $h_omnipath{$port}->{'omnipath.congestion.xmit_time'} = $1;
                } elsif ( $line =~ /^\h+Xmit Wait\h+(\d+)$/) {
                    $h_omnipath{$port}->{'omnipath.congestion.xmit_wait'} = $1;
                } elsif ( $line =~ /^\h+Xmit Wasted BW\h+(\d+)$/) {
                    $h_omnipath{$port}->{'omnipath.bubbles.xmit_wasted_bw'} = $1;
                } elsif ( $line =~ /^\h+Xmit Wait Data\h+(\d+)$/) {
                    $h_omnipath{$port}->{'omnipath.bubbles.xmit_wait_data'} = $1;
                } elsif ( $line =~ /^\h+Rcv Bubble\h+(\d+)$/) {
                    $h_omnipath{$port}->{'omnipath.bubbles.rcv'} = $1;
                }
	}
	close( OPAPMAQUERY );
}

#
# fetch is called once by pcp for each refresh and then the fetch callback is
# called to query each statistic individually
#
sub omnipath_fetch {
	omnipath_get_stats();

	our $pmda->replace_indom($omnipath_indom, \%h_omnipath);
}

sub omnipath_fetch_callback {
	my ($cluster, $item, $inst) = @_; 

	if( $cluster == 0 ){
		# opapmaquery stats 
		my $lookup = pmda_inst_lookup($omnipath_indom, $inst);
		return (PM_ERR_INST, 0) unless defined($lookup);

		my $pmid_name = pmda_pmid_name($cluster, $item)
			or die "Unknown metric name: cluster $cluster item $item\n";

		return ($lookup->{$pmid_name}, 1);
	}
	else{
		return (PM_ERR_PMID, 0);
	}
}

# the PCP::PMDA->new line is parsed by the check_domain rule of the PMDA build
# process, so there are special requirements:  no comments, the domain has to
# be a bare number.
#
our $pmda = PCP::PMDA->new('omnipath', 148);

# Metrics
#  opapmaquery stats - cluster 0
#  All registers are 64 bit

$pmda->add_metric(pmda_pmid(0,1), PM_TYPE_U64, $omnipath_indom,
		PM_SEM_INSTANT, pmda_units(0,0,0,0,0,0),
		'omnipath.port',
		'Port Number',
		'');

$pmda->add_metric(pmda_pmid(0, 2), PM_TYPE_U64, $omnipath_indom,
		PM_SEM_COUNTER, pmda_units(1,0,0,PM_SPACE_BYTE,0,0),
		'omnipath.xmit.bytes',
		'Transmit bytes',
		'');

$pmda->add_metric(pmda_pmid(0, 3), PM_TYPE_U64, $omnipath_indom,
		PM_SEM_COUNTER, pmda_units(0,0,1,0,0,PM_COUNT_ONE),
		'omnipath.xmit.flits',
		'Transmit FLITS',
		'');

$pmda->add_metric(pmda_pmid(0, 4), PM_TYPE_U64, $omnipath_indom,
		PM_SEM_COUNTER, pmda_units(0,0,1,0,0,PM_COUNT_ONE),
		'omnipath.xmit.pkts',
		'Transmit packets',
		'');

$pmda->add_metric(pmda_pmid(0, 5), PM_TYPE_U64, $omnipath_indom,
		PM_SEM_COUNTER, pmda_units(0,0,1,0,0,PM_COUNT_ONE),
		'omnipath.xmit.mcpkts',
		'Transmit multicast packets',
		'');

$pmda->add_metric(pmda_pmid(0, 6), PM_TYPE_U64, $omnipath_indom,
		PM_SEM_COUNTER, pmda_units(1,0,0,PM_SPACE_BYTE,0,0),
		'omnipath.rcv.bytes',
		'Receive bytes',
		'');

$pmda->add_metric(pmda_pmid(0, 7), PM_TYPE_U64, $omnipath_indom,
		PM_SEM_COUNTER, pmda_units(0,0,1,0,0,PM_COUNT_ONE),
		'omnipath.rcv.flits',
		'Receive FLITS',
		'');

$pmda->add_metric(pmda_pmid(0, 8), PM_TYPE_U64, $omnipath_indom,
		PM_SEM_COUNTER, pmda_units(0,0,1,0,0,PM_COUNT_ONE),
		'omnipath.rcv.pkts',
		'Receive packets',
		'');

$pmda->add_metric(pmda_pmid(0, 9), PM_TYPE_U64, $omnipath_indom,
		PM_SEM_COUNTER, pmda_units(0,0,1,0,0,PM_COUNT_ONE),
		'omnipath.rcv.mcpkts',
		'Receive multicast packets',
		'');

$pmda->add_metric(pmda_pmid(0,10), PM_TYPE_U64, $omnipath_indom,
		PM_SEM_INSTANT, pmda_units(0,0,0,0,0,0),
		'omnipath.error.link_quality',
		'Link Quality',
		'');

$pmda->add_metric(pmda_pmid(0, 11), PM_TYPE_U64, $omnipath_indom,
		PM_SEM_COUNTER, pmda_units(0,0,1,0,0,PM_COUNT_ONE),
		'omnipath.error.uncorrectable',
		'',
		'');

$pmda->add_metric(pmda_pmid(0, 12), PM_TYPE_U64, $omnipath_indom,
		PM_SEM_COUNTER, pmda_units(0,0,1,0,0,PM_COUNT_ONE),
		'omnipath.error.link_downed',
		'',
		'');

$pmda->add_metric(pmda_pmid(0, 13), PM_TYPE_U64, $omnipath_indom,
		PM_SEM_COUNTER, pmda_units(0,0,1,0,0,PM_COUNT_ONE),
		'omnipath.error.rcv',
		'',
		'');

$pmda->add_metric(pmda_pmid(0, 14), PM_TYPE_U64, $omnipath_indom,
		PM_SEM_COUNTER, pmda_units(0,0,1,0,0,PM_COUNT_ONE),
		'omnipath.error.buffer_overrun',
		'',
		'');

$pmda->add_metric(pmda_pmid(0, 15), PM_TYPE_U64, $omnipath_indom,
		PM_SEM_COUNTER, pmda_units(0,0,1,0,0,PM_COUNT_ONE),
		'omnipath.error.config',
		'',
		'');

$pmda->add_metric(pmda_pmid(0, 16), PM_TYPE_U64, $omnipath_indom,
		PM_SEM_COUNTER, pmda_units(0,0,1,0,0,PM_COUNT_ONE),
		'omnipath.error.local_integrity',
		'',
		'');

$pmda->add_metric(pmda_pmid(0, 17), PM_TYPE_U64, $omnipath_indom,
		PM_SEM_COUNTER, pmda_units(0,0,1,0,0,PM_COUNT_ONE),
		'omnipath.error.recovery',
		'',
		'');

$pmda->add_metric(pmda_pmid(0, 18), PM_TYPE_U64, $omnipath_indom,
		PM_SEM_COUNTER, pmda_units(0,0,1,0,0,PM_COUNT_ONE),
		'omnipath.error.rcv_phys',
		'',
		'');

$pmda->add_metric(pmda_pmid(0, 19), PM_TYPE_U64, $omnipath_indom,
		PM_SEM_COUNTER, pmda_units(0,0,1,0,0,PM_COUNT_ONE),
		'omnipath.error.xmit_constraint',
		'',
		'');

$pmda->add_metric(pmda_pmid(0, 20), PM_TYPE_U64, $omnipath_indom,
		PM_SEM_COUNTER, pmda_units(0,0,1,0,0,PM_COUNT_ONE),
		'omnipath.error.rcv_constraint',
		'',
		'');

$pmda->add_metric(pmda_pmid(0, 21), PM_TYPE_U64, $omnipath_indom,
		PM_SEM_COUNTER, pmda_units(0,0,1,0,0,PM_COUNT_ONE),
		'omnipath.error.rcv_relay',
		'',
		'');

$pmda->add_metric(pmda_pmid(0, 22), PM_TYPE_U64, $omnipath_indom,
		PM_SEM_COUNTER, pmda_units(0,0,1,0,0,PM_COUNT_ONE),
		'omnipath.error.xmit_discards',
		'',
		'');

$pmda->add_metric(pmda_pmid(0, 23), PM_TYPE_U64, $omnipath_indom,
		PM_SEM_COUNTER, pmda_units(0,0,1,0,0,PM_COUNT_ONE),
		'omnipath.congestion.discards',
		'',
		'');

$pmda->add_metric(pmda_pmid(0, 24), PM_TYPE_U64, $omnipath_indom,
		PM_SEM_COUNTER, pmda_units(0,0,1,0,0,PM_COUNT_ONE),
		'omnipath.congestion.rcv_fecn',
		'',
		'');

$pmda->add_metric(pmda_pmid(0, 25), PM_TYPE_U64, $omnipath_indom,
		PM_SEM_COUNTER, pmda_units(0,0,1,0,0,PM_COUNT_ONE),
		'omnipath.congestion.rcv_becn',
		'',
		'');

$pmda->add_metric(pmda_pmid(0, 26), PM_TYPE_U64, $omnipath_indom,
		PM_SEM_COUNTER, pmda_units(0,0,1,0,0,PM_COUNT_ONE),
		'omnipath.congestion.mark_fecn',
		'',
		'');

$pmda->add_metric(pmda_pmid(0, 27), PM_TYPE_U64, $omnipath_indom,
		PM_SEM_COUNTER, pmda_units(0,0,1,0,0,PM_COUNT_ONE),
		'omnipath.congestion.xmit_time',
		'',
		'');

$pmda->add_metric(pmda_pmid(0, 28), PM_TYPE_U64, $omnipath_indom,
		PM_SEM_COUNTER, pmda_units(0,0,1,0,0,PM_COUNT_ONE),
		'omnipath.congestion.xmit_wait',
		'',
		'');

$pmda->add_metric(pmda_pmid(0, 29), PM_TYPE_U64, $omnipath_indom,
		PM_SEM_COUNTER, pmda_units(0,0,1,0,0,PM_COUNT_ONE),
		'omnipath.bubbles.xmit_wasted_bw',
		'',
		'');

$pmda->add_metric(pmda_pmid(0, 30), PM_TYPE_U64, $omnipath_indom,
		PM_SEM_COUNTER, pmda_units(0,0,1,0,0,PM_COUNT_ONE),
		'omnipath.bubbles.xmit_wait_data',
		'',
		'');

$pmda->add_metric(pmda_pmid(0, 31), PM_TYPE_U64, $omnipath_indom,
		PM_SEM_COUNTER, pmda_units(0,0,1,0,0,PM_COUNT_ONE),
		'omnipath.bubbles.rcv',
		'',
		'');

&omnipath_get_stats;

$omnipath_indom = $pmda->add_indom($omnipath_indom, {}, '', '');

$pmda->set_fetch(\&omnipath_fetch);
$pmda->set_fetch_callback(\&omnipath_fetch_callback);

$pmda->run;
