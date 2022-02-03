# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def parse(nodes):
	mon.dbg('nodes_taint parse')
	sts = dict(
		NoExecute = 0,
		NoSchedule = 0,
		PreferNoSchedule = 0,
		Unknown = 0,
	)
	items = nodes.get('items', [])
	for i in items:
		kind = i.get('kind', None)
		if kind == 'Node':
			s = i.get('spec', {})
			for t in s.get('taints', []):
				effect = t.get('effect', 'Unknown')
				if sts.get(effect, None) is None:
					sts[effect] = 0
				sts[effect] += 1
	return sts

def _print(*args):
	print(*args)

def config(sts):
	mon.dbg('nodes_taint config')
	cluster = mon.cluster()
	_print('multigraph nodes_taint')
	_print(f"graph_title {cluster} nodes taint")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category nodes')
	_print('graph_vlabel number')
	_print('graph_printf %3.0lf')
	_print('graph_scale yes')
	color = 0
	for t in sorted(sts.keys()):
		tid = mon.cleanfn(t.lower())
		_print(f"t_{tid}.label {t}")
		_print(f"t_{tid}.colour COLOUR{color}")
		_print(f"t_{tid}.draw LINE")
		_print(f"t_{tid}.min 0")
		if not t.startswith('Prefer'):
			_print(f"t_{tid}.warning", 1)
			_print(f"t_{tid}.critical", 3)
		color = mon.color(color)

def report(sts):
	mon.dbg('nodes_taint report')
	_print('multigraph nodes_taint')
	for t in sorted(sts.keys()):
		tid = mon.cleanfn(t.lower())
		_print(f"t_{tid}.value", sts[t])
