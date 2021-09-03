# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

from time import time

sts = dict(
	cpu = dict(
		controller = 'U',
		total = 'U',
	),
	mem = dict(
		resident = 'U',
		virtual = 'U',
	),
	uptime = 'U',
	requests = 'U',
	byte = dict(
		read = 'U',
		write = 'U',
	),
)

def parse(kind, key, value):
	mon.dbg('parse nginx_proc:', kind, key)
	if kind == 'uptime':
		sts[kind] = time() - value
	elif kind == 'requests':
		sts[kind] = value
	else:
		sts[kind][key] = value

def config():
	mon.dbg('config nginx_proc')
	# cpu
	print('multigraph nginx_proc_cpu')
	print('graph_title CPU usage')
	print('graph_args --base 1000 -l 0')
	print('graph_category nginx')
	print('graph_vlabel time per second')
	print('graph_scale no')
	print('controller.label controller')
	print('controller.colour COLOUR0')
	print('controller.type DERIVE')
	print('controller.min 0')
	print('total.label total')
	print('total.colour COLOUR1')
	print('total.type DERIVE')
	print('total.min 0')
	# mem
	print('multigraph nginx_proc_mem')
	print('graph_title Memory usage')
	print('graph_args --base 1024 -l 0')
	print('graph_category nginx')
	print('graph_vlabel bytes')
	print('graph_scale yes')
	print('resident.label resident')
	print('resident.colour COLOUR0')
	print('resident.draw AREA')
	print('resident.min 0')
	print('virtual.label virtual')
	print('virtual.colour COLOUR1')
	print('virtual.draw AREA')
	print('virtual.min 0')
	# uptime
	print('multigraph nginx_proc_uptime')
	print('graph_title Uptime')
	print('graph_args --base 1000 -l 0')
	print('graph_category nginx')
	print('graph_vlabel seconds')
	print('graph_scale no')
	print('uptime.label uptime')
	print('uptime.colour COLOUR0')
	print('uptime.draw AREA')
	print('uptime.min 0')
	# requests counter
	print('multigraph nginx_proc_requests_counter')
	print('graph_title Requests counter')
	print('graph_args --base 1000 -l 0')
	print('graph_category nginx')
	print('graph_vlabel number per second')
	print('graph_scale no')
	print('requests.label requests')
	print('requests.colour COLOUR0')
	print('requests.type DERIVE')
	print('requests.min 0')
	# requests total
	print('multigraph nginx_proc_requests_total')
	print('graph_title Requests total')
	print('graph_args --base 1000 -l 0')
	print('graph_category nginx')
	print('graph_vlabel number')
	print('graph_scale yes')
	print('requests.label requests')
	print('requests.colour COLOUR0')
	print('requests.min 0')
	# bytes read/write
	print('multigraph nginx_proc_bytes')
	print('graph_title Bytes read/write')
	print('graph_args --base 1024 -l 0')
	print('graph_category nginx')
	print('graph_vlabel read(-)/write(+) per second')
	print('graph_scale yes')
	print('read.label bytes')
	print('read.type DERIVE')
	print('read.graph no')
	print('read.min 0')
	print('write.label bytes')
	print('write.type DERIVE')
	print('write.negative read')
	print('write.min 0')

def report(sts):
	mon.dbg('report nginx_proc')
	# cpu
	print('multigraph nginx_proc_cpu')
	print('controller.value', sts['cpu']['controller'])
	print('total.value', sts['cpu']['total'])
	# mem
	print('multigraph nginx_proc_mem')
	print('resident.value', sts['mem']['resident'])
	print('virtual.value', sts['mem']['virtual'])
	# uptime
	print('multigraph nginx_proc_uptime')
	print('uptime.value', sts['uptime'])
	# requests counter
	print('multigraph nginx_proc_requests_counter')
	print('requests.value', sts['requests'])
	# requests total
	print('multigraph nginx_proc_requests_total')
	print('requests.value', sts['requests'])
	# bytes read/write
	print('multigraph nginx_proc_bytes')
	print('write.value', sts['byte']['write'])
	print('read.value', sts['byte']['read'])
