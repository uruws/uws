# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def parse(sts, ns, name, i):
	if not sts.get('condition_index', None):
		sts['condition_index'] = {}
	if not sts.get('condition', None):
		sts['condition'] = {}
	if not sts['condition'].get(ns, None):
		sts['condition'][ns] = {}
	if not sts['condition'][ns].get(name, None):
		sts['condition'][ns][name] = {
			'Available': 0,
		}
	for c in i.get('status', {}).get('conditions', []):
		c_typ = c['type']
		c_st = c['status']
		if not sts['condition_index'].get(c_typ, None):
			sts['condition_index'][c_typ] = 0
		if not sts['condition'][ns][name].get(c_typ, None):
			sts['condition'][ns][name][c_typ] = 0
		if c_st == 'True':
			sts['condition_index'][c_typ] += 1
			sts['condition'][ns][name][c_typ] += 1

def _print(*args):
	print(*args)

def config(sts):
	mon.dbg('deploy_condition config')
	cluster = mon.cluster()
	# condition index
	_print('multigraph deploy_condition')
	_print(f"graph_title {cluster} deployments condition")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category deploy')
	_print('graph_vlabel number')
	_print('graph_printf %3.0lf')
	_print('graph_scale yes')
	cc = 0
	for c in sorted(sts.get('condition_index', {}).keys()):
		cid = mon.cleanfn(c)
		_print(f"c_{cid}.label", c)
		_print(f"c_{cid}.colour COLOUR{cc}")
		_print(f"c_{cid}.min 0")
		cc = mon.color(cc)
	if mon.debug(): _print()
	# condition
	for ns in sorted(sts.get('condition', {}).keys()):
		for name in sorted(sts['condition'].get(ns, {}).keys()):
			sid = mon.cleanfn(ns+"_"+name)
			_print(f"multigraph deploy_condition.{sid}")
			_print(f"graph_title {cluster} {ns}/{name} condition")
			_print('graph_args --base 1000 -l 0')
			_print('graph_category deploy')
			_print('graph_vlabel number of deployments')
			_print('graph_printf %3.0lf')
			_print('graph_scale yes')
			cc = 0
			for c in sorted(sts['condition'][ns][name].keys()):
				cid = mon.cleanfn(c)
				_print(f"c_{cid}.label", c)
				_print(f"c_{cid}.colour COLOUR{cc}")
				_print(f"c_{cid}.min 0")
				cc = mon.color(cc)
			if mon.debug(): _print()

def report(sts):
	mon.dbg('deploy_condition report')
	# condition index
	_print('multigraph deploy_condition')
	for c in sorted(sts['condition_index'].keys()):
		cid = mon.cleanfn(c)
		_print(f"c_{cid}.value", sts['condition_index'][c])
	if mon.debug(): _print()
	# condition
	for ns in sorted(sts['condition'].keys()):
		for name in sorted(sts['condition'][ns].keys()):
			sid = mon.cleanfn(ns+"_"+name)
			_print(f"multigraph deploy_condition.{sid}")
			for c in sorted(sts['condition'][ns][name].keys()):
				cid = mon.cleanfn(c)
				val = sts['condition'][ns][name][c]
				_print(f"c_{cid}.value", val)
			if mon.debug(): _print()
