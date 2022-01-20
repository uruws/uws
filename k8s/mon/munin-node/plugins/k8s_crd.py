# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

sts = dict(
	apiextensions_openapi_v2_regeneration_count = dict(),
)

def parse(name: str, meta: dict, value: float):
	global sts
	if sts.get(name, None) is not None:
		reason = meta.get('reason', None)
		crd = meta.get('crd', None)
		if sts[name].get(reason, None) is None:
			sts[name][reason] = dict()
		sts[name][reason][crd] = value
		return True
	return False

def _print(*args):
	print(*args)

def config(sts):
	mon.dbg('config k8s_crd')
	cluster = mon.cluster()
	total = sts['apiextensions_openapi_v2_regeneration_count']
	_print('multigraph k8s_crd')
	_print(f"graph_title {cluster} k8s api CRD regeneration")
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
			_print(f"{rid}.cdef {rid},1000,/")
			color = mon.color(color)

def report(sts):
	mon.dbg('report k8s_crd')
	total = sts['apiextensions_openapi_v2_regeneration_count']
	_print('multigraph k8s_crd')
	for reason in sorted(total.keys()):
		for name in sorted(total[reason].keys()):
			rid = mon.cleanfn(f"{reason}_{name}")
			_print(f"{rid}.value", mon.derive(total[reason][name]))
