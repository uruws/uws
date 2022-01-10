# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def parse(nodes):
	mon.dbg('nodes_top parse')
	sts = dict(
		count = 0,
		cpu = 0,
		cpup = 0,
		mem = 0,
		memp = 0,
	)
	try:
		sts.update(nodes)
	except TypeError:
		pass
	return sts

def _print(*args):
	print(*args)

def config(sts):
	mon.dbg('nodes_top config')

def report(sts):
	mon.dbg('nodes_top report')
