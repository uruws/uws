# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from typing import Any

import mon

sts: dict[str, Any] = dict(
	aggregator_unavailable_apiservice_total = dict(),
	total = 0.0,
)

def parse(name: str, meta: dict, value: float) -> bool:
	global sts
	if sts.get(name, None) is not None:
		reason = meta.get('reason', None)
		n = meta.get('name', None)
		if sts[name].get(reason, None) is None:
			sts[name][reason] = dict()
		sts[name][reason][n] = value
		sts['total'] += value
		return True
	return False

def _print(*args):
	print(*args)

def config(k8s: dict[str, Any]):
	mon.dbg('config k8s_service')
	cluster = mon.cluster()
	total = k8s['aggregator_unavailable_apiservice_total']
	_print('multigraph k8s_service')
	_print(f"graph_title {cluster} k8s api service unavailable")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category k8s')
	_print('graph_vlabel number')
	_print('graph_scale yes')
	_print('a_total.label total')
	_print('a_total.colour 000000')
	_print('a_total.min 0')
	_print('a_total.type DERIVE')
	_print('a_total.cdef a_total,1000,/')
	color = 0
	for reason in sorted(total.keys()):
		for name in sorted(total[reason].keys()):
			rid = mon.cleanfn(f"{reason}_{name}")
			_print(f"z_{rid}.label {reason} {name}")
			_print(f"z_{rid}.colour COLOUR{color}")
			_print(f"z_{rid}.min 0")
			_print(f"z_{rid}.type DERIVE")
			_print(f"z_{rid}.cdef z_{rid},1000,/")
			color = mon.color(color)

def report(k8s: dict[str, Any]):
	mon.dbg('report k8s_service')
	total = k8s['aggregator_unavailable_apiservice_total']
	_print('multigraph k8s_service')
	_print('a_total.value', mon.derive(k8s.get('total', 'U')))
	for reason in sorted(total.keys()):
		for name in sorted(total[reason].keys()):
			rid = mon.cleanfn(f"{reason}_{name}")
			_print(f"z_{rid}.value", mon.derive(total[reason][name]))
