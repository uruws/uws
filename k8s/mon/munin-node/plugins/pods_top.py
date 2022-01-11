# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def parse(pods):
	mon.dbg('pods_top parse')
	sts = dict(
		info = dict(),
		total = dict(),
	)
	for i in pods.get('items', []):
		ns = i.get('namespace', None)
		n = i.get('name', None)
		c = i.get('cpu', 0)
		m = i.get('mem', 0)
		if ns is not None and n is not None:
			if not sts['info'].get(ns, None):
				sts['info'][ns] = dict()
				sts['total'][ns] = dict(cpu = 0, mem = 0)
			if not sts['info'][ns].get(n, None):
				sts['info'][ns][n] = dict(cpu = 0, mem = 0)
			sts['info'][ns][n]['cpu'] = c
			sts['info'][ns][n]['mem'] = m
			sts['total'][ns]['cpu'] += c
			sts['total'][ns]['mem'] += m
	return sts

def _print(*args):
	print(*args)

def config(sts):
	mon.dbg('pods_top config')
	cluster = mon.cluster()
	total = sts.get('total', {})
	# cpu total
	_print('multigraph pods_top_cpu')
	_print(f"graph_title {cluster} pods CPU")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category top')
	_print('graph_vlabel millicores')
	_print('graph_printf %3.0lf')
	_print('graph_scale yes')
	_print('graph_total total')
	color = 0
	for ns in sorted(total.keys()):
		nsid = mon.cleanfn(ns)
		_print(f"{nsid}.label {ns}")
		_print(f"{nsid}.colour COLOUR{color}")
		_print(f"{nsid}.draw AREASTACK")
		_print(f"{nsid}.min 0")
		color = mon.color(color)
	# mem total
	_print('multigraph pods_top_mem')
	_print(f"graph_title {cluster} pods memory")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category top')
	_print('graph_vlabel MiB')
	_print('graph_printf %3.0lf')
	_print('graph_scale yes')
	_print('graph_total total')
	color = 0
	for ns in sorted(total.keys()):
		nsid = mon.cleanfn(ns)
		_print(f"{nsid}.label {ns}")
		_print(f"{nsid}.colour COLOUR{color}")
		_print(f"{nsid}.draw AREASTACK")
		_print(f"{nsid}.min 0")
		color = mon.color(color)

def report(sts):
	mon.dbg('pods_top report')
	total = sts.get('total', {})
	# cpu total
	_print('multigraph pods_top_cpu')
	for ns in sorted(total.keys()):
		nsid = mon.cleanfn(ns)
		_print(f"{nsid}.value", total[ns].get('cpu', 'U'))
	# mem total
	_print('multigraph pods_top_mem')
	for ns in sorted(total.keys()):
		nsid = mon.cleanfn(ns)
		_print(f"{nsid}.value", total[ns].get('mem', 'U'))
