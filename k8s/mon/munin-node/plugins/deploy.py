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
	# total
	sts['total'] = len(deploy['items'])
	for i in deploy['items']:
		kind = i['kind']
		if kind != 'Deployment'\
			and kind != 'StatefulSet'\
			and kind != 'DaemonSet':
			continue
		m = i['metadata']
		ns = m.get('namespace', None)
		name = m.get('name', None)
		# generation
		if not sts['deploy'].get(ns, None):
			sts['deploy'][ns] = dict()
		sts['deploy'][ns][name] = deploy_generation.parse(m, i['status'])
		# condition
		if not sts['condition'].get(ns, None):
			sts['condition'][ns] = dict()
		deploy_condition.parse(sts, ns, name, i)
		# status
		if not sts['status'].get(ns, None):
			sts['status'][ns] = dict()
		sts['status'][ns][name] = deploy_status.parse(i)
	return sts

def _dsStatus(kind, i):
	return dict(
		kind = kind,
		d = dict(),
	)

def config(sts):
	mon.dbg('deploy_info config')
	cluster = mon.cluster()
	# total
	print('multigraph deploy')
	print(f"graph_title {cluster} deployments")
	print('graph_args --base 1000 -l 0')
	print('graph_category deploy')
	print('graph_vlabel number')
	print('graph_printf %3.0lf')
	print('graph_scale yes')
	print('a_total.label total')
	print('a_total.colour COLOUR0')
	print('a_total.draw AREA')
	print('a_total.min 0')
	if mon.debug(): print()
	# generation
	deploy_generation.config(sts['deploy'])
	# condition
	deploy_condition.config(sts)
	# status
	deploy_status.config(sts['status'])

def report(sts):
	mon.dbg('deploy_info report')
	# total
	print('multigraph deploy')
	print('a_total.value', sts['total'])
	if mon.debug(): print()
	# generation
	deploy_generation.report(sts['deploy'])
	# condition
	deploy_condition.report(sts)
	# status
	deploy_status.report(sts['status'])
