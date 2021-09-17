# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def parse(pods):
	mon.dbg('pods_container parse')
	sts = dict(
		status = dict(),
		index = dict(),
	)
	for i in pods['items']:
		kind = i['kind']
		if kind != 'Pod':
			continue
		spec = i['spec'].get('containers', [])
		status = i['status'].get('containerStatuses', [])
		phase = i['status'].get('phase', None)
		m = i['metadata']
		ns = m.get('namespace', None)
		if not sts['status'].get(ns, None):
			sts['status'][ns] = dict()
		gname = mon.generateName(i)
		if not sts['status'][ns].get(gname, None):
			sts['status'][ns][gname] = dict(
				spec = 0,
				running = 0,
				restart = 0,
				ready = 0,
				started = 0,
			)
		__cinfo(sts['status'][ns][gname], spec, status, phase)
	for ns in sts['status'].keys():
		for gname in sts['status'][ns].keys():
			for fn in sts['status'][ns][gname].keys():
				if not sts['index'].get(fn, None):
					sts['index'][fn] = 0
				sts['index'][fn] += sts['status'][ns][gname][fn]
	return sts

def __cinfo(sts, spec, status, phase):
	sts['spec'] = len(spec)
	sts[phase.lower()] += len(status)
	for c in status:
		sts['restart'] += c['restartCount']
		if c['ready']:
			sts['ready'] += 1
		if c['started']:
			sts['started'] += 1

def config(sts):
	mon.dbg('pods_container config')
	cluster = mon.cluster()
	# index
	print('multigraph pod_container')
	print(f"graph_title {cluster} pods containers")
	print('graph_args --base 1000 -l 0')
	print('graph_category pod')
	print('graph_vlabel number')
	print('graph_printf %3.0lf')
	print('graph_scale yes')
	cc = 0
	for cid in sorted(sts['index'].keys()):
		print(f"{cid}.label", cid)
		print(f"{cid}.colour COLOUR{cc}")
		print(f"{cid}.min 0")
		cc = mon.color(cc)
	if mon.debug(): print()
	# status
	for ns in sorted(sts['status'].keys()):
		for gname in sorted(sts['status'][ns].keys()):
			cid = mon.cleanfn(f"{ns}_{gname}")
			print(f"multigraph pod_container.{cid}")
			print(f"graph_title {cluster} {ns}/{gname}")
			print('graph_args --base 1000 -l 0')
			print('graph_category pod')
			print('graph_vlabel containers number')
			print('graph_printf %3.0lf')
			print('graph_scale yes')
			fc = 0
			for fid in sorted(sts['status'][ns][gname].keys()):
				print(f"{fid}.label", fid)
				print(f"{fid}.colour COLOUR{fc}")
				print(f"{fid}.min 0")
				fc = mon.color(fc)
			if mon.debug(): print()

def report(sts):
	mon.dbg('pods_container report')
	# index
	print('multigraph pod_container')
	for cid in sorted(sts['index'].keys()):
		print(f"{cid}.value", sts['index'][cid])
	if mon.debug(): print()
	# status
	for ns in sorted(sts['status'].keys()):
		for gname in sorted(sts['status'][ns].keys()):
			cid = mon.cleanfn(f"{ns}_{gname}")
			print(f"multigraph pod_container.{cid}")
			for fid in sorted(sts['status'][ns][gname].keys()):
				val = sts['status'][ns][gname][fid]
				print(f"{fid}.value", val)
			if mon.debug(): print()
