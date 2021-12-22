# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def _print(*args):
	print(*args)

def config(cluster, host, hostid, sts):
	# per second
	_print(f"multigraph web_request_{hostid}.by_path")
	_print(f"graph_title {host} request by path")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category web')
	_print('graph_vlabel number per second')
	_print('graph_scale no')
	_print('graph_total', cluster, 'total')
	fc = 0
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		_print(f"req_{pathid}.label {path}")
		_print(f"req_{pathid}.colour COLOUR{fc}")
		_print(f"req_{pathid}.draw AREASTACK")
		_print(f"req_{pathid}.type DERIVE")
		_print(f"req_{pathid}.min 0")
		_print(f"req_{pathid}.cdef req_{pathid},1000,/")
		fc = mon.color(fc)
	if mon.debug(): _print()
	# per minute
	_print(f"multigraph web_request_{hostid}.by_path_per_minute")
	_print(f"graph_title {host} request by path")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category web')
	_print('graph_vlabel number per minute')
	_print('graph_scale no')
	_print('graph_total', cluster, 'total')
	_print('graph_period minute')
	fc = 0
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		_print(f"req_{pathid}.label {path}")
		_print(f"req_{pathid}.colour COLOUR{fc}")
		_print(f"req_{pathid}.draw AREASTACK")
		_print(f"req_{pathid}.type DERIVE")
		_print(f"req_{pathid}.min 0")
		_print(f"req_{pathid}.cdef req_{pathid},1000,/")
		fc = mon.color(fc)
	if mon.debug(): _print()

def report(hostid, sts):
	# per second
	_print(f"multigraph web_request_{hostid}.by_path")
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		value = mon.derive(sts[path])
		_print(f"req_{pathid}.value", value)
	if mon.debug(): _print()
	# per minute
	_print(f"multigraph web_request_{hostid}.by_path_per_minute")
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		value = mon.derive(sts[path])
		_print(f"req_{pathid}.value", value)
	if mon.debug(): _print()
