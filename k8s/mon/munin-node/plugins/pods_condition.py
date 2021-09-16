# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def parse(pods):
	mon.dbg('pods_condition parse')
	sts = dict(
		index = dict(),
		cond = dict(),
	)
	for i in pods['items']:
		kind = i['kind']
		if kind != 'Pod':
			continue
		# status
		m = i['metadata']
		ns = m.get('namespace', None)
		name = m.get('name', None)
		if not sts['cond'].get(ns, None):
			sts['cond'][ns] = dict()
		if not sts['cond'][ns].get(name, None):
			sts['cond'][ns][name] = dict(
				count = dict(),
				gname = mon.generateName(i),
			)
		# index
		for cond in i['status'].get('conditions', {}):
			st = cond['status']
			typ = cond['type']
			if not sts['index'].get(typ, None):
				sts['index'][typ] = 0
			if not sts['cond'][ns][name]['count'].get(typ, None):
				sts['cond'][ns][name]['count'][typ] = 0
			if st == 'True':
				sts['index'][typ] += 1
				sts['cond'][ns][name]['count'][typ] += 1
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
		for name in sorted(sts['cond'][ns].keys()):
			gname = sts['cond'][ns][name]['gname']
			cid = mon.cleanfn(f"{ns}_{gname}")
			print(f"multigraph pod_condition.{cid}")
			print(f"graph_title {cluster} {ns}/{name} condition")
			print('graph_args --base 1000 -l 0')
			print('graph_category pod')
			print('graph_vlabel number of pods')
			print('graph_printf %3.0lf')
			print('graph_scale yes')
			cc = 0
			for ctype in sorted(sts['cond'][ns][name]['count'].keys()):
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
		for name in sorted(sts['cond'][ns].keys()):
			gname = sts['cond'][ns][name]['gname']
			cid = mon.cleanfn(f"{ns}_{gname}")
			print(f"multigraph pod_condition.{cid}")
			for ctype in sorted(sts['cond'][ns][name]['count'].keys()):
				fid = mon.cleanfn(ctype.lower())
				val = sts['cond'][ns][name]['count'][ctype]
				print(f"c_{fid}.value", val)
			if mon.debug(): print()
