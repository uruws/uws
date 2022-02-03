# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from typing import Any

import mon

sts: dict[str, Any] = dict(
	apiserver_tls_handshake_errors_total = 'U',
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
	mon.dbg('config k8s_tls')
	cluster = mon.cluster()
	_print('multigraph k8s_tls')
	_print(f"graph_title {cluster} k8s apiserver TLS")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category k8s')
	_print('graph_vlabel number')
	_print('graph_scale yes')
	_print('errors.label errors')
	_print('errors.colour ff0000')
	_print('errors.draw AREA')
	_print('errors.min 0')
	_print('errors.type DERIVE')
	_print('errors.cdef errors,1000,/')

def report(sts: dict[str, Any]):
	mon.dbg('report k8s_tls')
	_print('multigraph k8s_tls')
	_print('errors.value',
		mon.derive(sts['apiserver_tls_handshake_errors_total']))
