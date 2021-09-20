# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def config(host, hostid, sts):
	# per second
	print(f"multigraph web_request_{hostid}.by_path")
	print(f"graph_title {host} request by path")
	print('graph_args --base 1000 -l 0')
	print('graph_category web')
	print('graph_vlabel number per second')
	print('graph_scale no')
	print('graph_total total')
	fc = 0
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		print(f"req_{pathid}.label {path}")
		print(f"req_{pathid}.colour COLOUR{fc}")
		print(f"req_{pathid}.draw AREASTACK")
		print(f"req_{pathid}.type DERIVE")
		print(f"req_{pathid}.min 0")
		print(f"req_{pathid}.cdef req_{pathid},1000,/")
		fc = mon.color(fc)
	if mon.debug(): print()
	# per minute
	print(f"multigraph web_request_{hostid}.by_path_per_minute")
	print(f"graph_title {host} request by path")
	print('graph_args --base 1000 -l 0')
	print('graph_category web')
	print('graph_vlabel number per minute')
	print('graph_scale no')
	print('graph_total total')
	print('graph_period minute')
	fc = 0
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		print(f"req_{pathid}.label {path}")
		print(f"req_{pathid}.colour COLOUR{fc}")
		print(f"req_{pathid}.draw AREASTACK")
		print(f"req_{pathid}.type DERIVE")
		print(f"req_{pathid}.min 0")
		print(f"req_{pathid}.cdef req_{pathid},1000,/")
		fc = mon.color(fc)
	if mon.debug(): print()

def report(hostid, sts):
	# per second
	print(f"multigraph web_request_{hostid}.by_path")
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		value = mon.derive(sts[path])
		print(f"req_{pathid}.value", value)
	if mon.debug(): print()
	# per minute
	print(f"multigraph web_request_{hostid}.by_path_per_minute")
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		value = mon.derive(sts[path])
		print(f"req_{pathid}.value", value)
	if mon.debug(): print()
