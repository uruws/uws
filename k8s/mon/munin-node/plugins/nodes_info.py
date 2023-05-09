# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

limits = {
	'Unknown': {
		'warning': 3,
		'critical': 5,
	},
}

def parse(nodes):
	mon.dbg('nodes_info parse')
	sts = dict(
		nodes = 0,
		condition = dict(
			Unknown = 0,
		),
		nodes_type = dict(),
	)
	items = nodes.get('items', [])
	sts['nodes'] = len(items)
	for i in items:
		kind = i.get('kind', None)
		if kind == 'Node':
			m = i.get('metadata', {})
			n = m.get('name', None)
			t = m.get('labels', {}).get('node.kubernetes.io/instance-type', 'unknown')
			# type
			if not sts.get('nodes_type', None):
				sts['nodes_type'] = {}
			if not sts['nodes_type'].get(t, None):
				sts['nodes_type'][t] = 0
			sts['nodes_type'][t] += 1
			# conditions
			s = i.get('status', {})
			for c in s.get('conditions', []):
				typ = c['type']
				if not sts['condition'].get(typ, None):
					sts['condition'][typ] = 0
				if c['status'] == 'True':
					sts['condition'][typ] += 1
				elif c['status'] == 'Unknown':
					if typ == 'Ready':
						sts['condition']['Unknown'] += 1
	return sts

def _print(*args):
	print(*args)

def config(sts):
	mon.dbg('nodes_info config')
	cluster = mon.cluster()
	# nodes
	_print('multigraph nodes')
	_print(f"graph_title {cluster} nodes")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category nodes')
	_print('graph_vlabel number')
	_print('graph_printf %3.0lf')
	_print('graph_scale yes')
	_print('a_total.label nodes')
	_print('a_total.colour COLOUR0')
	_print('a_total.draw AREASTACK')
	_print('a_total.min 0')
	tc = 1
	for n in sts.get('nodes_type', []):
		t = mon.cleanfn(n)
		_print(f"t_{t}.label", n)
		_print(f"t_{t}.colour COLOUR{tc}")
		_print(f"t_{t}.min 0")
		tc = mon.color(tc)
	# condition
	_print('multigraph nodes_condition')
	_print(f"graph_title {cluster} nodes condition")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category nodes')
	_print('graph_vlabel number')
	_print('graph_printf %3.0lf')
	_print('graph_scale yes')
	_print('graph_total total')
	cc = 0
	for cn in sorted(sts.get('condition', {}).keys()):
		cid = mon.cleanfn(cn.lower())
		_print(f"c_{cid}.label {cn}")
		_print(f"c_{cid}.colour COLOUR{cc}")
		_print(f"c_{cid}.draw AREASTACK")
		_print(f"c_{cid}.min 0")
		l = limits.get(cn, {})
		if l:
			warn = l.get('warning', 0)
			if warn > 0:
				_print(f"c_{cid}.warning", warn)
			crit = l.get('critical', 0)
			if crit > 0:
				_print(f"c_{cid}.critical", crit)
		cc = mon.color(cc)

def report(sts):
	mon.dbg('nodes_info report')
	# nodes
	_print('multigraph nodes')
	_print('a_total.value', sts.get('nodes', 'U'))
	for n in sts.get('nodes_type', []):
		t = mon.cleanfn(n)
		_print(f"t_{t}.value", sts['nodes_type'][n])
	# condition
	_print('multigraph nodes_condition')
	for cn in sorted(sts.get('condition', {}).keys()):
		cid = mon.cleanfn(cn.lower())
		val = sts['condition'][cn]
		_print(f"c_{cid}.value", val)
