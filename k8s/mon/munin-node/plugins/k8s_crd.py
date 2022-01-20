# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

sts = dict(
	apiextensions_openapi_v2_regeneration_count = dict(),
	total = 0,
)

def parse(name: str, meta: dict, value: float):
	global sts
	if sts.get(name, None) is not None:
		reason = meta.get('reason', None)
		crd = meta.get('crd', None)
		if sts[name].get(reason, None) is None:
			sts[name][reason] = dict()
		sts[name][reason][crd] = value
		sts['total'] += value
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

def report(sts):
	mon.dbg('report k8s_crd')
	total = sts['apiextensions_openapi_v2_regeneration_count']
	_print('multigraph k8s_crd')
	_print('a_total.value', mon.derive(sts.get('total', 'U')))
	for reason in sorted(total.keys()):
		for name in sorted(total[reason].keys()):
			rid = mon.cleanfn(f"{reason}_{name}")
			_print(f"z_{rid}.value", mon.derive(total[reason][name]))
