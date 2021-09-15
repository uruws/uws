# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon
import deploy_condition

def parse(deploy):
	mon.dbg('deploy_info parse')
	sts = dict(
		total = 0,
		deploy = dict(),
		status = dict(),
		condition = dict(),
		condition_index = dict(),
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
		s = i['spec']
		st = i['status']
		# condition
		cond = deploy_condition.parse(ns, name, i)
		sts['condition'] = cond['condition']
		sts['condition_index'] = cond['condition_index']
		# status
		if not sts['deploy'].get(ns, None):
			sts['deploy'][ns] = dict()
		sts['deploy'][ns][name] = _generation(m, st)
		if not sts['status'].get(ns, None):
			sts['status'][ns] = dict()
		if kind == 'DaemonSet':
			dst = _dsStatus(kind, i)
		else:
			dst = _status(kind, s, st)
		sts['status'][ns][name] = dst
	return sts

def _generation(m, st):
	return dict(
		generation = m.get('generation', 'U'),
		observed_generation = st.get('observedGeneration', 'U'),
	)

def _status(kind, s, st):
	return dict(
		kind = kind,
		d = dict(
			spec_replicas = s.get('replicas', 'U'),
			available_replicas = st.get('availableReplicas',
				st.get('currentReplicas', 'U')),
			ready_replicas = st.get('readyReplicas', 'U'),
			replicas = st.get('replicas', 'U'),
			updated_replicas = st.get('updatedReplicas', 'U'),
		),
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
	# condition
	deploy_condition.config(sts)
	# replicas
	print('multigraph deploy_replicas')
	print(f"graph_title {cluster} deployments replicas")
	print('graph_args --base 1000 -l 0')
	print('graph_category deploy')
	print('graph_vlabel number')
	print('graph_printf %3.0lf')
	print('graph_scale yes')
	fc = 0
	for ns in sorted(sts['status'].keys()):
		for name in sorted(sts['status'][ns].keys()):
			fid = mon.cleanfn(ns+"_"+name)
			print(f"f_{fid}.label {ns}/{name}")
			print(f"f_{fid}.colour COLOUR{fc}")
			print(f"f_{fid}.min 0")
			fc += 1
			if fc > 28:
				fc = 0
	if mon.debug(): print()
	# replicas all
	print('multigraph deploy_replicas.all')
	print(f"graph_title {cluster} all")
	print('graph_args --base 1000 -l 0')
	print('graph_category deploy')
	print('graph_vlabel number of replicas')
	print('graph_printf %3.0lf')
	print('graph_scale yes')
	fc = 0
	for ns in sorted(sts['status'].keys()):
		for name in sorted(sts['status'][ns].keys()):
			fid = mon.cleanfn(ns+"_"+name)
			print(f"f_{fid}.label {ns}/{name}")
			print(f"f_{fid}.colour COLOUR{fc}")
			print(f"f_{fid}.min 0")
			fc += 1
			if fc > 28:
				fc = 0
	if mon.debug(): print()
	# replicas status
	for ns in sorted(sts['status'].keys()):
		for name in sorted(sts['status'][ns].keys()):
			if mon.debug(): print()
			sid = mon.cleanfn(ns+"_"+name)
			print(f"multigraph deploy_replicas.{sid}")
			print(f"graph_title {cluster} {ns}/{name}")
			print('graph_args --base 1000 -l 0')
			print('graph_category deploy')
			print('graph_vlabel number of replicas')
			print('graph_printf %3.0lf')
			print('graph_scale yes')
			fc = 0
			for fn in sorted(sts['status'][ns][name]['d'].keys()):
				n = fn.replace('_replicas', '', 1)
				if n == 'replicas':
					n = 'running'
				print(f"{fn}.label", n)
				print(f"{fn}.colour COLOUR{fc}")
				print(f"{fn}.min 0")
				fc += 1
				if fc > 28:
					fc = 0
	if mon.debug(): print()
	# generation status
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

def report(sts):
	mon.dbg('deploy_info report')
	# total
	print('multigraph deploy')
	print('a_total.value', sts['total'])
	if mon.debug(): print()
	# condition
	deploy_condition.report(sts)
	# replicas
	print('multigraph deploy_replicas')
	for ns in sorted(sts['status'].keys()):
		for name in sorted(sts['status'][ns].keys()):
			fid = mon.cleanfn(ns+"_"+name)
			val = sts['status'][ns][name]['d']['replicas']
			print(f"f_{fid}.value", val)
	if mon.debug(): print()
	# replicas all
	print('multigraph deploy_replicas.all')
	for ns in sorted(sts['status'].keys()):
		for name in sorted(sts['status'][ns].keys()):
			fid = mon.cleanfn(ns+"_"+name)
			val = sts['status'][ns][name]['d']['replicas']
			print(f"f_{fid}.value", val)
	if mon.debug(): print()
	# replicas status
	for ns in sorted(sts['status'].keys()):
		for name in sorted(sts['status'][ns].keys()):
			if mon.debug(): print()
			sid = mon.cleanfn(ns+"_"+name)
			print(f"multigraph deploy_replicas.{sid}")
			for fn in sorted(sts['status'][ns][name]['d'].keys()):
				val = sts['status'][ns][name]['d'][fn]
				print(f"{fn}.value", val)
	# generation status
	print('multigraph deploy_status')
	for ns in sorted(sts['deploy'].keys()):
		for name in sorted(sts['deploy'][ns].keys()):
			fid = mon.cleanfn(ns+"_"+name)
			cur = sts['deploy'][ns][name]['generation']
			obs = sts['deploy'][ns][name]['observed_generation']
			print(f"f_{fid}_cur.value", cur)
			print(f"f_{fid}_obs.value", obs)
