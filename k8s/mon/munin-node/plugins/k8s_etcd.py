# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from typing import Any

import mon

sts: dict[str, Any] = dict(
	etcd_db_total_size_in_bytes = 'U',
	etcd_db_endpoint = None,
)

def parse(name: str, meta: dict, value: float) -> bool:
	global sts
	if sts.get(name, None) is not None:
		sts[name] = value
		sts['etcd_db_endpoint'] = meta.get('endpoint', None)
		return True
	return False

def _print(*args):
	print(*args)

def config(sts: dict[str, Any]):
	mon.dbg('config k8s_etcd')
	cluster = mon.cluster()
	_print('multigraph k8s_etcd')
	_print(f"graph_title {cluster} k8s apiserver etcd")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category k8s')
	_print('graph_vlabel bytes')
	_print('graph_scale yes')
	_print('db_size.label db size')
	_print('db_size.colour COLOUR0')
	_print('db_size.min 0')
	_print('db_size.draw AREA')
	_print('db_size.info endpoint:', sts['etcd_db_endpoint'])

def report(sts: dict[str, Any]):
	mon.dbg('report k8s_etcd')
	_print('multigraph k8s_etcd')
	_print('db_size.value', sts['etcd_db_total_size_in_bytes'])
