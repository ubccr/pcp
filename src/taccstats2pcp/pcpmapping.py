from pcp import pmi
pcpmappingdict = {
	'block': {
		'rd_ios': {
			'name': 'disk.dev.read',
			'pmid': 251658244,	#60.0.4
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': 251658241},	#60.1
		'rd_merges': {
			'name': 'disk.dev.read_merge',
			'pmid': 251658289,	#60.0.49
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': 251658241},	#60.1
		'rd_sectors': {
			'name': 'disk.dev.read_bytes',
			'pmid': 251658278,	#60.0.38
			'type': 1,	#U32
			'sem': 1,
			'units': 'Kbyte',
			'valconv': lambda x: x * 2,
			'indom': 251658241},	#60.1
		'rd_ticks': {
			'name': 'disk.dev.read_rawactive',
			'pmid': 251658312,	#60.0.72
			'type': 1,	#U32
			'sem': 1,
			'units': 'millisec',
			'indom': 251658241},	#60.1
		'wr_ios': {
			'name': 'disk.dev.write',
			'pmid': 251658245,	#60.0.5
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': 251658241},	#60.1
		'wr_merges': {
			'name': 'disk.dev.write_merge',
			'pmid': 251658290,	#60.0.50
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': 251658241},	#60.1
		'wr_sectors': {
			'name': 'disk.dev.write_bytes',
			'pmid': 251658279,	#60.0.39
			'type': 1,	#U32
			'sem': 1,
			'units': 'Kbyte',
			'valconv': lambda x: x * 2,
			'indom': 251658241},	#60.1
		'wr_ticks': {
			'name': 'disk.dev.write_rawactive',
			'pmid': 251658313,	#60.0.73
			'type': 1,	#U32
			'sem': 1,
			'units': 'millisec',
			'indom': 251658241},	#60.1
	},
	'cpu': {
		'idle': {
			'name': 'kernel.percpu.cpu.idle',
			'pmid': 251658243,	#60.0.3
			'type': 3,	#U64
			'sem': 1,
			'units': 'millisec',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'valconv': lambda x: x * 10,
			'indom': 251658240},	#60.0
		'iowait': {
			'name': 'kernel.percpu.cpu.wait.total',
			'pmid': 251658270,	#60.0.30
			'type': 3,	#U64
			'sem': 1,
			'units': 'millisec',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'valconv': lambda x: x * 10,
			'indom': 251658240},	#60.0
		'irq': {
			'name': 'kernel.percpu.cpu.irq.hard',
			'pmid': 251658297,	#60.0.57
			'type': 3,	#U64
			'sem': 1,
			'units': 'millisec',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'valconv': lambda x: x * 10,
			'indom': 251658240},	#60.0
		'nice': {
			'name': 'kernel.percpu.cpu.nice',
			'pmid': 251658241,	#60.0.1
			'type': 3,	#U64
			'sem': 1,
			'units': 'millisec',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'valconv': lambda x: x * 10,
			'indom': 251658240},	#60.0
		'softirq': {
			'name': 'kernel.percpu.cpu.irq.soft',
			'pmid': 251658296,	#60.0.56
			'type': 3,	#U64
			'sem': 1,
			'units': 'millisec',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'valconv': lambda x: x * 10,
			'indom': 251658240},	#60.0
		'system': {
			'name': 'kernel.percpu.cpu.sys',
			'pmid': 251658242,	#60.0.2
			'type': 3,	#U64
			'sem': 1,
			'units': 'millisec',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'valconv': lambda x: x * 10,
			'indom': 251658240},	#60.0
		'user': {
			'name': 'kernel.percpu.cpu.user',
			'pmid': 251658240,	#60.0.0
			'type': 3,	#U64
			'sem': 1,
			'units': 'millisec',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'valconv': lambda x: x * 10,
			'indom': 251658240},	#60.0
	},
	'ib_sw': {
		'rx_bytes': {
			'name': 'infiniband.port.switch.in.bytes',
			'pmid': 381684736,	#91.3.0
			'type': 3,	#U64
			'sem': 1,
			'units': 'byte',
			'valconv': lambda x: x * 4,
			'indom': 381681665},	#91.1
		'rx_packets': {
			'name': 'infiniband.port.switch.in.packets',
			'pmid': 381684737,	#91.3.1
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': 381681665},	#91.1
		'tx_bytes': {
			'name': 'infiniband.port.switch.out.bytes',
			'pmid': 381684738,	#91.3.2
			'type': 3,	#U64
			'sem': 1,
			'units': 'byte',
			'valconv': lambda x: x * 4,
			'indom': 381681665},	#91.1
		'tx_packets': {
			'name': 'infiniband.port.switch.out.packets',
			'pmid': 381684739,	#91.3.3
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': 381681665},	#91.1
	},
	'mem': {
		'Active': {
			'name': 'mem.numa.util.active',
			'pmid': 251695107,	#60.36.3
			'type': 3,	#U64
			'sem': 3,
			'units': 'Kbyte',
			'inst_pattern': '%d',
			'iname_pattern': 'node%d',
			'indom': 251658259},	#60.19
		'AnonPages': {
			'name': 'mem.numa.util.anonpages',
			'pmid': 251695123,	#60.36.19
			'type': 3,	#U64
			'sem': 3,
			'units': 'Kbyte',
			'inst_pattern': '%d',
			'iname_pattern': 'node%d',
			'indom': 251658259},	#60.19
		'Bounce': {
			'name': 'mem.numa.util.bounce',
			'pmid': 251695128,	#60.36.24
			'type': 3,	#U64
			'sem': 3,
			'units': 'Kbyte',
			'inst_pattern': '%d',
			'iname_pattern': 'node%d',
			'indom': 251658259},	#60.19
		'Dirty': {
			'name': 'mem.numa.util.dirty',
			'pmid': 251695119,	#60.36.15
			'type': 3,	#U64
			'sem': 3,
			'units': 'Kbyte',
			'inst_pattern': '%d',
			'iname_pattern': 'node%d',
			'indom': 251658259},	#60.19
		'HugePages_Free': {
			'name': 'mem.numa.util.hugepagesFree',
			'pmid': 251695134,	#60.36.30
			'type': 3,	#U64
			'sem': 3,
			'units': 'count',
			'inst_pattern': '%d',
			'iname_pattern': 'node%d',
			'indom': 251658259},	#60.19
		'HugePages_Total': {
			'name': 'mem.numa.util.hugepagesTotal',
			'pmid': 251695133,	#60.36.29
			'type': 3,	#U64
			'sem': 3,
			'units': 'count',
			'inst_pattern': '%d',
			'iname_pattern': 'node%d',
			'indom': 251658259},	#60.19
		'Inactive': {
			'name': 'mem.numa.util.inactive',
			'pmid': 251695108,	#60.36.4
			'type': 3,	#U64
			'sem': 3,
			'units': 'Kbyte',
			'inst_pattern': '%d',
			'iname_pattern': 'node%d',
			'indom': 251658259},	#60.19
		'Mapped': {
			'name': 'mem.numa.util.mapped',
			'pmid': 251695122,	#60.36.18
			'type': 3,	#U64
			'sem': 3,
			'units': 'Kbyte',
			'inst_pattern': '%d',
			'iname_pattern': 'node%d',
			'indom': 251658259},	#60.19
		'MemFree': {
			'name': 'mem.numa.util.free',
			'pmid': 251695105,	#60.36.1
			'type': 3,	#U64
			'sem': 3,
			'units': 'Kbyte',
			'inst_pattern': '%d',
			'iname_pattern': 'node%d',
			'indom': 251658259},	#60.19
		'MemTotal': {
			'name': 'mem.numa.util.total',
			'pmid': 251695104,	#60.36.0
			'type': 3,	#U64
			'sem': 3,
			'units': 'Kbyte',
			'inst_pattern': '%d',
			'iname_pattern': 'node%d',
			'indom': 251658259},	#60.19
		'MemUsed': {
			'name': 'mem.numa.util.used',
			'pmid': 251695106,	#60.36.2
			'type': 3,	#U64
			'sem': 3,
			'units': 'Kbyte',
			'inst_pattern': '%d',
			'iname_pattern': 'node%d',
			'indom': 251658259},	#60.19
		'NFS_Unstable': {
			'name': 'mem.numa.util.NFS_Unstable',
			'pmid': 251695127,	#60.36.23
			'type': 3,	#U64
			'sem': 3,
			'units': 'Kbyte',
			'inst_pattern': '%d',
			'iname_pattern': 'node%d',
			'indom': 251658259},	#60.19
		'PageTables': {
			'name': 'mem.numa.util.pageTables',
			'pmid': 251695126,	#60.36.22
			'type': 3,	#U64
			'sem': 3,
			'units': 'Kbyte',
			'inst_pattern': '%d',
			'iname_pattern': 'node%d',
			'indom': 251658259},	#60.19
		'Slab': {
			'name': 'mem.numa.util.slab',
			'pmid': 251695130,	#60.36.26
			'type': 3,	#U64
			'sem': 3,
			'units': 'Kbyte',
			'inst_pattern': '%d',
			'iname_pattern': 'node%d',
			'indom': 251658259},	#60.19
		'Writeback': {
			'name': 'mem.numa.util.writeback',
			'pmid': 251695120,	#60.36.16
			'type': 3,	#U64
			'sem': 3,
			'units': 'Kbyte',
			'inst_pattern': '%d',
			'iname_pattern': 'node%d',
			'indom': 251658259},	#60.19
	},
	'net': {
		'collisions': {
			'name': 'network.interface.collisions',
			'pmid': 251661325,	#60.3.13
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': 251658243},	#60.3
		'multicast': {
			'name': 'network.interface.total.mcasts',
			'pmid': 251661332,	#60.3.20
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': 251658243},	#60.3
		'rx_bytes': {
			'name': 'network.interface.in.bytes',
			'pmid': 251661312,	#60.3.0
			'type': 3,	#U64
			'sem': 1,
			'units': 'byte',
			'indom': 251658243},	#60.3
		'rx_compressed': {
			'name': 'network.interface.in.compressed',
			'pmid': 251661318,	#60.3.6
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': 251658243},	#60.3
		'rx_dropped': {
			'name': 'network.interface.in.drops',
			'pmid': 251661315,	#60.3.3
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': 251658243},	#60.3
		'rx_errors': {
			'name': 'network.interface.in.errors',
			'pmid': 251661314,	#60.3.2
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': 251658243},	#60.3
		'rx_fifo_errors': {
			'name': 'network.interface.in.fifo',
			'pmid': 251661316,	#60.3.4
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': 251658243},	#60.3
		'rx_frame_errors': {
			'name': 'network.interface.in.frame',
			'pmid': 251661317,	#60.3.5
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': 251658243},	#60.3
		'rx_packets': {
			'name': 'network.interface.in.packets',
			'pmid': 251661313,	#60.3.1
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': 251658243},	#60.3
		'tx_bytes': {
			'name': 'network.interface.out.bytes',
			'pmid': 251661320,	#60.3.8
			'type': 3,	#U64
			'sem': 1,
			'units': 'byte',
			'indom': 251658243},	#60.3
		'tx_carrier_errors': {
			'name': 'network.interface.out.carrier',
			'pmid': 251661326,	#60.3.14
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': 251658243},	#60.3
		'tx_compressed': {
			'name': 'network.interface.out.compressed',
			'pmid': 251661327,	#60.3.15
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': 251658243},	#60.3
		'tx_errors': {
			'name': 'network.interface.out.errors',
			'pmid': 251661322,	#60.3.10
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': 251658243},	#60.3
		'tx_packets': {
			'name': 'network.interface.out.packets',
			'pmid': 251661321,	#60.3.9
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': 251658243},	#60.3
	},
	'numa': {
		'interleave_hit': {
			'name': 'mem.numa.alloc.interleave_hit',
			'pmid': 251695139,	#60.36.35
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'inst_pattern': '%d',
			'iname_pattern': 'node%d',
			'indom': 251658259},	#60.19
		'local_node': {
			'name': 'mem.numa.alloc.local_node',
			'pmid': 251695140,	#60.36.36
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'inst_pattern': '%d',
			'iname_pattern': 'node%d',
			'indom': 251658259},	#60.19
		'numa_foreign': {
			'name': 'mem.numa.alloc.foreign',
			'pmid': 251695138,	#60.36.34
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'inst_pattern': '%d',
			'iname_pattern': 'node%d',
			'indom': 251658259},	#60.19
		'numa_hit': {
			'name': 'mem.numa.alloc.hit',
			'pmid': 251695136,	#60.36.32
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'inst_pattern': '%d',
			'iname_pattern': 'node%d',
			'indom': 251658259},	#60.19
		'numa_miss': {
			'name': 'mem.numa.alloc.miss',
			'pmid': 251695137,	#60.36.33
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'inst_pattern': '%d',
			'iname_pattern': 'node%d',
			'indom': 251658259},	#60.19
		'other_node': {
			'name': 'mem.numa.alloc.other_node',
			'pmid': 251695141,	#60.36.37
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'inst_pattern': '%d',
			'iname_pattern': 'node%d',
			'indom': 251658259},	#60.19
	},
	'ps': {
		'load_1': {
			'name': 'kernel.all.load',
			'pmid': 251660288,	#60.2.0
			'type': 4,	#FLOAT
			'sem': 3,
			'units': '',
			'inst': '1',
			'iname': '1 minute',
			'valconv': lambda x: x / 100.0,
			'indom': 251658242},	#60.2
		'load_15': {
			'name': 'kernel.all.load',
			'pmid': 251660288,	#60.2.0
			'type': 4,	#FLOAT
			'sem': 3,
			'units': '',
			'inst': '15',
			'iname': '15 minute',
			'valconv': lambda x: x / 100.0,
			'indom': 251658242},	#60.2
		'load_5': {
			'name': 'kernel.all.load',
			'pmid': 251660288,	#60.2.0
			'type': 4,	#FLOAT
			'sem': 3,
			'units': '',
			'inst': '5',
			'iname': '5 minute',
			'valconv': lambda x: x / 100.0,
			'indom': 251658242},	#60.2
	},
	'sysv_shm': {
		'mem_used': {
			'name': 'ipc.shm.max_shmsys',
			'pmid': 251681796,	#60.23.4
			'type': 1,	#U32
			'sem': 4,
			'units': '',
			'indom': -1},
		'segs_used': {
			'name': 'ipc.shm.max_seg',
			'pmid': 251681794,	#60.23.2
			'type': 1,	#U32
			'sem': 4,
			'units': '',
			'indom': -1},
	},
	'tmpfs': {
		'bytes_used': {
			'name': 'tmpfs.used',
			'pmid': 251693058,	#60.34.2
			'type': 3,	#U64
			'sem': 3,
			'units': 'Kbyte',
			'indom': 251658258},	#60.18
		'files_used': {
			'name': 'tmpfs.usedfiles',
			'pmid': 251693061,	#60.34.5
			'type': 1,	#U32
			'sem': 3,
			'units': '',
			'indom': 251658258},	#60.18
	},
	'vfs': {
		'dentry_use': {
			'name': 'vfs.dentry.count',
			'pmid': 251685893,	#60.27.5
			'type': 0,	#32
			'sem': 3,
			'units': '',
			'indom': -1},
		'file_use': {
			'name': 'vfs.files.count',
			'pmid': 251685888,	#60.27.0
			'type': 0,	#32
			'sem': 3,
			'units': '',
			'indom': -1},
		'inode_use': {
			'name': 'vfs.inodes.count',
			'pmid': 251685891,	#60.27.3
			'type': 0,	#32
			'sem': 3,
			'units': '',
			'indom': -1},
	},
	'vm': {
		'allocstall': {
			'name': 'mem.vmstat.allocstall',
			'pmid': 251686947,	#60.28.35
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': -1},
		'kswapd_inodesteal': {
			'name': 'mem.vmstat.kswapd_inodesteal',
			'pmid': 251686945,	#60.28.33
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': -1},
		'kswapd_steal': {
			'name': 'mem.vmstat.kswapd_steal',
			'pmid': 251686944,	#60.28.32
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': -1},
		'pageoutrun': {
			'name': 'mem.vmstat.pageoutrun',
			'pmid': 251686946,	#60.28.34
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': -1},
		'pgactivate': {
			'name': 'mem.vmstat.pgactivate',
			'pmid': 251686926,	#60.28.14
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': -1},
		'pgalloc_normal': {
			'name': 'mem.vmstat.pgalloc_normal',
			'pmid': 251686923,	#60.28.11
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': -1},
		'pgdeactivate': {
			'name': 'mem.vmstat.pgdeactivate',
			'pmid': 251686927,	#60.28.15
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': -1},
		'pgfault': {
			'name': 'mem.vmstat.pgfault',
			'pmid': 251686928,	#60.28.16
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': -1},
		'pgfree': {
			'name': 'mem.vmstat.pgfree',
			'pmid': 251686925,	#60.28.13
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': -1},
		'pginodesteal': {
			'name': 'mem.vmstat.pginodesteal',
			'pmid': 251686942,	#60.28.30
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': -1},
		'pgmajfault': {
			'name': 'mem.vmstat.pgmajfault',
			'pmid': 251686929,	#60.28.17
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': -1},
		'pgpgin': {
			'name': 'mem.vmstat.pgpgin',
			'pmid': 251686918,	#60.28.6
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': -1},
		'pgpgout': {
			'name': 'mem.vmstat.pgpgout',
			'pmid': 251686919,	#60.28.7
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': -1},
		'pgrefill_normal': {
			'name': 'mem.vmstat.pgrefill_normal',
			'pmid': 251686931,	#60.28.19
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': -1},
		'pgrotated': {
			'name': 'mem.vmstat.pgrotated',
			'pmid': 251686948,	#60.28.36
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': -1},
		'pgscan_direct_normal': {
			'name': 'mem.vmstat.pgscan_direct_normal',
			'pmid': 251686940,	#60.28.28
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': -1},
		'pgscan_kswapd_normal': {
			'name': 'mem.vmstat.pgscan_kswapd_normal',
			'pmid': 251686937,	#60.28.25
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': -1},
		'pgsteal_normal': {
			'name': 'mem.vmstat.pgsteal_normal',
			'pmid': 251686934,	#60.28.22
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': -1},
		'pswpin': {
			'name': 'mem.vmstat.pswpin',
			'pmid': 251686920,	#60.28.8
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': -1},
		'pswpout': {
			'name': 'mem.vmstat.pswpout',
			'pmid': 251686921,	#60.28.9
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': -1},
		'slabs_scanned': {
			'name': 'mem.vmstat.slabs_scanned',
			'pmid': 251686943,	#60.28.31
			'type': 3,	#U64
			'sem': 1,
			'units': 'count',
			'indom': -1},
	},
	'amd64_core': {
		'DCSF': {
			'name': 'perfevent.hwcounters.DATA_CACHE_REFILLS_SYSTEM',
			'pmid': pmi.pmiLogImport.pmiID(127, 1, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 0)},
		'SSE_FLOPS': {
			'name': 'perfevent.hwcounters.RETIRED_SSE_OPERATIONS_ALL',
			'pmid': pmi.pmiLogImport.pmiID(127, 2, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 1)},
		'USER': {
			'name': 'perfevent.hwcounters.CPU_CLK_UNHALTED_u',
			'pmid': pmi.pmiLogImport.pmiID(127, 3, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 2)},
	},
	'amd64_sock': {
		'DRAM': {
			'name': 'perfevent.hwcounters.DRAM_ACCESSES_PAGE_HIT_MISS_CONFLICT',
			'pmid': pmi.pmiLogImport.pmiID(127, 4, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 3)},
		'HT0': {
			'name': 'perfevent.hwcounters.HYPERTRANSPORT_LINK0_COMMAND_DWORD_SENT_DATA_DWORD_SENT_BUFFER_RELEASE_DWORD_SENT_ADDRESS_EXT_DWORD_SENT_PER_PACKET_CRC_SENT',
			'pmid': pmi.pmiLogImport.pmiID(127, 5, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 4)},
		'HT1': {
			'name': 'perfevent.hwcounters.HYPERTRANSPORT_LINK1_COMMAND_DWORD_SENT_DATA_DWORD_SENT_BUFFER_RELEASE_DWORD_SENT_ADDRESS_EXT_DWORD_SENT_PER_PACKET_CRC_SENT',
			'pmid': pmi.pmiLogImport.pmiID(127, 6, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 5)},
		'HT2': {
			'name': 'perfevent.hwcounters.HYPERTRANSPORT_LINK2_COMMAND_DWORD_SENT_DATA_DWORD_SENT_BUFFER_RELEASE_DWORD_SENT_ADDRESS_EXT_DWORD_SENT_PER_PACKET_CRC_SENT',
			'pmid': pmi.pmiLogImport.pmiID(127, 7, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 6)},
	},
	'intel_pmc3': {
		'CLOCKS_UNHALTED_CORE': {
			'name': 'perfevent.hwcounters.UNHALTED_CORE_CYCLES',
			'pmid': pmi.pmiLogImport.pmiID(127, 8, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 7)},
		'CLOCKS_UNHALTED_REF': {
			'name': 'perfevent.hwcounters.UNHALTED_REFERENCE_CYCLES',
			'pmid': pmi.pmiLogImport.pmiID(127, 9, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 8)},
		'FP_COMP_OPS_EXE_SSE': {
			'name': 'perfevent.hwcounters.FP_COMP_OPS_EXE_SSE_FP',
			'pmid': pmi.pmiLogImport.pmiID(127, 10, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 9)},
		'FP_COMP_OPS_EXE_X87': {
			'name': 'perfevent.hwcounters.FP_COMP_OPS_EXE_X87',
			'pmid': pmi.pmiLogImport.pmiID(127, 11, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 10)},
		'INSTRUCTIONS_RETIRED': {
			'name': 'perfevent.hwcounters.INSTRUCTIONS_RETIRED',
			'pmid': pmi.pmiLogImport.pmiID(127, 12, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 11)},
		'MEM_LOAD_RETIRED_L1D_HIT': {
			'name': 'perfevent.hwcounters.MEM_LOAD_RETIRED_L1D_HIT',
			'pmid': pmi.pmiLogImport.pmiID(127, 13, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 12)},
		'MEM_UNCORE_RETIRED_LOCAL_DRAM': {
			'name': 'perfevent.hwcounters.MEM_UNCORE_RETIRED_OTHER_LLC_MISS',
			'pmid': pmi.pmiLogImport.pmiID(127, 14, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 13)},
		'MEM_UNCORE_RETIRED_REMOTE_DRAM': {
			'name': 'perfevent.hwcounters.MEM_UNCORE_RETIRED_REMOTE_DRAM',
			'pmid': pmi.pmiLogImport.pmiID(127, 15, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 14)},
	},
	'intel_snb': {
		'CLOCKS_UNHALTED_CORE': {
			'name': 'perfevent.hwcounters.UNHALTED_CORE_CYCLES',
			'pmid': pmi.pmiLogImport.pmiID(127, 16, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 15)},
		'CLOCKS_UNHALTED_REF': {
			'name': 'perfevent.hwcounters.UNHALTED_REFERENCE_CYCLES',
			'pmid': pmi.pmiLogImport.pmiID(127, 17, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 16)},
		'INSTRUCTIONS_RETIRED': {
			'name': 'perfevent.hwcounters.INSTRUCTION_RETIRED',
			'pmid': pmi.pmiLogImport.pmiID(127, 18, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 17)},
		'LOAD_L1D_ALL': {
			'name': 'perfevent.hwcounters.L1D_REPLACEMENT',
			'pmid': pmi.pmiLogImport.pmiID(127, 19, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 18)},
		'LOAD_OPS_ALL': {
			'name': 'perfevent.hwcounters.MEM_UOPS_RETIRED_ALL_LOADS',
			'pmid': pmi.pmiLogImport.pmiID(127, 20, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 19)},
		'LOAD_OPS_L1_HIT': {
			'name': 'perfevent.hwcounters.MEM_LOAD_UOPS_RETIRED_L1_HIT',
			'pmid': pmi.pmiLogImport.pmiID(127, 21, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 20)},
		'LOAD_OPS_L2_HIT': {
			'name': 'perfevent.hwcounters.MEM_LOAD_UOPS_RETIRED_L2_HIT',
			'pmid': pmi.pmiLogImport.pmiID(127, 22, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 21)},
		'LOAD_OPS_LLC_HIT': {
			'name': 'perfevent.hwcounters.MEM_LOAD_UOPS_RETIRED_HIT_LFB',
			'pmid': pmi.pmiLogImport.pmiID(127, 23, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 22)},
		'SIMD_DOUBLE_256': {
			'name': 'perfevent.hwcounters.SIMD_FP_256_PACKED_DOUBLE',
			'pmid': pmi.pmiLogImport.pmiID(127, 24, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 23)},
		'SSE_DOUBLE_PACKED': {
			'name': 'perfevent.hwcounters.FP_COMP_OPS_EXE_SSE_FP_PACKED_DOUBLE',
			'pmid': pmi.pmiLogImport.pmiID(127, 25, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 24)},
		'SSE_DOUBLE_SCALAR': {
			'name': 'perfevent.hwcounters.FP_COMP_OPS_EXE_SSE_SCALAR_DOUBLE',
			'pmid': pmi.pmiLogImport.pmiID(127, 26, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 25)},
	},
	'intel_snb_cbo': {
		'CLOCK_TICKS': {
			'name': 'perfevent.hwcounters.snbep_unc_cbo%d__UNC_C_CLOCKTICKS',
			'pmid': pmi.pmiLogImport.pmiID(127, 27, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 26)},
		'COUNTER0_OCCUPANCY': {
			'name': 'perfevent.hwcounters.snbep_unc_cbo%d__UNC_C_COUNTER0_OCCUPANCY_e_t_1',
			'pmid': pmi.pmiLogImport.pmiID(127, 28, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 27)},
		'LLC_LOOKUP': {
			'name': 'perfevent.hwcounters.snbep_unc_cbo%d__UNC_C_LLC_LOOKUP_DATA_READ',
			'pmid': pmi.pmiLogImport.pmiID(127, 29, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 28)},
		'RxR_OCCUPANCY': {
			'name': 'perfevent.hwcounters.snbep_unc_cbo%d__UNC_C_RXR_OCCUPANCY_IRQ',
			'pmid': pmi.pmiLogImport.pmiID(127, 30, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 29)},
	},
	'intel_snb_hau': {
		'CLOCKTICKS': {
			'name': 'perfevent.hwcounters.snbep_unc_ha__UNC_H_CLOCKTICKS',
			'pmid': pmi.pmiLogImport.pmiID(127, 31, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 30)},
		'IMC_WRITES': {
			'name': 'perfevent.hwcounters.snbep_unc_ha__UNC_H_IMC_WRITES_ALL',
			'pmid': pmi.pmiLogImport.pmiID(127, 32, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 31)},
		'READ_REQUESTS': {
			'name': 'perfevent.hwcounters.snbep_unc_ha__UNC_H_REQUESTS_READS',
			'pmid': pmi.pmiLogImport.pmiID(127, 33, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 32)},
		'WRITE_REQUESTS': {
			'name': 'perfevent.hwcounters.snbep_unc_ha__UNC_H_REQUESTS_WRITES',
			'pmid': pmi.pmiLogImport.pmiID(127, 34, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 33)},
	},
	'intel_snb_imc': {
		'ACT_COUNT': {
			'name': 'perfevent.hwcounters.snbep_unc_imc%d__UNC_M_ACT_COUNT',
			'pmid': pmi.pmiLogImport.pmiID(127, 35, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 34)},
		'CAS_READS': {
			'name': 'perfevent.hwcounters.snbep_unc_imc%d__UNC_M_CAS_COUNT_RD',
			'pmid': pmi.pmiLogImport.pmiID(127, 36, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 35)},
		'CAS_WRITES': {
			'name': 'perfevent.hwcounters.snbep_unc_imc%d__UNC_M_CAS_COUNT_WR',
			'pmid': pmi.pmiLogImport.pmiID(127, 37, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 36)},
		'CYCLES': {
			'name': 'perfevent.hwcounters.snbep_unc_imc%d__UNC_M_CLOCKTICKS',
			'pmid': pmi.pmiLogImport.pmiID(127, 38, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 37)},
		'PRE_COUNT_MISS': {
			'name': 'perfevent.hwcounters.snbep_unc_imc%d__UNC_M_PRE_COUNT_PAGE_MISS',
			'pmid': pmi.pmiLogImport.pmiID(127, 39, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 38)},
	},
	'intel_snb_pcu': {
		'C3_CYCLES': {
			'name': 'perfevent.hwcounters.snbep_unc_pcu__UNC_P_CLOCKTICKS_C3',
			'pmid': pmi.pmiLogImport.pmiID(127, 40, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 39)},
		'C6_CYCLES': {
			'name': 'perfevent.hwcounters.snbep_unc_pcu__UNC_P_CLOCKTICKS_C6',
			'pmid': pmi.pmiLogImport.pmiID(127, 41, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 40)},
		'MAX_POWER_CYCLES': {
			'name': 'perfevent.hwcounters.snbep_unc_pcu__UNC_P_FREQ_MAX_POWER_CYCLES',
			'pmid': pmi.pmiLogImport.pmiID(127, 42, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 41)},
		'MAX_TEMP_CYCLES': {
			'name': 'perfevent.hwcounters.snbep_unc_pcu__UNC_P_FREQ_MAX_LIMIT_THERMAL_CYCLES',
			'pmid': pmi.pmiLogImport.pmiID(127, 43, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 42)},
		'MIN_IO_CYCLES': {
			'name': 'perfevent.hwcounters.snbep_unc_pcu__UNC_P_FREQ_MIN_IO_P_CYCLES',
			'pmid': pmi.pmiLogImport.pmiID(127, 44, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 43)},
		'MIN_SNOOP_CYCLES': {
			'name': 'perfevent.hwcounters.snbep_unc_pcu__UNC_P_FREQ_MIN_PERF_P_CYCLES',
			'pmid': pmi.pmiLogImport.pmiID(127, 45, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 44)},
	},
	'intel_snb_qpi': {
		'G1_DRS_DATA': {
			'name': 'perfevent.hwcounters.snbep_unc_qpi%d__UNC_Q_RXL_FLITS_G1_DRS_DATA',
			'pmid': pmi.pmiLogImport.pmiID(127, 46, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 45)},
		'G2_NCB_DATA': {
			'name': 'perfevent.hwcounters.snbep_unc_qpi%d__UNC_Q_RXL_FLITS_G2_NCB_DATA',
			'pmid': pmi.pmiLogImport.pmiID(127, 47, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 46)},
		'TxL_FLITS_G1_HOM': {
			'name': 'perfevent.hwcounters.snbep_unc_qpi%d__UNC_Q_TXL_FLITS_G1_HOM_NONREQ',
			'pmid': pmi.pmiLogImport.pmiID(127, 48, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 47)},
		'TxL_FLITS_G1_SNP': {
			'name': 'perfevent.hwcounters.snbep_unc_qpi%d__UNC_Q_TXL_FLITS_G1_SNP',
			'pmid': pmi.pmiLogImport.pmiID(127, 49, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 48)},
	},
	'intel_snb_r2pci': {
		'ACKNOWLEDGED_USED': {
			'name': 'perfevent.hwcounters.snbep_unc_r2pcie__UNC_R2_RING_AK_USED_ANY',
			'pmid': pmi.pmiLogImport.pmiID(127, 50, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 49)},
		'ADDRESS_USED': {
			'name': 'perfevent.hwcounters.snbep_unc_r2pcie__UNC_R2_RING_AD_USED_ANY',
			'pmid': pmi.pmiLogImport.pmiID(127, 51, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 50)},
		'CLOCKTICKS': {
			'name': 'perfevent.hwcounters.snbep_unc_r2pcie__UNC_R2_CLOCKTICKS',
			'pmid': pmi.pmiLogImport.pmiID(127, 52, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 51)},
		'DATA_USED': {
			'name': 'perfevent.hwcounters.snbep_unc_r2pcie__UNC_R2_RING_BL_USED_ANY',
			'pmid': pmi.pmiLogImport.pmiID(127, 53, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 52)},
		'TRANSMITS': {
			'name': 'perfevent.hwcounters.snbep_unc_r2pcie__UNC_R2_TXR_INSERTS',
			'pmid': pmi.pmiLogImport.pmiID(127, 54, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 53)},
	},
	'intel_uncore': {
		'CLOCKS_UNCORE': {
			'name': 'perfevent.hwcounters.UNC_CLK_UNHALTED',
			'pmid': pmi.pmiLogImport.pmiID(127, 55, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 54)},
		'L3_HITS_PROBE': {
			'name': 'perfevent.hwcounters.UNC_LLC_HITS_PROBE',
			'pmid': pmi.pmiLogImport.pmiID(127, 56, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 55)},
		'L3_HITS_READ': {
			'name': 'perfevent.hwcounters.UNC_LLC_HITS_READ',
			'pmid': pmi.pmiLogImport.pmiID(127, 57, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 56)},
		'L3_HITS_WRITE': {
			'name': 'perfevent.hwcounters.UNC_LLC_HITS_WRITE',
			'pmid': pmi.pmiLogImport.pmiID(127, 58, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 57)},
		'L3_LINES_IN_ANY': {
			'name': 'perfevent.hwcounters.UNC_LLC_LINES_IN_ANY',
			'pmid': pmi.pmiLogImport.pmiID(127, 59, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 58)},
		'L3_LINES_OUT_ANY': {
			'name': 'perfevent.hwcounters.UNC_LLC_LINES_OUT_ANY',
			'pmid': pmi.pmiLogImport.pmiID(127, 60, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 59)},
		'L3_MISS_PROBE': {
			'name': 'perfevent.hwcounters.UNC_LLC_MISS_PROBE',
			'pmid': pmi.pmiLogImport.pmiID(127, 61, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 60)},
		'L3_MISS_READ': {
			'name': 'perfevent.hwcounters.UNC_LLC_MISS_READ',
			'pmid': pmi.pmiLogImport.pmiID(127, 62, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 61)},
		'L3_MISS_WRITE': {
			'name': 'perfevent.hwcounters.UNC_LLC_MISS_WRITE',
			'pmid': pmi.pmiLogImport.pmiID(127, 63, 0),
			'type': 3,
			'sem': 1,
			'units': '',
			'inst_pattern': '%d',
			'iname_pattern': 'cpu%d',
			'indom': pmi.pmiLogImport.pmiInDom(127, 62)},
	},
}
