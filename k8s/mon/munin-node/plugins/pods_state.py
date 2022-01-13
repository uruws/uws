# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def parse(pods):
	mon.dbg('pods_state parse')
	sts = dict(
		info = dict(),
		total = dict(
			Error = 0,
			OOMKilled = 0,
		),
	)
	for i in pods.get('items', []):
		if i.get('kind') != 'Pod':
			continue
		m = i.get('metadata', {})
		ns = m.get('namespace')
		if not ns:
			continue
		st = i.get('status', {}).get('containerStatuses', [])
		for s in st:
			n = s.get('name')
			if not n:
				continue
			img = s.get('image')
			state = s.get('lastState', {}).get('terminated', {}).get('reason', '')
			if not sts['info'].get(ns):
				sts['info'][ns] = dict()
			if not sts['info'][ns].get(n):
				sts['info'][ns][n] = dict(
					image = img,
					state = dict(
						Error = 0,
						OOMKilled = 0,
					),
				)
			if state != '':
				if not sts['info'][ns][n]['state'].get(state):
					sts['info'][ns][n]['state'][state] = 0
				sts['info'][ns][n]['state'][state] += 1
				# total
				if sts['total'].get(state, None) is None:
					sts['total'][state] = 0
				sts['total'][state] += 1
	return sts

def _print(*args):
	print(*args)

def config(sts):
	mon.dbg('pods_state config')
	cluster = mon.cluster()
	# total
	_print('multigraph pod_state')
	_print(f"graph_title {cluster} pods state")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category pod')
	_print('graph_vlabel number')
	_print('graph_printf %3.0lf')
	_print('graph_scale no')

def report(sts):
	mon.dbg('pods_state report')
