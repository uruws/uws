# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def parse(pods):
	mon.dbg('pods_state parse')
	sts = dict()
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
			if not sts.get(ns):
				sts[ns] = dict()
			if not sts[ns].get(n):
				sts[ns][n] = dict(
					image = img,
					state = dict(
						Error = 0,
						OOMKilled = 0,
					),
				)
			if state != '':
				if not sts[ns][n]['state'].get(state):
					sts[ns][n]['state'][state] = 0
				sts[ns][n]['state'][state] += 1
	return sts

def _print(*args):
	print(*args)

def config(sts):
	mon.dbg('pods_state config')
	cluster = mon.cluster()

def report(sts):
	mon.dbg('pods_state report')
