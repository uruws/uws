# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def parse(pods):
	mon.dbg('pods_container parse')
	sts = dict(
		status = dict(),
		index = dict(
			spec = 0,
			running = 0,
			restart = 0,
			ready = 0,
			started = 0,
		),
	)
	for i in pods['items']:
		kind = i['kind']
		if kind != 'Pod':
			continue
		spec = i['spec'].get('containers', [])
		status = i['status'].get('containerStatuses', [])
		m = i['metadata']
		ns = m.get('namespace', None)
		name = m.get('name', None)
		if not sts['status'].get(ns, None):
			sts['status'][ns] = dict()
		gname = mon.generateName(i)
		sts['status'][ns][name] = __cinfo(gname, spec, status)
		for fn in sts['status'][ns][name].keys():
			if fn == 'gname':
				continue
			sts['index'][fn] += sts['status'][ns][name][fn]
	return sts

def __cinfo(gname, spec, status):
	sts = dict(
		gname = gname,
		spec = 0,
		running = 0,
		restart = 0,
		ready = 0,
		started = 0,
	)
	sts['spec'] = len(spec)
	sts['running'] = len(status)
	for c in status:
		sts['restart'] += c['restartCount']
		if c['ready']:
			sts['ready'] += 1
		if c['started']:
			sts['started'] += 1
	return sts

def config(sts):
	mon.dbg('pods_container config')
	cluster = mon.cluster()
	# index
	print('multigraph pod_container')
	print(f"graph_title {cluster} pod containers")
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
		for name in sorted(sts['status'][ns].keys()):
			gname = sts['status'][ns][name]['gname']
			cid = mon.cleanfn(f"{ns}_{gname}")
			print(f"multigraph pod_container.{cid}")
			print(f"graph_title {cluster} {ns}/{name} containers")
			print('graph_args --base 1000 -l 0')
			print('graph_category pod')
			print('graph_vlabel number')
			print('graph_printf %3.0lf')
			print('graph_scale yes')
			fc = 0
			for fid in sorted(sts['status'][ns][name].keys()):
				if fid == 'gname':
					continue
				print(f"{fid}.label", fid)
				print(f"{fid}.colour COLOUR{cc}")
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
		for name in sorted(sts['status'][ns].keys()):
			gname = sts['status'][ns][name]['gname']
			cid = mon.cleanfn(f"{ns}_{gname}")
			print(f"multigraph pod_container.{cid}")
			for fid in sorted(sts['status'][ns][name].keys()):
				if fid == 'gname':
					continue
				val = sts['status'][ns][name][fid]
				print(f"{fid}.value", val)
			if mon.debug(): print()
