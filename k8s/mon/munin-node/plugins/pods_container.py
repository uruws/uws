# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

limits = {
	'failed_ratio': {
		'warning': 1,
		'critical': 2,
	},
	'restart_ratio': {
		'warning': 3,
		'critical': 5,
	},
	'restarted_ratio': {
		'warning': 1,
		'critical': 2,
	},
}

def parse(pods):
	mon.dbg('pods_container parse')
	sts = dict(
		info = dict(),
		status = dict(),
		index = dict(),
	)
	for i in pods.get('items', []):
		kind = i['kind']
		if kind != 'Pod':
			continue
		spec = i.get('spec', {}).get('containers', [])
		status = i.get('status', {}).get('containerStatuses', [])
		phase = i.get('status', {}).get('phase', 'NONE')
		m = i.get('metadata', {})
		ns = m.get('namespace', None)
		gname = mon.generateName(i)
		# info
		if not sts['info'].get(ns, None):
			sts['info'][ns] = dict()
		if not sts['info'][ns].get(gname, None):
			sts['info'][ns][gname] = dict(
				spec = dict(),
				status = dict(),
			)
		__cinfo(sts['info'][ns][gname], spec, status, phase)
		# status
		if not sts['status'].get(ns, None):
			sts['status'][ns] = dict()
		if not sts['status'][ns].get(gname, None):
			sts['status'][ns][gname] = dict(
				failed = 0,
				pending = 0,
				ready = 0,
				restart = 0,
				restarted = 0,
				running = 0,
				spec = 0,
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
		i = mon.containerImage(c.get('image', 'NONE'))
		if sts['spec'].get(i, None) is None:
			sts['spec'][i] = True
	p = phase.lower()
	if not sts['status'].get(p, None):
		sts['status'][p] = dict()
	for c in status:
		i = mon.containerImage(c.get('image', 'NONE'))
		if sts['status'][p].get(i, None) is None:
			sts['status'][p][i] = 0
		sts['status'][p][i] += 1

def __cstatus(sts, spec, status, phase):
	sts['spec'] = len(spec)
	p = phase.lower()
	if not sts.get(p, None):
		sts[p] = 0
	st = len(status)
	if st == 0:
		sts[p] += len(spec)
	else:
		sts[p] += st
	for c in status:
		sts['restart'] += c.get('restartCount', 0)
		if c.get('restartCount', 0) > 0:
			sts['restarted'] += 1
		if c.get('ready', None):
			sts['ready'] += 1
		if c.get('started', None):
			sts['started'] += 1
	sts['failed_ratio'] = 0
	sts['restart_ratio'] = 0
	sts['restarted_ratio'] = 0
	running = sts.get('running', 0)
	if running > 0:
		sts['failed_ratio'] = sts['failed'] / running
		sts['restart_ratio'] = sts['restart'] / running
		sts['restarted_ratio'] = sts['restarted'] / running

def _print(*args):
	print(*args)

def config(sts):
	mon.dbg('pods_container config')
	cluster = mon.cluster()
	# index
	_print('multigraph pod_container')
	_print(f"graph_title {cluster} pods containers")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category pod')
	_print('graph_vlabel number')
	_print('graph_scale no')
	cc = 0
	for cid in sorted(sts.get('index', {}).keys()):
		_print(f"{cid}.label", cid.replace('_', ' '))
		_print(f"{cid}.colour COLOUR{cc}")
		_print(f"{cid}.min 0")
		cc = mon.color(cc)
	if mon.debug(): _print()
	# status
	for ns in sorted(sts.get('status', {}).keys()):
		for gname in sorted(sts['status'][ns].keys()):
			cid = mon.cleanfn(f"{ns}_{gname}")
			_print(f"multigraph pod_container.{cid}")
			_print(f"graph_title {cluster} {ns}/{gname}")
			_print('graph_args --base 1000 -l 0')
			_print('graph_category pod')
			_print('graph_vlabel containers number')
			_print('graph_scale no')
			fc = 0
			for fn in sorted(sts['status'][ns][gname].keys()):
				fid = mon.cleanfn(fn)
				_print(f"{fid}.label", fn.replace('_', ' '))
				_print(f"{fid}.colour COLOUR{fc}")
				_print(f"{fid}.min 0")
				fc = mon.color(fc)
				# limits
				lim = limits.get(fid, None)
				if lim is not None:
					for n in lim.keys():
						_print(f"{fid}.{n}", limits[fid][n])
			# info
			if not sts.get('info', None): sts['info'] = {}
			inf = sts['info'].get(ns, {}).get(gname, {})
			# spec
			idx = 0
			for i in sorted(inf.get('spec', {}).keys()):
				fid = mon.cleanfn(f"zza_spec_{idx:0>4}")
				_print(f"{fid}.label S", i)
				_print(f"{fid}.colour COLOUR{fc}")
				_print(f"{fid}.min 0")
				fc = mon.color(fc)
				idx += 1
			# status
			for s in sorted(inf.get('status', {}).keys()):
				idx = 0
				for i in sorted(inf['status'][s].keys()):
					fid = mon.cleanfn(f"zzz_{s}_{idx:0>4}")
					_print(f"{fid}.label", s[0].upper(), i)
					_print(f"{fid}.colour COLOUR{fc}")
					_print(f"{fid}.min 0")
					fc = mon.color(fc)
					idx += 1
			if mon.debug(): _print()

def report(sts):
	mon.dbg('pods_container report')
	# index
	_print('multigraph pod_container')
	for cid in sorted(sts['index'].keys()):
		_print(f"{cid}.value", sts['index'][cid])
	if mon.debug(): _print()
	# status
	for ns in sorted(sts['status'].keys()):
		for gname in sorted(sts['status'][ns].keys()):
			cid = mon.cleanfn(f"{ns}_{gname}")
			_print(f"multigraph pod_container.{cid}")
			for fn in sorted(sts['status'][ns][gname].keys()):
				fid = mon.cleanfn(fn)
				val = sts['status'][ns][gname][fn]
				_print(f"{fid}.value", val)
			# info
			inf = sts['info'][ns].get(gname, {})
			# spec
			idx = 0
			for i in sorted(inf.get('spec', {}).keys()):
				fid = mon.cleanfn(f"zza_spec_{idx:0>4}")
				_print(f"{fid}.value 1")
				idx += 1
			# status
			for s in sorted(inf['status'].keys()):
				idx = 0
				for i in sorted(inf['status'][s].keys()):
					fid = mon.cleanfn(f"zzz_{s}_{idx:0>4}")
					val = inf['status'][s][i]
					_print(f"{fid}.value", val)
					idx += 1
			if mon.debug(): _print()
