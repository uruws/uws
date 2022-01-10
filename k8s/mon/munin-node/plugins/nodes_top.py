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
	cluster = mon.cluster()
	# cpu
	_print('multigraph nodes_top_cpu')
	_print(f"graph_title {cluster} nodes CPU")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category nodes')
	_print('graph_vlabel millicores')
	_print('graph_printf %3.0lf')
	_print('graph_scale yes')
	_print('f0_total.label total')
	_print('f0_total.colour COLOUR0')
	_print('f0_total.draw AREASTACK')
	_print('f0_total.min 0')
	_print('f1_avg.label average')
	_print('f1_avg.colour COLOUR1')
	_print('f1_avg.min 0')
	# cpu percentage
	_print('multigraph nodes_top_cpup')
	_print(f"graph_title {cluster} nodes CPU usage")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category nodes')
	_print('graph_vlabel percentage')
	_print('graph_printf %3.0lf')
	_print('graph_scale yes')
	_print('f0_total.label total')
	_print('f0_total.colour COLOUR0')
	_print('f0_total.draw AREASTACK')
	_print('f0_total.min 0')
	_print('f1_avg.label average')
	_print('f1_avg.colour COLOUR1')
	_print('f1_avg.min 0')

def report(sts):
	mon.dbg('nodes_top report')
