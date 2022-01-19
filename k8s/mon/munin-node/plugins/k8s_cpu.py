# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

from time import time

sts = dict(
	go_info                    = 'go_version',
	go_goroutines              = 'U',
	go_threads                 = 'U',
	process_cpu_seconds_total  = 'U',
	process_start_time_seconds = 'U',
	process_start_time_hours   = 'U',
)

def parse(name: str, meta: dict, value: float):
	global sts
	if name == 'go_info':
		sts[name] = meta.get('version', 'go_version')
	elif name == 'go_goroutines':
		sts[name] = value
	elif name == 'go_threads':
		sts[name] = value
	elif name == 'process_cpu_seconds_total':
		sts[name] = value
	elif name == 'process_start_time_seconds':
		sts[name] = value
		sts['process_start_time_hours'] = value / 60.0 / 60.0
	else:
		return False
	return True

def _print(*args):
	print(*args)

def config(sts):
	mon.dbg('config k8s_cpu')
	# cpu
	_print('multigraph k8s_cpu')
	_print('graph_title Kubernetes apiserver')
	_print('graph_args --base 1000 -l 0')
	_print('graph_category k8s')
	_print('graph_vlabel number')
	_print('graph_scale yes')
	_print('f0_goroutines.label', sts['go_info'])
	_print('f0_goroutines.colour COLOUR0')
	_print('f0_goroutines.min 0')
	_print('f1_threads.label threads')
	_print('f1_threads.colour COLOUR1')
	_print('f1_threads.min 0')
	# cpu usage
	_print('multigraph k8s_cpu_usage')
	_print('graph_title Kubernetes apiserver CPU')
	_print('graph_args --base 1000 -l 0')
	_print('graph_category k8s')
	_print('graph_vlabel seconds')
	_print('graph_scale yes')
	_print('usage.label usage')
	_print('usage.colour COLOUR0')
	_print('usage.min 0')
	_print('usage.type DERIVE')
	_print('usage.cdef usage,1000,/')

def report(sts):
	mon.dbg('config k8s_cpu')
	# cpu
	_print('multigraph k8s_cpu')
	_print('f0_goroutines.value', sts['go_goroutines'])
	_print('f1_threads.label', sts['go_threads'])
	# cpu usage
	_print('multigraph k8s_cpu_usage')
	_print('usage.value', mon.derive(sts['process_cpu_seconds_total']))
