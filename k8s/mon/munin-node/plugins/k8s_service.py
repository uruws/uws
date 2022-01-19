# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

sts = dict(
	aggregator_unavailable_apiservice_total = dict(),
)

def parse(name: str, meta: dict, value: float):
	global sts
	if sts.get(name, None) is not None:
		reason = meta.get('reason', None)
		n = meta.get('name', None)
		if sts[name].get(reason, None) is None:
			sts[name][reason] = dict()
		sts[name][reason][n] = value
		return True
	return False

def _print(*args):
	print(*args)

def config(sts):
	mon.dbg('config k8s_service')
	cluster = mon.cluster()
	total = sts['aggregator_unavailable_apiservice_total']
	_print('multigraph k8s_service')
	_print(f"graph_title {cluster} k8s api service unavailable")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category k8s')
	_print('graph_vlabel number')
	_print('graph_scale yes')
	color = 0
	for reason in sorted(total.keys()):
		for name in sorted(total[reason].keys()):
			rid = mon.cleanfn(f"{reason}_{name}")
			_print(f"{rid}.label {reason} {name}")
			_print(f"{rid}.colour COLOUR{color}")
			_print(f"{rid}.min 0")
			_print(f"{rid}.type DERIVE")
			_print(f"{rid}.cdef errors,1000,/")

def report(sts):
	mon.dbg('report k8s_service')
	total = sts['aggregator_unavailable_apiservice_total']
	_print('multigraph k8s_service')
	for reason in sorted(total.keys()):
		for name in sorted(total[reason].keys()):
			rid = mon.cleanfn(f"{reason}_{name}")
			_print(f"{rid}.value", total[reason][name])
