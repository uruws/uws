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

def __parse(kind, key, value):
	mon.dbg('parse nginx_proc:', kind, key)
	if kind == 'uptime':
		sts[kind] = time() - value
	elif kind == 'requests':
		sts[kind] = value
	else:
		sts[kind][key] = value
	return True

def parse(name, meta, value):
	# cpu
	if name == 'nginx_ingress_controller_nginx_process_cpu_seconds_total':
		return __parse('cpu', 'controller', value)
	elif name == 'process_cpu_seconds_total':
		return __parse('cpu', 'total', value)
	# mem
	elif name == 'nginx_ingress_controller_nginx_process_resident_memory_bytes':
		return __parse('mem', 'resident', value)
	elif name == 'nginx_ingress_controller_nginx_process_virtual_memory_bytes':
		return __parse('mem', 'virtual', value)
	# uptime
	elif name == 'process_start_time_seconds':
		return __parse('uptime', 'since', value)
	# requests
	elif name == 'nginx_ingress_controller_nginx_process_requests_total':
		return __parse('requests', 'total', value)
	# read
	elif name == 'nginx_ingress_controller_nginx_process_read_bytes_total':
		return __parse('byte', 'read', value)
	# write
	elif name == 'nginx_ingress_controller_nginx_process_write_bytes_total':
		return __parse('byte', 'write', value)
	return False

def config(sts):
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
	print('controller.cdef controller,1000,/')
	print('total.label total')
	print('total.colour COLOUR1')
	print('total.type DERIVE')
	print('total.min 0')
	print('total.cdef total,1000,/')
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
	print('graph_vlabel hours')
	print('graph_scale no')
	print('uptime.label uptime')
	print('uptime.colour COLOUR0')
	print('uptime.draw AREA')
	print('uptime.min 0')
	# requests total
	print('multigraph nginx_proc_requests')
	print('graph_title Requests total')
	print('graph_args --base 1000 -l 0')
	print('graph_category nginx_req')
	print('graph_vlabel number')
	print('graph_scale yes')
	print('requests.label requests')
	print('requests.colour COLOUR0')
	print('requests.min 0')
	# requests counter
	print('multigraph nginx_proc_requests.counter')
	print('graph_title Requests')
	print('graph_args --base 1000 -l 0')
	print('graph_category nginx_req')
	print('graph_vlabel number per second')
	print('graph_scale yes')
	print('requests.label requests')
	print('requests.colour COLOUR0')
	print('requests.type DERIVE')
	print('requests.min 0')
	print('requests.cdef requests,1000,/')
	# bytes total
	print('multigraph nginx_proc_bytes')
	print('graph_title Bytes read/write total')
	print('graph_args --base 1024 -l 0')
	print('graph_category nginx')
	print('graph_vlabel read(-)/write(+) per second')
	print('graph_scale yes')
	print('read.label bytes')
	print('read.graph no')
	print('read.min 0')
	print('write.label bytes')
	print('write.negative read')
	print('write.min 0')
	# bytes counter
	print('multigraph nginx_proc_bytes.counter')
	print('graph_title Bytes read/write')
	print('graph_args --base 1024 -l 0')
	print('graph_category nginx')
	print('graph_vlabel read(-)/write(+) per second')
	print('graph_scale yes')
	print('read.label bytes')
	print('read.type DERIVE')
	print('read.graph no')
	print('read.min 0')
	print('read.cdef read,1000,/')
	print('write.label bytes')
	print('write.type DERIVE')
	print('write.negative read')
	print('write.min 0')
	print('write.cdef write,1000,/')

def report(sts):
	mon.dbg('report nginx_proc')
	# cpu
	print('multigraph nginx_proc_cpu')
	print('controller.value', mon.derive(sts['cpu']['controller']))
	print('total.value', mon.derive(sts['cpu']['total']))
	# mem
	print('multigraph nginx_proc_mem')
	print('resident.value', sts['mem']['resident'])
	print('virtual.value', sts['mem']['virtual'])
	# uptime
	print('multigraph nginx_proc_uptime')
	print('uptime.value', sts['uptime'] / 3600.0)
	# requests total
	print('multigraph nginx_proc_requests')
	print('requests.value', sts['requests'])
	# requests counter
	print('multigraph nginx_proc_requests.counter')
	print('requests.value', mon.derive(sts['requests']))
	# bytes total
	print('multigraph nginx_proc_bytes')
	print('write.value', sts['byte']['write'])
	print('read.value', sts['byte']['read'])
	# bytes counter
	print('multigraph nginx_proc_bytes.counter')
	print('write.value', mon.derive(sts['byte']['write']))
	print('read.value', mon.derive(sts['byte']['read']))
