# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def parse(nodes):
	mon.dbg('nodes_info parse')
	sts = dict(
		nodes = 0,
		condition = dict(),
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
			if not sts.get('nodes_type', None):
				sts['nodes_type'] = {}
			if not sts['nodes_type'].get(t, None):
				sts['nodes_type'][t] = 0
			sts['nodes_type'][t] += 1
			s = i.get('status', {})
			for c in s.get('conditions', []):
				if c['status'] == 'True':
					typ = c['type']
					if not sts['condition'].get(typ, None):
						sts['condition'][typ] = 0
					sts['condition'][typ] += 1
				else:
					typ = c['type']
					if not sts['condition'].get(typ, None):
						sts['condition'][typ] = 0
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
	for n in sts['nodes_type']:
		t = mon.cleanfn(n)
		_print(f"t_{t}.label", n)
		_print(f"t_{t}.colour COLOUR{tc}")
		_print(f"t_{t}.min 0")
		tc += 1
		if tc > 28: tc = 0
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
	for cn in sorted(sts['condition'].keys()):
		cid = mon.cleanfn(cn.lower())
		_print(f"c_{cid}.label {cn}")
		_print(f"c_{cid}.colour COLOUR{cc}")
		_print(f"c_{cid}.draw AREASTACK")
		_print(f"c_{cid}.min 0")
		cc += 1
		if cc > 28: cc = 0

def report(sts):
	mon.dbg('nodes_info report')
	# nodes
	_print('multigraph nodes')
	_print('a_total.value', sts['nodes'])
	for n in sts['nodes_type']:
		t = mon.cleanfn(n)
		_print(f"t_{t}.value", sts['nodes_type'][n])
	# condition
	_print('multigraph nodes_condition')
	for cn in sorted(sts['condition'].keys()):
		cid = mon.cleanfn(cn.lower())
		val = sts['condition'][cn]
		_print(f"c_{cid}.value", val)
