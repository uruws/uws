# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def parse(m, st):
	return dict(
		generation = m.get('generation', 'U'),
		observed_generation = st.get('observedGeneration', 'U'),
	)

def _print(msg):
	print(msg)

def config(sts):
	cluster = mon.cluster()
	_print('multigraph deploy_generation')
	_print(f"graph_title {cluster} deployments generation")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category deploy')
	_print('graph_vlabel number')
	_print('graph_printf %3.0lf')
	_print('graph_scale yes')
	fc = 0
	for ns in sorted(sts.keys()):
		for name in sorted(sts[ns].keys()):
			fid = mon.cleanfn(ns+"_"+name)
			_print(f"f_{fid}_cur.label {ns}/{name} cur")
			_print(f"f_{fid}_cur.colour COLOUR{fc}")
			_print(f"f_{fid}_cur.min 0")
			_print(f"f_{fid}_obs.label {ns}/{name} obs")
			_print(f"f_{fid}_obs.colour COLOUR{fc}")
			_print(f"f_{fid}_obs.min 0")
			fc += 1
			if fc > 28: fc = 0
	if mon.debug(): _print()

def report(sts):
	_print('multigraph deploy_generation')
	for ns in sorted(sts.keys()):
		for name in sorted(sts[ns].keys()):
			fid = mon.cleanfn(ns+"_"+name)
			cur = sts[ns][name]['generation']
			obs = sts[ns][name]['observed_generation']
			_print(f"f_{fid}_cur.value", cur)
			_print(f"f_{fid}_obs.value", obs)
	if mon.debug(): _print()
