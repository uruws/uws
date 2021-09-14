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
	sts['nodes'] = len(nodes['items'])
	for i in nodes['items']:
		if i['kind'] == 'Node':
			n = i['metadata']['name']
			t = i['metadata']['labels'].get('node.kubernetes.io/instance-type', 'unknown')
			if not sts['nodes_type'].get(t, None):
				sts['nodes_type'][t] = 0
			sts['nodes_type'][t] += 1
			for c in i['status']['conditions']:
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

def config(sts):
	mon.dbg('nodes_info config')
	cluster = mon.cluster()
	# nodes
	print('multigraph nodes')
	print(f"graph_title {cluster} nodes")
	print('graph_args --base 1000 -l 0')
	print('graph_category nodes')
	print('graph_vlabel number')
	print('graph_printf %3.0lf')
	print('graph_scale yes')
	print('a_total.label nodes')
	print('a_total.colour COLOUR0')
	print('a_total.draw AREASTACK')
	print('a_total.min 0')
	tc = 1
	for n in sts['nodes_type']:
		t = mon.cleanfn(n)
		print(f"t_{t}.label", n)
		print(f"t_{t}.colour COLOUR{tc}")
		print(f"t_{t}.min 0")
		tc += 1
		if tc > 28:
			tc = 0
	# condition
	print('multigraph nodes_condition')
	print(f"graph_title {cluster} nodes condition")
	print('graph_args --base 1000 -l 0')
	print('graph_category nodes')
	print('graph_vlabel number')
	print('graph_printf %3.0lf')
	print('graph_scale yes')
	print('graph_total total')
	cc = 0
	for cn in sorted(sts['condition'].keys()):
		cid = mon.cleanfn(cn.lower())
		print(f"c_{cid}.label {cn}")
		print(f"c_{cid}.colour COLOUR{cc}")
		print(f"c_{cid}.draw AREASTACK")
		print(f"c_{cid}.min 0")
		cc += 1
		if cc > 28:
			cc = 0

def report(sts):
	mon.dbg('nodes_info report')
	# nodes
	print('multigraph nodes')
	print('a_total.value', sts['nodes'])
	for n in sts['nodes_type']:
		t = mon.cleanfn(n)
		print(f"t_{t}.value", sts['nodes_type'][n])
	# condition
	print('multigraph nodes_condition')
	for cn in sorted(sts['condition'].keys()):
		cid = mon.cleanfn(cn.lower())
		val = sts['condition'][cn]
		print(f"c_{cid}.value", val)
