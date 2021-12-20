# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon
import deploy_generation
import deploy_condition
import deploy_status

def parse(deploy):
	mon.dbg('deploy_info parse')
	sts = dict(
		total = 0,
		deploy = dict(),
		condition = dict(),
		condition_index = dict(),
		status = dict(),
	)
	items = deploy.get('items', [])
	# total
	sts['total'] = len(items)
	for i in items:
		kind = i.get('kind', None)
		if kind != 'Deployment'\
			and kind != 'StatefulSet'\
			and kind != 'DaemonSet':
			continue
		m = i.get('metadata', None)
		if m is None:
			continue
		ns = m.get('namespace', None)
		name = m.get('name', None)
		# generation
		if not sts['deploy'].get(ns, None):
			sts['deploy'][ns] = dict()
		sts['deploy'][ns][name] = deploy_generation.parse(m, i.get('status', {}))
		# condition
		if not sts['condition'].get(ns, None):
			sts['condition'][ns] = dict()
		deploy_condition.parse(sts, ns, name, i)
		# status
		if not sts['status'].get(ns, None):
			sts['status'][ns] = dict()
		sts['status'][ns][name] = deploy_status.parse(i)
	return sts

def _print(msg):
	print(msg)

def config(sts):
	mon.dbg('deploy_info config')
	cluster = mon.cluster()
	# total
	_print('multigraph deploy')
	_print(f"graph_title {cluster} deployments")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category deploy')
	_print('graph_vlabel number')
	_print('graph_printf %3.0lf')
	_print('graph_scale yes')
	_print('a_total.label total')
	_print('a_total.colour COLOUR0')
	_print('a_total.draw AREA')
	_print('a_total.min 0')
	if mon.debug(): _print()
	# generation
	deploy_generation.config(sts.get('deploy', {}))
	# condition
	deploy_condition.config(sts)
	# status
	deploy_status.config(sts.get('status', {}))

def report(sts):
	mon.dbg('deploy_info report')
	# total
	_print('multigraph deploy')
	_print('a_total.value', sts.get('total', 'U'))
	if mon.debug(): _print()
	# generation
	deploy_generation.report(sts.get('deploy', {}))
	# condition
	deploy_condition.report(sts)
	# status
	deploy_status.report(sts.get('status', {}))
