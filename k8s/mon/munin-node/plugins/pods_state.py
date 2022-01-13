# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def parse(pods):
	mon.dbg('pods_state parse')
	sts = dict(
		info = dict(),
		total = dict(
			Failed = 0,
			Error = 0,
			OOMKilled = 0,
			Restarted = 0,
			Running = 0,
		),
	)
	for i in pods.get('items', []):
		if i.get('kind') != 'Pod':
			continue
		m = i.get('metadata', {})
		ns = m.get('namespace', '').strip()
		if ns == '':
			continue
		st = i.get('status', {}).get('containerStatuses', [])
		for s in st:
			n = s.get('name', '').strip()
			if n == '':
				continue
			img = mon.containerImage(s.get('image', '').strip())
			state = s.get('lastState', {}).get('terminated', {}).get('reason', '')
			if not sts['info'].get(ns):
				sts['info'][ns] = dict()
			if not sts['info'][ns].get(n):
				sts['info'][ns][n] = dict(
					image = dict(),
					state = dict(
						Failed = 0,
						Error = 0,
						OOMKilled = 0,
						Restarted = 0,
						Running = 0,
					),
				)
			ready = s.get('ready', False) is True
			started = s.get('started', False) is True
			restarted = s.get('restartCount', 0) > 0
			# image
			if img != '':
				if not sts['info'][ns][n]['image'].get(img):
					sts['info'][ns][n]['image'][img] = 0
				sts['info'][ns][n]['image'][img] += 1
			if state != '':
				# info
				if not sts['info'][ns][n]['state'].get(state):
					sts['info'][ns][n]['state'][state] = 0
				sts['info'][ns][n]['state'][state] += 1
				# total
				if sts['total'].get(state, None) is None:
					sts['total'][state] = 0
				sts['total'][state] += 1
			if ready and started:
				# running
				sts['info'][ns][n]['state']['Running'] += 1
				sts['total']['Running'] += 1
			else:
				# failed
				sts['info'][ns][n]['state']['Failed'] += 1
				sts['total']['Failed'] += 1
			if restarted:
				# restarted
				sts['info'][ns][n]['state']['Restarted'] += 1
				sts['total']['Restarted'] += 1
	return sts

def _print(*args):
	print(*args)

def config(sts):
	mon.dbg('pods_state config')
	cluster = mon.cluster()
	# total
	total = sts.get('total', {})
	_print('multigraph pod_state')
	_print(f"graph_title {cluster} pods state")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category pod')
	_print('graph_vlabel number')
	_print('graph_printf %3.0lf')
	_print('graph_scale no')
	color = 0
	for s in sorted(total.keys()):
		sid = mon.cleanfn(s)
		_print(f"s_{sid}.label", s)
		_print(f"s_{sid}.colour COLOUR{color}")
		_print(f"s_{sid}.min 0")
		color = mon.color(color)
	# info
	info = sts.get('info', {})
	for ns in sorted(info.keys()):
		for n in sorted(info[ns].keys()):
			name = f"{ns}/{n}"
			pid = mon.cleanfn(name)
			_print(f"multigraph pod_state.{pid}")
			_print(f"graph_title {cluster} {name} pods state")
			_print('graph_args --base 1000 -l 0')
			_print('graph_category pod')
			_print('graph_vlabel number')
			_print('graph_printf %3.0lf')
			_print('graph_scale no')
			color = 0
			for s in sorted(info[ns][n]['state'].keys()):
				sid = mon.cleanfn(s)
				_print(f"f_{sid}.label", s)
				_print(f"f_{sid}.colour COLOUR{color}")
				_print(f"f_{sid}.min 0")
				color = mon.color(color)
			img = info[ns][n].get('image', {})
			for i in sorted(img.keys()):
				sid = mon.cleanfn(i)
				_print(f"z_{sid}.label", i)
				_print(f"z_{sid}.colour COLOUR{color}")
				_print(f"z_{sid}.min 0")
				color = mon.color(color)

def report(sts):
	mon.dbg('pods_state report')
	# total
	total = sts.get('total', {})
	_print('multigraph pod_state')
	for s in sorted(total.keys()):
		sid = mon.cleanfn(s)
		v = sts['total'][s]
		_print(f"s_{sid}.value", v)
	# info
	info = sts.get('info', {})
	for ns in sorted(info.keys()):
		for n in sorted(info[ns].keys()):
			name = f"{ns}/{n}"
			pid = mon.cleanfn(name)
			_print(f"multigraph pod_state.{pid}")
			for s in sorted(info[ns][n]['state'].keys()):
				sid = mon.cleanfn(s)
				v = info[ns][n]['state'][s]
				_print(f"f_{sid}.value", v)
			img = info[ns][n].get('image', {})
			for i in sorted(img.keys()):
				sid = mon.cleanfn(i)
				_print(f"z_{sid}.value", img[i])
