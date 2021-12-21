# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def parse(pods):
	mon.dbg('pods_info parse')
	sts = dict(
		total = 'U',
	)
	# total
	sts['total'] = len(pods['items'])
	for i in pods['items']:
		kind = i['kind']
		if kind != 'Pod':
			continue
	return sts

def _print(*args):
	print(*args)

def config(sts):
	mon.dbg('pods_info config')
	cluster = mon.cluster()
	# total
	_print('multigraph pod')
	_print(f"graph_title {cluster} pods")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category pod')
	_print('graph_vlabel number')
	_print('graph_printf %3.0lf')
	_print('graph_scale yes')
	_print('total.label total')
	_print('total.colour COLOUR0')
	_print('total.draw AREA')
	_print('total.min 0')
	if mon.debug(): _print()

def report(sts):
	mon.dbg('pods_info report')
	# total
	_print('multigraph pod')
	_print('total.value', sts['total'])
	if mon.debug(): _print()
