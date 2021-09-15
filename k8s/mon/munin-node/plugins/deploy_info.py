# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon
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
		sts['deploy'][ns][name] = _generation(m, i['status'])
		# condition
		if not sts['condition'].get(ns, None):
			sts['condition'][ns] = dict()
		deploy_condition.parse(sts, ns, name, i)
		# status
		if not sts['status'].get(ns, None):
			sts['status'][ns] = dict()
		if kind == 'DaemonSet':
			dst = _dsStatus(kind, i)
		else:
			dst = deploy_status.parse(i)
		sts['status'][ns][name] = dst
	return sts

def _generation(m, st):
	return dict(
		generation = m.get('generation', 'U'),
		observed_generation = st.get('observedGeneration', 'U'),
	)

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
	print('multigraph deploy_status')
	print(f"graph_title {cluster} deployments status")
	print('graph_args --base 1000 -l 0')
	print('graph_category deploy')
	print('graph_vlabel generation number')
	print('graph_printf %3.0lf')
	print('graph_scale yes')
	fc = 0
	for ns in sorted(sts['deploy'].keys()):
		for name in sorted(sts['deploy'][ns].keys()):
			fid = mon.cleanfn(ns+"_"+name)
			print(f"f_{fid}_cur.label {ns}/{name} cur")
			print(f"f_{fid}_cur.colour COLOUR{fc}")
			print(f"f_{fid}_cur.min 0")
			print(f"f_{fid}_obs.label {ns}/{name} obs")
			print(f"f_{fid}_obs.colour COLOUR{fc}")
			print(f"f_{fid}_obs.min 0")
			fc += 1
			if fc > 28:
				fc = 0
	if mon.debug(): print()
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
	print('multigraph deploy_status')
	for ns in sorted(sts['deploy'].keys()):
		for name in sorted(sts['deploy'][ns].keys()):
			fid = mon.cleanfn(ns+"_"+name)
			cur = sts['deploy'][ns][name]['generation']
			obs = sts['deploy'][ns][name]['observed_generation']
			print(f"f_{fid}_cur.value", cur)
			print(f"f_{fid}_obs.value", obs)
	if mon.debug(): print()
	# condition
	deploy_condition.report(sts)
	# status
	deploy_status.report(sts['status'])
