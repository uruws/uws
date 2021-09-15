# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def parse(i):
	sts = dict()
	s = i['spec']
	st = i['status']
	return dict(
		spec_replicas = s.get('replicas', 'U'),
		available_replicas = st.get('availableReplicas',
			st.get('currentReplicas', 'U')),
		ready_replicas = st.get('readyReplicas', 'U'),
		replicas = st.get('replicas', 'U'),
		updated_replicas = st.get('updatedReplicas', 'U'),
	)

def config(sts):
	mon.dbg('deploy_status config')
	cluster = mon.cluster()
	# replicas
	print('multigraph deploy_replicas')
	print(f"graph_title {cluster} deployments replicas")
	print('graph_args --base 1000 -l 0')
	print('graph_category deploy')
	print('graph_vlabel number')
	print('graph_printf %3.0lf')
	print('graph_scale yes')
	fc = 0
	for ns in sorted(sts.keys()):
		for name in sorted(sts[ns].keys()):
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
	for ns in sorted(sts.keys()):
		for name in sorted(sts[ns].keys()):
			fid = mon.cleanfn(ns+"_"+name)
			print(f"f_{fid}.label {ns}/{name}")
			print(f"f_{fid}.colour COLOUR{fc}")
			print(f"f_{fid}.min 0")
			fc += 1
			if fc > 28:
				fc = 0
	if mon.debug(): print()
	# replicas status
	for ns in sorted(sts.keys()):
		for name in sorted(sts[ns].keys()):
			sid = mon.cleanfn(ns+"_"+name)
			print(f"multigraph deploy_replicas.{sid}")
			print(f"graph_title {cluster} {ns}/{name}")
			print('graph_args --base 1000 -l 0')
			print('graph_category deploy')
			print('graph_vlabel number of replicas')
			print('graph_printf %3.0lf')
			print('graph_scale yes')
			fc = 0
			for fn in sorted(sts[ns][name].keys()):
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

def report(sts):
	mon.dbg('deploy_status report')
	# replicas
	print('multigraph deploy_replicas')
	for ns in sorted(sts.keys()):
		for name in sorted(sts[ns].keys()):
			fid = mon.cleanfn(ns+"_"+name)
			val = sts[ns][name]['replicas']
			print(f"f_{fid}.value", val)
	if mon.debug(): print()
	# replicas all
	print('multigraph deploy_replicas.all')
	for ns in sorted(sts.keys()):
		for name in sorted(sts[ns].keys()):
			fid = mon.cleanfn(ns+"_"+name)
			val = sts[ns][name]['replicas']
			print(f"f_{fid}.value", val)
	if mon.debug(): print()
	# replicas status
	for ns in sorted(sts.keys()):
		for name in sorted(sts[ns].keys()):
			if mon.debug(): print()
			sid = mon.cleanfn(ns+"_"+name)
			print(f"multigraph deploy_replicas.{sid}")
			for fn in sorted(sts[ns][name].keys()):
				val = sts[ns][name][fn]
				print(f"{fn}.value", val)
	if mon.debug(): print()
