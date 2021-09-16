# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def parse(m, st):
	return dict(
		generation = m.get('generation', 'U'),
		observed_generation = st.get('observedGeneration', 'U'),
	)

def config(sts):
	cluster = mon.cluster()
	print('multigraph deploy_generation')
	print(f"graph_title {cluster} deployments generation")
	print('graph_args --base 1000 -l 0')
	print('graph_category deploy')
	print('graph_vlabel number')
	print('graph_printf %3.0lf')
	print('graph_scale yes')
	fc = 0
	for ns in sorted(sts.keys()):
		for name in sorted(sts[ns].keys()):
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
	print('multigraph deploy_generation')
	for ns in sorted(sts.keys()):
		for name in sorted(sts[ns].keys()):
			fid = mon.cleanfn(ns+"_"+name)
			cur = sts[ns][name]['generation']
			obs = sts[ns][name]['observed_generation']
			print(f"f_{fid}_cur.value", cur)
			print(f"f_{fid}_obs.value", obs)
	if mon.debug(): print()
