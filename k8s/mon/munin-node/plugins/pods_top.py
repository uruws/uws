# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def parse(pods):
	mon.dbg('pods_top parse')
	sts = dict()
	for i in pods.get('items', []):
		ns = i.get('namespace', None)
		c = i.get('cpu', 0)
		m = i.get('mem', 0)
		if ns is not None:
			if not sts.get(ns, None):
				sts[ns] = dict(count = 0, cpu = 0, mem = 0)
			sts[ns]['count'] += 1
			sts[ns]['cpu'] += c
			sts[ns]['mem'] += m
	return sts

def _print(*args):
	print(*args)

def config(sts):
	mon.dbg('pods_top config')
	cluster = mon.cluster()
	# cpu total
	cpu_total = 0
	_print('multigraph pod_top_cpu')
	_print(f"graph_title {cluster} pods CPU")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category top')
	_print('graph_vlabel millicores')
	_print('graph_scale yes')
	color = 0
	for ns in sorted(sts.keys()):
		nsid = mon.cleanfn(ns)
		c = sts[ns].get('count', 0)
		cpu_total += c
		_print(f"{nsid}.label {ns}", f"({c})")
		_print(f"{nsid}.colour COLOUR{color}")
		_print(f"{nsid}.draw AREASTACK")
		_print(f"{nsid}.min 0")
		color = mon.color(color)
	_print('ztotal.label total', f"({cpu_total})")
	_print('ztotal.colour 000000')
	_print('ztotal.draw LINE1')
	_print('ztotal.min 0')
	# namespace cpu
	for ns in sorted(sts.keys()):
		nsid = mon.cleanfn(ns)
		_print(f"multigraph pod_top_cpu.{nsid}")
		_print(f"graph_title {cluster} {nsid} pods CPU")
		_print('graph_args --base 1000 -l 0')
		_print('graph_category top')
		_print('graph_vlabel millicores')
		_print('graph_scale yes')
		_print('f0_total.label total', f"({sts[ns].get('count', 0)})")
		_print('f0_total.colour COLOUR0')
		_print('f0_total.draw AREASTACK')
		_print('f0_total.min 0')
		_print('f1_avg.label average')
		_print('f1_avg.colour COLOUR1')
		_print('f1_avg.draw LINE1')
		_print('f1_avg.min 0')
	# mem total
	mem_total = 0
	_print('multigraph pod_top_mem')
	_print(f"graph_title {cluster} pods memory")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category top')
	_print('graph_vlabel MiB')
	_print('graph_scale yes')
	color = 0
	for ns in sorted(sts.keys()):
		nsid = mon.cleanfn(ns)
		m = sts[ns].get('count', 0)
		mem_total += m
		_print(f"{nsid}.label {ns}", f"({m})")
		_print(f"{nsid}.colour COLOUR{color}")
		_print(f"{nsid}.draw AREASTACK")
		_print(f"{nsid}.min 0")
		color = mon.color(color)
	_print('ztotal.label total', f"({mem_total})")
	_print('ztotal.colour 000000')
	_print('ztotal.draw LINE1')
	_print('ztotal.min 0')
	# namespace mem
	for ns in sorted(sts.keys()):
		nsid = mon.cleanfn(ns)
		_print(f"multigraph pod_top_mem.{nsid}")
		_print(f"graph_title {cluster} {nsid} pods memory")
		_print('graph_args --base 1000 -l 0')
		_print('graph_category top')
		_print('graph_vlabel MiB')
		_print('graph_scale yes')
		_print('f0_total.label total', f"({sts[ns].get('count', 0)})")
		_print('f0_total.colour COLOUR0')
		_print('f0_total.draw AREASTACK')
		_print('f0_total.min 0')
		_print('f1_avg.label average')
		_print('f1_avg.colour COLOUR1')
		_print('f1_avg.draw LINE1')
		_print('f1_avg.min 0')

def _avg(sts, k):
	c = sts.get('count', 0)
	v = sts.get(k, 'U')
	if v != 'U' and c > 0:
		return v / c
	return v

def report(sts):
	mon.dbg('pods_top report')
	# cpu total
	cpu_total = 0
	_print('multigraph pod_top_cpu')
	for ns in sorted(sts.keys()):
		nsid = mon.cleanfn(ns)
		c = sts[ns].get('cpu', 'U')
		_print(f"{nsid}.value", c)
		if c != 'U':
			cpu_total += c
	_print('ztotal.value', cpu_total)
	# namespace cpu
	for ns in sorted(sts.keys()):
		nsid = mon.cleanfn(ns)
		_print(f"multigraph pod_top_cpu.{nsid}")
		_print('f0_total.value', sts[ns].get('cpu', 'U'))
		_print('f1_avg.value', _avg(sts[ns], 'cpu'))
	# mem total
	mem_total = 0
	_print('multigraph pod_top_mem')
	for ns in sorted(sts.keys()):
		nsid = mon.cleanfn(ns)
		m = sts[ns].get('mem', 'U')
		_print(f"{nsid}.value", m)
		if m != 'U':
			mem_total += m
	_print('ztotal.value', mem_total)
	# namespace mem
	for ns in sorted(sts.keys()):
		nsid = mon.cleanfn(ns)
		_print(f"multigraph pod_top_mem.{nsid}")
		_print('f0_total.value', sts[ns].get('mem', 'U'))
		_print('f1_avg.value', _avg(sts[ns], 'mem'))
