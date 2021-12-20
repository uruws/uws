# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def parse(i):
	sts = dict()
	s = i.get('spec', {})
	st = i.get('status', {})
	return dict(
		spec_replicas = s.get('replicas',
			st.get('desiredNumberScheduled', 'U')),
		available_replicas = st.get('availableReplicas',
			st.get('currentReplicas',
				st.get('numberAvailable', 'U'))),
		ready_replicas = st.get('readyReplicas',
			st.get('numberReady', 'U')),
		replicas = st.get('replicas',
			st.get('currentNumberScheduled', 'U')),
		updated_replicas = st.get('updatedReplicas',
			st.get('updatedNumberScheduled', 'U')),
	)

def _print(*args):
	print(*args)

def config(sts):
	mon.dbg('deploy_status config')
	cluster = mon.cluster()
	# replicas
	_print('multigraph deploy_replicas')
	_print(f"graph_title {cluster} deployments replicas")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category deploy')
	_print('graph_vlabel number')
	_print('graph_printf %3.0lf')
	_print('graph_scale yes')
	fc = 0
	for ns in sorted(sts.keys()):
		for name in sorted(sts[ns].keys()):
			fid = mon.cleanfn(ns+"_"+name)
			_print(f"f_{fid}.label {ns}/{name}")
			_print(f"f_{fid}.colour COLOUR{fc}")
			_print(f"f_{fid}.min 0")
			fc += 1
			if fc > 28: fc = 0
	if mon.debug(): _print()
	# replicas all
	_print('multigraph deploy_replicas.all')
	_print(f"graph_title {cluster} all deployments")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category deploy')
	_print('graph_vlabel number of replicas')
	_print('graph_printf %3.0lf')
	_print('graph_scale yes')
	fc = 0
	for ns in sorted(sts.keys()):
		for name in sorted(sts[ns].keys()):
			fid = mon.cleanfn(ns+"_"+name)
			_print(f"f_{fid}.label {ns}/{name}")
			_print(f"f_{fid}.colour COLOUR{fc}")
			_print(f"f_{fid}.min 0")
			fc += 1
			if fc > 28: fc = 0
	if mon.debug(): _print()
	# replicas status
	for ns in sorted(sts.keys()):
		for name in sorted(sts[ns].keys()):
			sid = mon.cleanfn(ns+"_"+name)
			_print(f"multigraph deploy_replicas.{sid}")
			_print(f"graph_title {cluster} {ns}/{name} deployment")
			_print('graph_args --base 1000 -l 0')
			_print('graph_category deploy')
			_print('graph_vlabel number of replicas')
			_print('graph_printf %3.0lf')
			_print('graph_scale yes')
			fc = 0
			for fn in sorted(sts[ns][name].keys()):
				n = fn.replace('_replicas', '', 1)
				if n == 'replicas':
					n = 'running'
				_print(f"{fn}.label", n)
				_print(f"{fn}.colour COLOUR{fc}")
				_print(f"{fn}.min 0")
				fc += 1
				if fc > 28: fc = 0
			if mon.debug(): _print()

def report(sts):
	mon.dbg('deploy_status report')
	# replicas
	_print('multigraph deploy_replicas')
	for ns in sorted(sts.keys()):
		for name in sorted(sts[ns].keys()):
			fid = mon.cleanfn(ns+"_"+name)
			val = sts[ns][name]['replicas']
			_print(f"f_{fid}.value", val)
	if mon.debug(): _print()
	# replicas all
	_print('multigraph deploy_replicas.all')
	for ns in sorted(sts.keys()):
		for name in sorted(sts[ns].keys()):
			fid = mon.cleanfn(ns+"_"+name)
			val = sts[ns][name]['replicas']
			_print(f"f_{fid}.value", val)
	if mon.debug(): _print()
	# replicas status
	for ns in sorted(sts.keys()):
		for name in sorted(sts[ns].keys()):
			sid = mon.cleanfn(ns+"_"+name)
			_print(f"multigraph deploy_replicas.{sid}")
			for fn in sorted(sts[ns][name].keys()):
				val = sts[ns][name][fn]
				_print(f"{fn}.value", val)
			if mon.debug(): _print()
