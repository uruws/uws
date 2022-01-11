# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def parse(pods):
	mon.dbg('pods_top parse')
	sts = dict(
		info = dict(),
		total = dict(),
	)
	for i in pods.get('items', []):
		ns = i.get('namespace', None)
		n = i.get('name', None)
		c = i.get('cpu', 0)
		m = i.get('mem', 0)
		if ns is not None and n is not None:
			if not sts['info'].get(ns, None):
				sts['info'][ns] = dict()
				sts['total'][ns] = dict(cpu = 0, mem = 0)
			if not sts['info'][ns].get(n, None):
				sts['info'][ns][n] = dict(cpu = 0, mem = 0)
			sts['info'][ns][n]['cpu'] = c
			sts['info'][ns][n]['mem'] = m
			sts['total'][ns]['cpu'] += c
			sts['total'][ns]['mem'] += m
	return sts

def _print(*args):
	print(*args)

def config(sts):
	mon.dbg('pods_top config')

def report(sts):
	mon.dbg('pods_top report')
