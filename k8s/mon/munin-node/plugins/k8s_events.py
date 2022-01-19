# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

sts = dict(
	apiserver_init_events_total = dict(),
)

def parse(name: str, meta: dict, value: float):
	global sts
	if sts.get(name, None) is not None:
		resource = meta.get('resource', None)
		sts[name][resource] = value
		return True
	return False

def _print(*args):
	print(*args)

def config(sts):
	mon.dbg('config k8s_events')
	cluster = mon.cluster()
	_print('multigraph k8s_events')
	_print(f"graph_title {cluster} kubernetes events")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category k8s')
	_print('graph_vlabel number')
	_print('graph_scale yes')
	color = 0
	for event in sorted(sts['apiserver_init_events_total'].keys()):
		eid = mon.cleanfn(event)
		_print(f"event_{eid}.label {event}")
		_print(f"event_{eid}.colour COLOUR{color}")
		_print(f"event_{eid}.draw AREA")
		_print(f"event_{eid}.min 0")
		_print(f"event_{eid}.type DERIVE")
		_print(f"event_{eid}.cdef event_{eid},1000,/")
		color = mon.color(color)

def report(sts):
	mon.dbg('report k8s_events')
	_print('multigraph k8s_events')
	for event in sorted(sts['apiserver_init_events_total'].keys()):
		eid = mon.cleanfn(event)
		val = mon.derive(sts['apiserver_init_events_total'][event])
		_print(f"event_{eid}.value", val)
