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

def config(sts):
	mon.dbg('pods_condition config')
	cluster = mon.cluster()
	# index
	print('multigraph pod_condition')
	print(f"graph_title {cluster} pods condition")
	print('graph_args --base 1000 -l 0')
	print('graph_category pod')
	print('graph_vlabel number')
	print('graph_printf %3.0lf')
	print('graph_scale yes')
	cc = 0
	for ctype in sorted(sts['index'].keys()):
		cid = mon.cleanfn(ctype.lower())
		print(f"c_{cid}.label", ctype)
		print(f"c_{cid}.colour COLOUR{cc}")
		print(f"c_{cid}.min 0")
		cc = mon.color(cc)
	if mon.debug(): print()
	# status
	for ns in sorted(sts['cond'].keys()):
		for gname in sorted(sts['cond'][ns].keys()):
			cid = mon.cleanfn(f"{ns}_{gname}")
			print(f"multigraph pod_condition.{cid}")
			print(f"graph_title {cluster} {ns}/{gname} condition")
			print('graph_args --base 1000 -l 0')
			print('graph_category pod')
			print('graph_vlabel number of pods')
			print('graph_printf %3.0lf')
			print('graph_scale yes')
			cc = 0
			for ctype in sorted(sts['cond'][ns][gname].keys()):
				fid = mon.cleanfn(ctype.lower())
				print(f"c_{fid}.label", ctype)
				print(f"c_{fid}.colour COLOUR{cc}")
				print(f"c_{fid}.min 0")
				cc = mon.color(cc)
			if mon.debug(): print()

def report(sts):
	mon.dbg('pods_condition report')
	# index
	print('multigraph pod_condition')
	for ctype in sorted(sts['index'].keys()):
		cid = mon.cleanfn(ctype.lower())
		print(f"c_{cid}.value", sts['index'][ctype])
	if mon.debug(): print()
	# status
	for ns in sorted(sts['cond'].keys()):
		for gname in sorted(sts['cond'][ns].keys()):
			cid = mon.cleanfn(f"{ns}_{gname}")
			print(f"multigraph pod_condition.{cid}")
			for ctype in sorted(sts['cond'][ns][gname].keys()):
				fid = mon.cleanfn(ctype.lower())
				val = sts['cond'][ns][gname][ctype]
				print(f"c_{fid}.value", val)
			if mon.debug(): print()
