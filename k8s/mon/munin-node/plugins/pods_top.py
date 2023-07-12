# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def _podname(n):
	if n == '':
		return None
	n = n.strip()
	# aws-node
	if n.startswith('aws-node-'):
		return 'aws-node'
	# ebs-csi-node
	if n.startswith('ebs-csi-node-'):
		return 'ebs-csi-node'
	# efs-csi-node
	if n.startswith('efs-csi-node-'):
		return 'efs-csi-node'
	# kube-proxy
	if n.startswith('kube-proxy-'):
		return 'kube-proxy'
	# deployments
	i = n.split('-')
	if len(i) >= 3:
		return '-'.join(i[:-2])
	# stateful set
	return n

def parse(pods):
	mon.dbg('pods_top parse')
	sts = dict()
	for i in pods.get('items', []):
		ns = i.get('namespace', None)
		n = _podname(i.get('name', ''))
		ns = '%s/%s' % (ns, n)
		c = i.get('cpu', 0)
		m = i.get('mem', 0)
		if ns is not None:
			if not sts.get(ns, None):
				sts[ns] = dict(
					count = 0,
					cpu = 0,
					cpu_min = None,
					cpu_max = 0,
					mem = 0,
					mem_min = None,
					mem_max = 0,
				)
			sts[ns]['count'] += 1
			sts[ns]['cpu'] += c
			if sts[ns]['cpu_min'] is None:
				sts[ns]['cpu_min'] = c
			elif c < sts[ns]['cpu_min']:
				sts[ns]['cpu_min'] = c
			if c > sts[ns]['cpu_max']:
				sts[ns]['cpu_max'] = c
			sts[ns]['mem'] += m
			if sts[ns]['mem_min'] is None:
				sts[ns]['mem_min'] = m
			elif m < sts[ns]['mem_min']:
				sts[ns]['mem_min'] = m
			if m > sts[ns]['mem_max']:
				sts[ns]['mem_max'] = m
	return sts

def _print(*args):
	print(*args)

def config(sts):
	mon.dbg('pods_top config')
	cluster = mon.cluster()
	# cpu all
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
		_print(f"{nsid}.label {ns}", f"({c})")
		_print(f"{nsid}.colour COLOUR{color}")
		_print(f"{nsid}.draw AREASTACK")
		_print(f"{nsid}.min 0")
		color = mon.color(color)
	# namespace cpu
	for ns in sorted(sts.keys()):
		nsid = mon.cleanfn(ns)
		_print(f"multigraph pod_top_cpu.{nsid}_cpu")
		_print(f"graph_title {cluster} {ns} pods CPU")
		_print('graph_args --base 1000 -l 0')
		_print('graph_category top')
		_print('graph_vlabel millicores')
		_print('graph_scale yes')
		_print('f1_avg.label average')
		_print('f1_avg.colour COLOUR1')
		_print('f1_avg.draw LINE1')
		_print('f1_avg.min 0')
		_print('f2_min.label min')
		_print('f2_min.colour COLOUR2')
		_print('f2_min.draw LINE1')
		_print('f2_min.min 0')
		_print('f3_max.label max')
		_print('f3_max.colour COLOUR3')
		_print('f3_max.draw LINE1')
		_print('f3_max.min 0')
	# mem all
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
		_print(f"{nsid}.label {ns}", f"({m})")
		_print(f"{nsid}.colour COLOUR{color}")
		_print(f"{nsid}.draw AREASTACK")
		_print(f"{nsid}.min 0")
		color = mon.color(color)
	# namespace mem
	for ns in sorted(sts.keys()):
		nsid = mon.cleanfn(ns)
		_print(f"multigraph pod_top_mem.{nsid}_mem")
		_print(f"graph_title {cluster} {ns} pods memory")
		_print('graph_args --base 1000 -l 0')
		_print('graph_category top')
		_print('graph_vlabel MiB')
		_print('graph_scale yes')
		_print('f1_avg.label average')
		_print('f1_avg.colour COLOUR1')
		_print('f1_avg.draw LINE1')
		_print('f1_avg.min 0')
		_print('f2_min.label min')
		_print('f2_min.colour COLOUR2')
		_print('f2_min.draw LINE1')
		_print('f2_min.min 0')
		_print('f3_max.label max')
		_print('f3_max.colour COLOUR3')
		_print('f3_max.draw LINE1')
		_print('f3_max.min 0')

def _avg(sts, k):
	c = sts.get('count', 0)
	v = sts.get(k, 'U')
	if v != 'U' and c > 0:
		return v / c
	return v

def report(sts):
	mon.dbg('pods_top report')
	# cpu all
	_print('multigraph pod_top_cpu')
	for ns in sorted(sts.keys()):
		nsid = mon.cleanfn(ns)
		c = sts[ns].get('cpu', 'U')
		_print(f"{nsid}.value", c)
	# namespace cpu
	for ns in sorted(sts.keys()):
		nsid = mon.cleanfn(ns)
		_print(f"multigraph pod_top_cpu.{nsid}_cpu")
		_print('f1_avg.value', _avg(sts[ns], 'cpu'))
		_print('f2_min.value', sts[ns].get('cpu_min', 'U'))
		_print('f3_max.value', sts[ns].get('cpu_max', 'U'))
	# mem all
	_print('multigraph pod_top_mem')
	for ns in sorted(sts.keys()):
		nsid = mon.cleanfn(ns)
		m = sts[ns].get('mem', 'U')
		_print(f"{nsid}.value", m)
	# namespace mem
	for ns in sorted(sts.keys()):
		nsid = mon.cleanfn(ns)
		_print(f"multigraph pod_top_mem.{nsid}_mem")
		_print('f1_avg.value', _avg(sts[ns], 'mem'))
		_print('f2_min.value', sts[ns].get('mem_min', 'U'))
		_print('f3_max.value', sts[ns].get('mem_max', 'U'))
