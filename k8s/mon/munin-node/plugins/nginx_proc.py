# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

sts = dict(
	cpu = dict(
		controller = 'U',
		total = 'U',
	),
)

def parse(kind, key, value):
	mon.dbg('parse nginx_proc:', kind, key)
	sts[kind][key] = value

def config():
	mon.dbg('config nginx_proc')
	# cpu
	print('multigraph nginx_proc_cpu')
	print('graph_title CPU usage')
	print('graph_args --base 1000 -l 0')
	print('graph_category nginx')
	print('graph_vlabel time per second')
	print('graph_scale no')
	print('controller.label controller')
	print('controller.colour COLOUR0')
	print('controller.type DERIVE')
	print('controller.min 0')
	print('total.label total')
	print('total.colour COLOUR0')
	print('total.type DERIVE')
	print('total.min 0')

def report(sts):
	mon.dbg('report nginx_proc')
	# cpu
	print('multigraph nginx_proc_cpu')
	print('controller.value', sts['cpu']['controller'])
	print('total.value', sts['cpu']['total'])
