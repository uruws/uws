# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def parse(deploy):
	mon.dbg('deploy_info parse')
	sts = dict(
		total = 0,
		deploy = dict(),
	)
	sts['total'] = len(deploy['items'])
	for i in deploy['items']:
		if i['kind'] != 'Deployment':
			continue
		ns = i['metadata']['namespace']
		name = i['metadata']['name']
		if not sts['deploy'].get(ns, None):
			sts['deploy'][ns] = dict()
		m = i['metadata']
		s = i['spec']
		st = i['status']
		d = dict(
			generation = m.get('generation', 'U'),
			spec_replicas = s.get('replicas', 'U'),
			observed_generation = st.get('observedGeneration', 'U'),
			available_replicas = st.get('availableReplicas', 'U'),
			ready_replicas = st.get('readyReplicas', 'U'),
			replicas = st.get('replicas', 'U'),
			updated_replicas = st.get('updatedReplicas', 'U'),
		)
		sts['deploy'][ns][name] = d
	return sts

def config(sts):
	mon.dbg('deploy_info config')
	cluster = mon.cluster()
	# total index
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
	# total
	print('multigraph deploy.total')
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

def report(sts):
	mon.dbg('deploy_info report')
	# total index
	print('multigraph deploy')
	print('a_total.value', sts['total'])
	# total
	print('multigraph deploy.total')
	print('a_total.value', sts['total'])
