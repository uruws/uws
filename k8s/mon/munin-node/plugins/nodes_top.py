# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def parse(nodes):
	mon.dbg('nodes_top parse')
	sts = dict(
		count    = 0,
		cpu      = 0,
		cpu_min  = 0,
		cpu_max  = 0,
		cpup     = 0,
		cpup_min = 0,
		cpup_max = 0,
		mem      = 0,
		mem_min  = 0,
		mem_max  = 0,
		memp     = 0,
		memp_min = 0,
		memp_max = 0,
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
	_print('graph_scale yes')
	_print('f1_avg.label average')
	_print('f1_avg.colour COLOUR1')
	_print('f1_avg.min 0')
	_print('f2_min.label min')
	_print('f2_min.colour COLOUR2')
	_print('f2_min.min 0')
	_print('f3_max.label max')
	_print('f3_max.colour COLOUR3')
	_print('f3_max.min 0')
	# cpu percentage
	_print('multigraph nodes_top_cpup')
	_print(f"graph_title {cluster} nodes CPU usage")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category nodes')
	_print('graph_vlabel percentage')
	_print('graph_scale no')
	_print('f1_min.label min')
	_print('f1_min.colour COLOUR1')
	_print('f1_min.min 0')
	_print('f1_min.max 100')
	_print('f2_max.label max')
	_print('f2_max.colour COLOUR2')
	_print('f2_max.min 0')
	_print('f2_max.max 100')
	# mem
	_print('multigraph nodes_top_mem')
	_print(f"graph_title {cluster} nodes memory")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category nodes')
	_print('graph_vlabel MiB')
	_print('graph_scale yes')
	_print('f1_avg.label average')
	_print('f1_avg.colour COLOUR1')
	_print('f1_avg.min 0')
	_print('f2_min.label min')
	_print('f2_min.colour COLOUR2')
	_print('f2_min.min 0')
	_print('f3_max.label max')
	_print('f3_max.colour COLOUR3')
	_print('f3_max.min 0')
	# mem percentage
	_print('multigraph nodes_top_memp')
	_print(f"graph_title {cluster} nodes memory usage")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category nodes')
	_print('graph_vlabel percentage')
	_print('graph_scale no')
	_print('f1_min.label min')
	_print('f1_min.colour COLOUR1')
	_print('f1_min.min 0')
	_print('f1_min.max 100')
	_print('f2_max.label max')
	_print('f2_max.colour COLOUR2')
	_print('f2_max.min 0')
	_print('f2_max.max 100')

def _avg(sts, count, name):
	v = sts.get(name, 'U')
	if count > 0 and v != 'U':
		return v / count
	return v

def report(sts):
	mon.dbg('nodes_top report')
	n = sts.get('count', 0)
	# cpu
	_print('multigraph nodes_top_cpu')
	_print('f1_avg.value', _avg(sts, n, 'cpu'))
	_print('f2_min.value', sts.get('cpu_min', 'U'))
	_print('f3_max.value', sts.get('cpu_max', 'U'))
	# cpu percentage
	_print('multigraph nodes_top_cpup')
	_print('f1_min.value', sts.get('cpup_min', 'U'))
	_print('f2_max.value', sts.get('cpup_max', 'U'))
	# mem
	_print('multigraph nodes_top_mem')
	_print('f1_avg.value', _avg(sts, n, 'mem'))
	_print('f2_min.value', sts.get('mem_min', 'U'))
	_print('f3_max.value', sts.get('mem_max', 'U'))
	# mem percentage
	_print('multigraph nodes_top_memp')
	_print('f1_min.value', sts.get('memp_min', 'U'))
	_print('f2_max.value', sts.get('memp_max', 'U'))
