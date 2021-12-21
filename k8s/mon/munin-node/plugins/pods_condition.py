# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def parse(pods):
	mon.dbg('pods_condition parse')
	sts = dict(
		index = dict(
			ContainersReady = 0,
			Initialized = 0,
			PodScheduled = 0,
			Ready = 0,
		),
		cond = dict(),
	)
	for i in pods['items']:
		kind = i['kind']
		if kind != 'Pod':
			continue
		# status
		m = i['metadata']
		ns = m.get('namespace', None)
		gname = mon.generateName(i)
		if not sts['cond'].get(ns, None):
			sts['cond'][ns] = dict()
		if not sts['cond'][ns].get(gname, None):
			sts['cond'][ns][gname] = dict(
				ContainersReady = 0,
				Initialized = 0,
				PodScheduled = 0,
				Ready = 0,
			)
		# index
		for cond in i['status'].get('conditions', {}):
			st = cond['status']
			typ = cond['type']
			if sts['index'].get(typ, None) is None:
				sts['index'][typ] = 0
			if sts['cond'][ns][gname].get(typ, None) is None:
				sts['cond'][ns][gname][typ] = 0
			if st == 'True':
				sts['index'][typ] += 1
				sts['cond'][ns][gname][typ] += 1
	return sts

def _print(*args):
	print(*args)

def config(sts):
	mon.dbg('pods_condition config')
	cluster = mon.cluster()
	# index
	_print('multigraph pod_condition')
	_print(f"graph_title {cluster} pods condition")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category pod')
	_print('graph_vlabel number')
	_print('graph_printf %3.0lf')
	_print('graph_scale yes')
	cc = 0
	for ctype in sorted(sts['index'].keys()):
		cid = mon.cleanfn(ctype.lower())
		_print(f"c_{cid}.label", ctype)
		_print(f"c_{cid}.colour COLOUR{cc}")
		_print(f"c_{cid}.min 0")
		cc = mon.color(cc)
	if mon.debug(): _print()
	# status
	for ns in sorted(sts['cond'].keys()):
		for gname in sorted(sts['cond'][ns].keys()):
			cid = mon.cleanfn(f"{ns}_{gname}")
			_print(f"multigraph pod_condition.{cid}")
			_print(f"graph_title {cluster} {ns}/{gname} condition")
			_print('graph_args --base 1000 -l 0')
			_print('graph_category pod')
			_print('graph_vlabel number of pods')
			_print('graph_printf %3.0lf')
			_print('graph_scale yes')
			cc = 0
			for ctype in sorted(sts['cond'][ns][gname].keys()):
				fid = mon.cleanfn(ctype.lower())
				_print(f"c_{fid}.label", ctype)
				_print(f"c_{fid}.colour COLOUR{cc}")
				_print(f"c_{fid}.min 0")
				cc = mon.color(cc)
			if mon.debug(): _print()

def report(sts):
	mon.dbg('pods_condition report')
	# index
	_print('multigraph pod_condition')
	for ctype in sorted(sts['index'].keys()):
		cid = mon.cleanfn(ctype.lower())
		_print(f"c_{cid}.value", sts['index'][ctype])
	if mon.debug(): _print()
	# status
	for ns in sorted(sts['cond'].keys()):
		for gname in sorted(sts['cond'][ns].keys()):
			cid = mon.cleanfn(f"{ns}_{gname}")
			_print(f"multigraph pod_condition.{cid}")
			for ctype in sorted(sts['cond'][ns][gname].keys()):
				fid = mon.cleanfn(ctype.lower())
				val = sts['cond'][ns][gname][ctype]
				_print(f"c_{fid}.value", val)
			if mon.debug(): _print()
