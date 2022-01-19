# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

sts = dict(
	etcd_db_total_size_in_bytes = 'U',
)

def parse(name: str, meta: dict, value: float):
	global sts
	if sts.get(name, None) is not None:
		sts[name] = value
		return True
	return False

def _print(*args):
	print(*args)

def config(sts):
	mon.dbg('config k8s_etcd')
	_print('multigraph k8s_etcd')
	_print('graph_title Kubernetes apiserver etcd')
	_print('graph_args --base 1000 -l 0')
	_print('graph_category k8s')
	_print('graph_vlabel bytes')
	_print('graph_scale yes')
	_print('db_size.label db size')
	_print('db_size.colour COLOUR0')
	_print('db_size.min 0')

def report(sts):
	mon.dbg('report k8s_etcd')
	_print('multigraph k8s_etcd')
	_print('db_size.value', sts['etcd_db_total_size_in_bytes'])
