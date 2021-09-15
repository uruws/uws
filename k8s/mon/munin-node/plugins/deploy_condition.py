# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def parse(deploy):
	mon.dbg('deploy_condition parse')
	sts = dict(
		condition = dict(),
		condition_index = dict(),
	)
	for c in i['status'].get('conditions', {}):
		c_typ = c['type']
		c_st = c['status']
		if not sts['condition_index'].get(c_typ, None):
			sts['condition_index'][c_typ] = 0
		if not sts['condition'].get(ns, None):
			sts['condition'][ns] = dict()
		if not sts['condition'][ns].get(name, None):
			sts['condition'][ns][name] = dict()
		if not sts['condition'][ns][name].get(c_typ, None):
			sts['condition'][ns][name][c_typ] = 0
		if c_st == 'True':
			sts['condition_index'][c_typ] += 1
			sts['condition'][ns][name][c_typ] += 1
	return sts

def config(sts):
	mon.dbg('deploy_condition config')
	cluster = mon.cluster()
	# condition index
	print('multigraph deploy_condition')
	print(f"graph_title {cluster} deployments condition")
	print('graph_args --base 1000 -l 0')
	print('graph_category deploy')
	print('graph_vlabel number')
	print('graph_printf %3.0lf')
	print('graph_scale yes')
	cc = 0
	for c in sorted(sts['condition_index'].keys()):
		cid = mon.cleanfn(c)
		print(f"c_{cid}.label", c)
		print(f"c_{cid}.colour COLOUR{cc}")
		print(f"c_{cid}.min 0")
		cc += 1
		if cc > 28:
			cc = 0
	if mon.debug(): print()
	# condition
	for ns in sorted(sts['condition'].keys()):
		for name in sorted(sts['condition'][ns].keys()):
			if mon.debug(): print()
			sid = mon.cleanfn(ns+"_"+name)
			print(f"multigraph deploy_condition.{sid}")
			print(f"graph_title {cluster} {ns}/{name} condition")
			print('graph_args --base 1000 -l 0')
			print('graph_category deploy')
			print('graph_vlabel number')
			print('graph_printf %3.0lf')
			print('graph_scale yes')
			cc = 0
			for c in sorted(sts['condition'][ns][name].keys()):
				cid = mon.cleanfn(c)
				print(f"c_{cid}.label", c)
				print(f"c_{cid}.colour COLOUR{cc}")
				print(f"c_{cid}.min 0")
				cc += 1
				if cc > 28:
					cc = 0
	if mon.debug(): print()

def report(sts):
	mon.dbg('deploy_info report')
	# condition index
	print('multigraph deploy_condition')
	for c in sorted(sts['condition_index'].keys()):
		cid = mon.cleanfn(c)
		print(f"c_{cid}.value", sts['condition_index'][c])
	if mon.debug(): print()
	# condition
	for ns in sorted(sts['condition'].keys()):
		for name in sorted(sts['condition'][ns].keys()):
			if mon.debug(): print()
			sid = mon.cleanfn(ns+"_"+name)
			print(f"multigraph deploy_condition.{sid}")
			for c in sorted(sts['condition'][ns][name].keys()):
				cid = mon.cleanfn(c)
				val = sts['condition'][ns][name][c]
				print(f"c_{cid}.value", val)
	if mon.debug(): print()
