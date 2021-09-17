# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def parse(pods):
	mon.dbg('pods_container parse')
	sts = dict(
		info = dict(),
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
		gname = mon.generateName(i)
		# info
		if not sts['info'].get(ns, None):
			sts['info'][ns] = dict()
		if not sts['info'][ns].get(gname, None):
			sts['info'][ns][gname] = dict(
				spec = dict(),
				running = dict(),
			)
		__cinfo(sts['info'][ns][gname], spec, status, phase)
		# status
		if not sts['status'].get(ns, None):
			sts['status'][ns] = dict()
		if not sts['status'][ns].get(gname, None):
			sts['status'][ns][gname] = dict(
				spec = 0,
				running = 0,
				restart = 0,
				ready = 0,
				started = 0,
			)
		__cstatus(sts['status'][ns][gname], spec, status, phase)
	# index
	for ns in sts['status'].keys():
		for gname in sts['status'][ns].keys():
			for fn in sts['status'][ns][gname].keys():
				if not sts['index'].get(fn, None):
					sts['index'][fn] = 0
				sts['index'][fn] += sts['status'][ns][gname][fn]
	return sts

def __cinfo(sts, spec, status, phase):
	for c in spec:
		i = c['image']
		if sts['spec'].get(i, None) is None:
			sts['spec'][i] = True
	p = phase.lower()
	if not sts.get(p, None):
		sts[p] = dict()
	for c in status:
		i = c['image']
		if sts[p].get(i, None) is None:
			sts[p][i] = 0
		sts[p][i] += 1

def __cstatus(sts, spec, status, phase):
	sts['spec'] = len(spec)
	p = phase.lower()
	if not sts.get(p, None):
		sts[p] = 0
	sts[p] += len(status)
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
			for fn in sorted(sts['status'][ns][gname].keys()):
				fid = mon.cleanfn(fn)
				print(f"{fid}.label", fn)
				print(f"{fid}.colour COLOUR{fc}")
				print(f"{fid}.min 0")
				inf = sts['info'][ns][gname].get(fn, None)
				if inf is not None:
					msg = list()
					for i in sorted(inf.keys()):
						if fn == 'spec':
							msg.append(i)
						else:
							msg.append(f"{i}: {inf[i]}")
					print(f"{fid}.info", ','.join(msg))
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
			for fn in sorted(sts['status'][ns][gname].keys()):
				fid = mon.cleanfn(fn)
				val = sts['status'][ns][gname][fn]
				print(f"{fid}.value", val)
			if mon.debug(): print()
