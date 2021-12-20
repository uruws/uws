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

def __parse(meta, value):
	mon.dbg('parse nginx_conn:', meta)
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
	return True

def parse(name, meta, value):
	if name == 'nginx_ingress_controller_nginx_process_connections':
		return __parse(meta, value)
	elif name == 'nginx_ingress_controller_nginx_process_connections_total':
		return __parse(meta, value)
	return False

def _print(*args):
	print(*args)

def config(sts):
	mon.dbg('config nginx_conn')
	# connections state
	_print('multigraph nginx_connections_state')
	_print('graph_title connections state')
	_print('graph_args --base 1000 -l 0')
	_print('graph_category nginx_conn')
	_print('graph_vlabel number')
	_print('graph_scale yes')
	_print('active.label active')
	_print('active.colour COLOUR0')
	_print('active.min 0')
	_print('reading.label reading')
	_print('reading.colour COLOUR1')
	_print('reading.min 0')
	_print('waiting.label waiting')
	_print('waiting.colour COLOUR2')
	_print('waiting.min 0')
	_print('writing.label writing')
	_print('writing.colour COLOUR3')
	_print('writing.min 0')
	# connections total
	_print('multigraph nginx_connections')
	_print('graph_title connections total')
	_print('graph_args --base 1000 -l 0')
	_print('graph_category nginx_conn')
	_print('graph_vlabel number')
	_print('graph_scale yes')
	_print('accepted.label accepted')
	_print('accepted.colour COLOUR0')
	_print('accepted.min 0')
	_print('handled.label handled')
	_print('handled.colour COLOUR1')
	_print('handled.min 0')
	# connections counter
	_print('multigraph nginx_connections.counter')
	_print('graph_title connections')
	_print('graph_args --base 1000 -l 0')
	_print('graph_category nginx_conn')
	_print('graph_vlabel number per second')
	_print('graph_scale no')
	_print('accepted.label accepted')
	_print('accepted.colour COLOUR0')
	_print('accepted.type DERIVE')
	_print('accepted.min 0')
	_print('accepted.cdef accepted,1000,/')
	_print('handled.label handled')
	_print('handled.colour COLOUR1')
	_print('handled.type DERIVE')
	_print('handled.min 0')
	_print('handled.cdef handled,1000,/')

def report(sts):
	mon.dbg('report nginx_conn')
	# connections
	_print('multigraph nginx_connections_state')
	_print('active.value', sts['active'])
	_print('reading.value', sts['reading'])
	_print('waiting.value', sts['waiting'])
	_print('writing.value', sts['writing'])
	# connections total
	_print('multigraph nginx_connections')
	_print('accepted.value', sts['accepted'])
	_print('handled.value', sts['handled'])
	# connections counter
	_print('multigraph nginx_connections.counter')
	_print('accepted.value', mon.derive(sts['accepted']))
	_print('handled.value', mon.derive(sts['handled']))
