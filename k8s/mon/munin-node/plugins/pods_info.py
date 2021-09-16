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

def config(sts):
	mon.dbg('pods_info config')
	cluster = mon.cluster()
	# total
	print('multigraph pod')
	print(f"graph_title {cluster} pods")
	print('graph_args --base 1000 -l 0')
	print('graph_category pod')
	print('graph_vlabel number')
	print('graph_printf %3.0lf')
	print('graph_scale yes')
	print('total.label total')
	print('total.colour COLOUR0')
	print('total.draw AREA')
	print('total.min 0')
	if mon.debug(): print()

def report(sts):
	mon.dbg('pods_info report')
	# total
	print('multigraph pod')
	print('total.value', sts['total'])
	if mon.debug(): print()
