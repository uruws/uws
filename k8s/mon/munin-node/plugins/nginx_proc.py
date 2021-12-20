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

CPU_CONTROLLER = 'nginx_ingress_controller_nginx_process_cpu_seconds_total'
CPU_TOTAL = 'process_cpu_seconds_total'

def parse(name, meta, value):
	# cpu
	if name == CPU_CONTROLLER:
		return __parse('cpu', 'controller', value)
	elif name == CPU_TOTAL:
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

def _print(*args):
	print(*args)

def config(sts):
	mon.dbg('config nginx_proc')
	# cpu
	_print('multigraph nginx_proc_cpu')
	_print('graph_title CPU usage')
	_print('graph_args --base 1000 -l 0')
	_print('graph_category nginx')
	_print('graph_vlabel time per second')
	_print('graph_scale no')
	_print('controller.label controller')
	_print('controller.colour COLOUR0')
	_print('controller.type DERIVE')
	_print('controller.min 0')
	_print('controller.cdef controller,1000,/')
	_print('total.label total')
	_print('total.colour COLOUR1')
	_print('total.type DERIVE')
	_print('total.min 0')
	_print('total.cdef total,1000,/')
	# mem
	_print('multigraph nginx_proc_mem')
	_print('graph_title Memory usage')
	_print('graph_args --base 1024 -l 0')
	_print('graph_category nginx')
	_print('graph_vlabel bytes')
	_print('graph_scale yes')
	_print('resident.label resident')
	_print('resident.colour COLOUR0')
	_print('resident.draw AREA')
	_print('resident.min 0')
	_print('virtual.label virtual')
	_print('virtual.colour COLOUR1')
	_print('virtual.draw AREA')
	_print('virtual.min 0')
	# uptime
	_print('multigraph nginx_proc_uptime')
	_print('graph_title Uptime')
	_print('graph_args --base 1000 -l 0')
	_print('graph_category nginx')
	_print('graph_vlabel hours')
	_print('graph_scale no')
	_print('uptime.label uptime')
	_print('uptime.colour COLOUR0')
	_print('uptime.draw AREA')
	_print('uptime.min 0')
	# requests total
	_print('multigraph nginx_proc_requests')
	_print('graph_title Requests total')
	_print('graph_args --base 1000 -l 0')
	_print('graph_category nginx_req')
	_print('graph_vlabel number')
	_print('graph_scale yes')
	_print('requests.label requests')
	_print('requests.colour COLOUR0')
	_print('requests.min 0')
	# requests counter
	_print('multigraph nginx_proc_requests.counter')
	_print('graph_title Requests')
	_print('graph_args --base 1000 -l 0')
	_print('graph_category nginx_req')
	_print('graph_vlabel number per second')
	_print('graph_scale yes')
	_print('requests.label requests')
	_print('requests.colour COLOUR0')
	_print('requests.type DERIVE')
	_print('requests.min 0')
	_print('requests.cdef requests,1000,/')
	# bytes total
	_print('multigraph nginx_proc_bytes')
	_print('graph_title Bytes read/write total')
	_print('graph_args --base 1024 -l 0')
	_print('graph_category nginx')
	_print('graph_vlabel read(-)/write(+) per second')
	_print('graph_scale yes')
	_print('read.label bytes')
	_print('read.graph no')
	_print('read.min 0')
	_print('write.label bytes')
	_print('write.negative read')
	_print('write.min 0')
	# bytes counter
	_print('multigraph nginx_proc_bytes.counter')
	_print('graph_title Bytes read/write')
	_print('graph_args --base 1024 -l 0')
	_print('graph_category nginx')
	_print('graph_vlabel read(-)/write(+) per second')
	_print('graph_scale yes')
	_print('read.label bytes')
	_print('read.type DERIVE')
	_print('read.graph no')
	_print('read.min 0')
	_print('read.cdef read,1000,/')
	_print('write.label bytes')
	_print('write.type DERIVE')
	_print('write.negative read')
	_print('write.min 0')
	_print('write.cdef write,1000,/')

def report(sts):
	mon.dbg('report nginx_proc')
	# cpu
	_print('multigraph nginx_proc_cpu')
	_print('controller.value', mon.derive(sts['cpu']['controller']))
	_print('total.value', mon.derive(sts['cpu']['total']))
	# mem
	_print('multigraph nginx_proc_mem')
	_print('resident.value', sts['mem']['resident'])
	_print('virtual.value', sts['mem']['virtual'])
	# uptime
	_print('multigraph nginx_proc_uptime')
	_print('uptime.value', sts['uptime'] / 3600.0)
	# requests total
	_print('multigraph nginx_proc_requests')
	_print('requests.value', sts['requests'])
	# requests counter
	_print('multigraph nginx_proc_requests.counter')
	_print('requests.value', mon.derive(sts['requests']))
	# bytes total
	_print('multigraph nginx_proc_bytes')
	_print('write.value', sts['byte']['write'])
	_print('read.value', sts['byte']['read'])
	# bytes counter
	_print('multigraph nginx_proc_bytes.counter')
	_print('write.value', mon.derive(sts['byte']['write']))
	_print('read.value', mon.derive(sts['byte']['read']))
