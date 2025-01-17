# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from typing import Any

import mon

sts: dict[str, Any] = dict(
	process_resident_memory_bytes   = 'U',
	process_virtual_memory_bytes    = 'U',
	go_memstats_alloc_bytes         = 'U',
	go_memstats_buck_hash_sys_bytes = 'U',
)

def parse(name: str, meta: dict, value: float) -> bool:
	global sts
	if sts.get(name, None) is not None:
		sts[name] = value
		return True
	return False

def _print(*args):
	print(*args)

def config(sts: dict[str, Any]):
	mon.dbg('config k8s_mem')
	cluster = mon.cluster()
	_print('multigraph k8s_mem')
	_print(f"graph_title {cluster} k8s apiserver memory")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category k8s')
	_print('graph_vlabel bytes')
	_print('graph_scale yes')
	_print('f0_virtual.label virtual')
	_print('f0_virtual.colour COLOUR0')
	_print('f0_virtual.min 0')
	_print('f0_virtual.draw AREA')
	_print('f1_resident.label resident')
	_print('f1_resident.colour COLOUR1')
	_print('f1_resident.min 0')
	_print('f1_resident.draw LINE')
	_print('f2_allocated.label allocated')
	_print('f2_allocated.colour COLOUR2')
	_print('f2_allocated.min 0')
	_print('f2_allocated.draw LINE')
	_print('f3_profiling.label profiling')
	_print('f3_profiling.colour COLOUR3')
	_print('f3_profiling.min 0')
	_print('f3_profiling.draw LINE')

def report(sts: dict[str, Any]):
	mon.dbg('report k8s_mem')
	_print('multigraph k8s_mem')
	_print('f0_virtual.value', sts['process_virtual_memory_bytes'])
	_print('f1_resident.value', sts['process_resident_memory_bytes'])
	_print('f2_allocated.value', sts['go_memstats_alloc_bytes'])
	_print('f3_profiling.value', sts['go_memstats_buck_hash_sys_bytes'])
