# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def parse(deploy):
	mon.dbg('deploy_info parse')
	sts = dict(
		total = 0,
		deploy = dict(),
		status = dict(),
		condition = dict(),
	)
	# total
	sts['total'] = len(deploy['items'])
	for i in deploy['items']:
		if i['kind'] != 'Deployment':
			continue
		# condition
		for c in i['status'].get('conditions', {}):
			typ = c['type']
			st = c['status']
			if not sts['condition'].get(typ, None):
				sts['condition'][typ] = 0
			if st == 'True':
				sts['condition'][typ] += 1
		# status
		ns = i['metadata']['namespace']
		name = i['metadata']['name']
		if not sts['deploy'].get(ns, None):
			sts['deploy'][ns] = dict()
		m = i['metadata']
		s = i['spec']
		st = i['status']
		d = dict(
			generation = m.get('generation', 'U'),
			observed_generation = st.get('observedGeneration', 'U'),
		)
		sts['deploy'][ns][name] = d
		if not sts['status'].get(ns, None):
			sts['status'][ns] = dict()
		ds = dict(
			spec_replicas = s.get('replicas', 'U'),
			available_replicas = st.get('availableReplicas', 'U'),
			ready_replicas = st.get('readyReplicas', 'U'),
			replicas = st.get('replicas', 'U'),
			updated_replicas = st.get('updatedReplicas', 'U'),
		)
		sts['status'][ns][name] = ds
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
	if mon.debug(): print()
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
	if mon.debug(): print()
	# condition
	print('multigraph deploy.condition')
	print(f"graph_title {cluster} deployments condition")
	print('graph_args --base 1000 -l 0')
	print('graph_category deploy')
	print('graph_vlabel number')
	print('graph_printf %3.0lf')
	print('graph_scale yes')
	cc = 0
	for c in sorted(sts['condition'].keys()):
		cid = mon.cleanfn(c)
		print(f"c_{cid}.label", c)
		print(f"c_{cid}.colour COLOUR{cc}")
		print(f"c_{cid}.min 0")
		cc += 1
		if cc > 28:
			cc = 0
	if mon.debug(): print()
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
	# status index
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
	# status
	for ns in sorted(sts['status'].keys()):
		for name in sorted(sts['status'][ns].keys()):
			if mon.debug(): print()
			sid = mon.cleanfn(ns+"_"+name)
			print(f"multigraph deploy_status.{sid}")
			print(f"graph_title {cluster} {ns}/{name}")
			print('graph_args --base 1000 -l 0')
			print('graph_category deploy')
			print('graph_vlabel number of replicas')
			print('graph_printf %3.0lf')
			print('graph_scale yes')
			fc = 0
			for fn in sorted(sts['status'][ns][name].keys()):
				n = fn.replace('_replicas', '', 1)
				if n == 'replicas':
					n = 'running'
				print(f"{fn}.label", n)
				print(f"{fn}.colour COLOUR{fc}")
				print(f"{fn}.min 0")
				fc += 1
				if fc > 28:
					fc = 0

def report(sts):
	mon.dbg('deploy_info report')
	# total index
	print('multigraph deploy')
	print('a_total.value', sts['total'])
	if mon.debug(): print()
	# total
	print('multigraph deploy.total')
	print('a_total.value', sts['total'])
	if mon.debug(): print()
	# condition
	print('multigraph deploy.condition')
	for c in sorted(sts['condition'].keys()):
		cid = mon.cleanfn(c)
		print(f"c_{cid}.value", sts['condition'][c])
	if mon.debug(): print()
	# replicas
	print('multigraph deploy_replicas')
	for ns in sorted(sts['status'].keys()):
		for name in sorted(sts['status'][ns].keys()):
			fid = mon.cleanfn(ns+"_"+name)
			val = sts['status'][ns][name]['replicas']
			print(f"f_{fid}.value", val)
	if mon.debug(): print()
	# status index
	print('multigraph deploy_status')
	for ns in sorted(sts['deploy'].keys()):
		for name in sorted(sts['deploy'][ns].keys()):
			fid = mon.cleanfn(ns+"_"+name)
			cur = sts['deploy'][ns][name]['generation']
			obs = sts['deploy'][ns][name]['observed_generation']
			print(f"f_{fid}_cur.value", cur)
			print(f"f_{fid}_obs.value", obs)
	# status
	for ns in sorted(sts['status'].keys()):
		for name in sorted(sts['status'][ns].keys()):
			if mon.debug(): print()
			sid = mon.cleanfn(ns+"_"+name)
			print(f"multigraph deploy_status.{sid}")
			for fn in sorted(sts['status'][ns][name].keys()):
				val = sts['status'][ns][name][fn]
				print(f"{fn}.value", val)
