# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

sts = dict(
	cpu = dict(
		controller = 'U',
		total = 'U',
	),
	mem = dict(
		controller = 'U',
		total = 'U',
		controller_virtual = 'U',
		total_virtual = 'U',
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
	print('total.colour COLOUR1')
	print('total.type DERIVE')
	print('total.min 0')
	# mem
	print('multigraph nginx_proc_mem')
	print('graph_title Memory usage')
	print('graph_args --base 1024 -l 0')
	print('graph_category nginx')
	print('graph_vlabel bytes')
	print('graph_scale yes')
	print('controller.label controller')
	print('controller.colour COLOUR0')
	print('controller.min 0')
	print('total.label total')
	print('total.colour COLOUR1')
	print('total.min 0')
	print('controller_virtual.label controller virtual')
	print('controller_virtual.colour COLOUR2')
	print('controller_virtual.min 0')
	print('total_virtual.label total virtual')
	print('total_virtual.colour COLOUR3')
	print('total_virtual.min 0')

def report(sts):
	mon.dbg('report nginx_proc')
	# cpu
	print('multigraph nginx_proc_cpu')
	print('controller.value', sts['cpu']['controller'])
	print('total.value', sts['cpu']['total'])
	# mem
	print('multigraph nginx_proc_mem')
	print('controller.value', sts['mem']['controller'])
	print('total.value', sts['mem']['total'])
	print('controller_virtual.value', sts['mem']['controller_virtual'])
	print('total_virtual.value', sts['mem']['total_virtual'])
