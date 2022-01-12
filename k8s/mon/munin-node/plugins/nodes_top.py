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
	_print('f0_total.label total', f"(nodes: {sts.get('count', 0)})")
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
	_print('graph_scale no')
	_print('f0_total.label total', f"(nodes: {sts.get('count', 0)})")
	_print('f0_total.colour COLOUR0')
	_print('f0_total.draw AREASTACK')
	_print('f0_total.min 0')
	_print('f0_total.max 100')
	_print('f0_total.warning 93')
	_print('f0_total.critical 97')
	# mem
	_print('multigraph nodes_top_mem')
	_print(f"graph_title {cluster} nodes memory")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category nodes')
	_print('graph_vlabel MiB')
	_print('graph_printf %3.0lf')
	_print('graph_scale yes')
	_print('f0_total.label total', f"(nodes: {sts.get('count', 0)})")
	_print('f0_total.colour COLOUR0')
	_print('f0_total.draw AREASTACK')
	_print('f0_total.min 0')
	_print('f1_avg.label average')
	_print('f1_avg.colour COLOUR1')
	_print('f1_avg.min 0')
	# mem percentage
	_print('multigraph nodes_top_memp')
	_print(f"graph_title {cluster} nodes memory usage")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category nodes')
	_print('graph_vlabel percentage')
	_print('graph_printf %3.0lf')
	_print('graph_scale no')
	_print('f0_total.label total', f"(nodes: {sts.get('count', 0)})")
	_print('f0_total.colour COLOUR0')
	_print('f0_total.draw AREASTACK')
	_print('f0_total.min 0')
	_print('f0_total.max 100')
	_print('f0_total.warning 93')
	_print('f0_total.critical 97')

def _value(sts, count, name):
	v = sts.get(name, 'U')
	if count > 0 and v != 'U':
		return v / count
	return v

def report(sts):
	mon.dbg('nodes_top report')
	n = sts.get('count', 0)
	# cpu
	_print('multigraph nodes_top_cpu')
	_print('f0_total.value', sts.get('cpu', 'U'))
	_print('f1_avg.value', _value(sts, n, 'cpu'))
	# cpu percentage
	_print('multigraph nodes_top_cpup')
	_print('f0_total.value', _value(sts, n, 'cpup'))
	# mem
	_print('multigraph nodes_top_mem')
	_print('f0_total.value', sts.get('mem', 'U'))
	_print('f1_avg.value', _value(sts, n, 'mem'))
	# mem percentage
	_print('multigraph nodes_top_memp')
	_print('f0_total.value', _value(sts, n, 'memp'))
