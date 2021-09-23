# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def config(cluster, host, hostid, sts):
	# per second
	print(f"multigraph web_request_{hostid}.errors")
	print(f"graph_title {host} request errors")
	print('graph_args --base 1000 -l 0')
	print('graph_category web')
	print('graph_vlabel number per second')
	print('graph_scale no')
	print('graph_total', cluster, 'total')
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		fc = 0
		for status in sorted(sts[path].keys()):
			stid = mon.cleanfn(status)
			print(f"req_{pathid}_{stid}.label {status} {path}")
			print(f"req_{pathid}_{stid}.colour COLOUR{fc}")
			print(f"req_{pathid}_{stid}.draw AREASTACK")
			print(f"req_{pathid}_{stid}.type DERIVE")
			print(f"req_{pathid}_{stid}.min 0")
			print(f"req_{pathid}_{stid}.cdef req_{pathid}_{stid},1000,/")
			fc = mon.color(fc)
	if mon.debug(): print()
	# per minute
	print(f"multigraph web_request_{hostid}.errors_per_minute")
	print(f"graph_title {host} request errors")
	print('graph_args --base 1000 -l 0')
	print('graph_category web')
	print('graph_vlabel number per minute')
	print('graph_scale no')
	print('graph_total', cluster, 'total')
	print('graph_period minute')
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		fc = 0
		for status in sorted(sts[path].keys()):
			stid = mon.cleanfn(status)
			print(f"req_{pathid}_{stid}.label {status} {path}")
			print(f"req_{pathid}_{stid}.colour COLOUR{fc}")
			print(f"req_{pathid}_{stid}.draw AREASTACK")
			print(f"req_{pathid}_{stid}.type DERIVE")
			print(f"req_{pathid}_{stid}.min 0")
			print(f"req_{pathid}_{stid}.cdef req_{pathid}_{stid},1000,/")
			fc = mon.color(fc)
	if mon.debug(): print()

def report(hostid, sts):
	# per second
	print(f"multigraph web_request_{hostid}.errors")
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for status in sorted(sts[path].keys()):
			stid = mon.cleanfn(status)
			value = mon.derive(sts[path][status])
			print(f"req_{pathid}_{stid}.value", value)
	# per minute
	print(f"multigraph web_request_{hostid}.errors_per_minute")
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for status in sorted(sts[path].keys()):
			stid = mon.cleanfn(status)
			value = mon.derive(sts[path][status])
			print(f"req_{pathid}_{stid}.value", value)
