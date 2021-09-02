# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

sts = dict(
	active = 'U',
	reading = 'U',
	waiting = 'U',
	writing = 'U',
	accepted = 'U',
	handled = 'U',
)

def parse(meta, value):
	mon.dbg('parse nginx_conn')
	if meta['state'] == 'active':
		sts['active'] = value
	elif meta['state'] == 'reading':
		sts['reading'] = value
	elif meta['state'] == 'waiting':
		sts['waiting'] = value
	elif meta['state'] == 'writing':
		sts['writing'] = value
	elif meta['state'] == 'accepted':
		sts['accepted'] = value
	elif meta['state'] == 'handled':
		sts['handled'] = value

def config():
	mon.dbg('config nginx_conn')
	# connections state
	print('multigraph nginx_connections_state')
	print('graph_title Connections state')
	print('graph_args --base 1000 -l 0')
	print('graph_category nginx')
	print('graph_vlabel number')
	print('graph_scale yes')
	print('graph_printf %3.0lf')
	print('active.label active')
	print('active.colour COLOUR0')
	print('active.min 0')
	print('reading.label reading')
	print('reading.colour COLOUR1')
	print('reading.min 0')
	print('waiting.label waiting')
	print('waiting.colour COLOUR2')
	print('waiting.min 0')
	print('writing.label writing')
	print('writing.colour COLOUR3')
	print('writing.min 0')
	# connections total
	print('multigraph nginx_connections_total')
	print('graph_title Connections total')
	print('graph_args --base 1000 -l 0')
	print('graph_category nginx')
	print('graph_vlabel number')
	print('graph_scale yes')
	print('graph_printf %3.0lf')
	print('accepted.label accepted')
	print('accepted.colour COLOUR0')
	print('accepted.min 0')
	print('handled.label handled')
	print('handled.colour COLOUR1')
	print('handled.min 0')
	# connections total counter
	print('multigraph nginx_connections_total_counter')
	print('graph_title Connections total counter')
	print('graph_args --base 1000 -l 0')
	print('graph_category nginx')
	print('graph_vlabel number per second')
	print('graph_scale no')
	print('accepted.label accepted')
	print('accepted.colour COLOUR0')
	print('accepted.type COUNTER')
	print('accepted.min 0')
	print('handled.label handled')
	print('handled.colour COLOUR1')
	print('handled.type COUNTER')
	print('handled.min 0')

def report(sts):
	mon.dbg('report nginx_conn')
	# connections
	print('multigraph nginx_connections_state')
	print('active.value', sts['active'])
	print('reading.value', sts['reading'])
	print('waiting.value', sts['waiting'])
	print('writing.value', sts['writing'])
	# connections total
	print('multigraph nginx_connections_total')
	print('accepted.value', sts['accepted'])
	print('handled.value', sts['handled'])
	# connections total counter
	print('multigraph nginx_connections_total_counter')
	print('accepted.value', sts['accepted'])
	print('handled.value', sts['handled'])
