# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def _print(*args):
	print(*args)

def config(cluster, host, hostid, sts):
	# total index
	_print(f"multigraph web_request_{hostid}")
	_print(f"graph_title {host} request")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category web')
	_print('graph_vlabel total number')
	_print('graph_scale yes')
	_print('graph_total', cluster, 'total')
	fid = 0
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts.get(path, {}).keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path].get(method, {}).keys()):
				stid = mon.cleanfn(status)
				_print(f"req_{pathid}_{methid}_{stid}.label {status} {method} {path}")
				_print(f"req_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
				_print(f"req_{pathid}_{methid}_{stid}.draw AREASTACK")
				_print(f"req_{pathid}_{methid}_{stid}.min 0")
				fid = mon.color(fid)
	if mon.debug(): _print()
	# total
	_print(f"multigraph web_request_{hostid}.total")
	_print(f"graph_title {host} request")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category web')
	_print('graph_vlabel total number')
	_print('graph_scale yes')
	_print('graph_total', cluster, 'total')
	fid = 0
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts.get(path, {}).keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path].get(method, {}).keys()):
				stid = mon.cleanfn(status)
				_print(f"req_{pathid}_{methid}_{stid}.label {status} {method} {path}")
				_print(f"req_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
				_print(f"req_{pathid}_{methid}_{stid}.draw AREASTACK")
				_print(f"req_{pathid}_{methid}_{stid}.min 0")
				fid = mon.color(fid)
	if mon.debug(): _print()
	# total count
	_print(f"multigraph web_request_{hostid}.count")
	_print(f"graph_title {host} request count")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category web')
	_print('graph_vlabel number per second')
	_print('graph_scale no')
	_print('graph_total', cluster, 'total')
	fid = 0
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts.get(path, {}).keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path].get(method, {}).keys()):
				stid = mon.cleanfn(status)
				_print(f"req_{pathid}_{methid}_{stid}.label {status} {method} {path}")
				_print(f"req_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
				_print(f"req_{pathid}_{methid}_{stid}.draw AREASTACK")
				_print(f"req_{pathid}_{methid}_{stid}.type DERIVE")
				_print(f"req_{pathid}_{methid}_{stid}.min 0")
				_print(f"req_{pathid}_{methid}_{stid}.cdef req_{pathid}_{methid}_{stid},1000,/")
				fid = mon.color(fid)
	if mon.debug(): _print()
	# total count per minute
	_print(f"multigraph web_request_{hostid}.count_per_minute")
	_print(f"graph_title {host} request count")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category web')
	_print('graph_vlabel number per minute')
	_print('graph_scale no')
	_print('graph_total', cluster, 'total')
	_print('graph_period minute')
	fid = 0
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts.get(path, {}).keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path].get(method, {}).keys()):
				stid = mon.cleanfn(status)
				_print(f"req_{pathid}_{methid}_{stid}.label {status} {method} {path}")
				_print(f"req_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
				_print(f"req_{pathid}_{methid}_{stid}.draw AREASTACK")
				_print(f"req_{pathid}_{methid}_{stid}.type DERIVE")
				_print(f"req_{pathid}_{methid}_{stid}.min 0")
				_print(f"req_{pathid}_{methid}_{stid}.cdef req_{pathid}_{methid}_{stid},1000,/")
				fid = mon.color(fid)
	if mon.debug(): _print()

def report(hostid, sts):
	# total index
	_print(f"multigraph web_request_{hostid}")
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts.get(path, {}).keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path].get(method, {}).keys()):
				stid = mon.cleanfn(status)
				value = sts[path][method][status].get('count', 'U')
				_print(f"req_{pathid}_{methid}_{stid}.value {value}")
	if mon.debug(): _print()
	# total
	_print(f"multigraph web_request_{hostid}.total")
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts.get(path, {}).keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path].get(method, {}).keys()):
				stid = mon.cleanfn(status)
				value = sts[path][method][status].get('count', 'U')
				_print(f"req_{pathid}_{methid}_{stid}.value {value}")
	if mon.debug(): _print()
	# total count
	_print(f"multigraph web_request_{hostid}.count")
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts.get(path, {}).keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path].get(method, {}).keys()):
				stid = mon.cleanfn(status)
				value = mon.derive(sts[path][method][status].get('count', 'U'))
				_print(f"req_{pathid}_{methid}_{stid}.value {value}")
	if mon.debug(): _print()
	# total count per minute
	_print(f"multigraph web_request_{hostid}.count_per_minute")
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts.get(path, {}).keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path].get(method, {}).keys()):
				stid = mon.cleanfn(status)
				value = mon.derive(sts[path][method][status].get('count', 'U'))
				_print(f"req_{pathid}_{methid}_{stid}.value {value}")
	if mon.debug(): _print()
