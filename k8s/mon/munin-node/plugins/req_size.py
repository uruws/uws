# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def _print(*args):
	print(*args)

def config(cluster, host, hostid, sts):
	# size index
	_print(f"multigraph web_request_size_{hostid}")
	_print(f"graph_title {host} request size")
	_print('graph_args --base 1024 -l 0')
	_print('graph_category web_size')
	_print('graph_vlabel total bytes')
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
	# size total
	_print(f"multigraph web_request_size_{hostid}.total")
	_print(f"graph_title {host} request size")
	_print('graph_args --base 1024 -l 0')
	_print('graph_category web_size')
	_print('graph_vlabel total bytes')
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
	# size count
	_print(f"multigraph web_request_size_{hostid}.count")
	_print(f"graph_title {host} request size count")
	_print('graph_args --base 1024 -l 0')
	_print('graph_category web_size')
	_print('graph_vlabel bytes per second')
	_print('graph_scale yes')
	_print('graph_total', cluster, 'total')
	fid = 0
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts[path].keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path][method].keys()):
				stid = mon.cleanfn(status)
				_print(f"req_{pathid}_{methid}_{stid}.label {status} {method} {path}")
				_print(f"req_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
				_print(f"req_{pathid}_{methid}_{stid}.draw AREASTACK")
				_print(f"req_{pathid}_{methid}_{stid}.type DERIVE")
				_print(f"req_{pathid}_{methid}_{stid}.min 0")
				_print(f"req_{pathid}_{methid}_{stid}.cdef req_{pathid}_{methid}_{stid},1000,/")
				fid = mon.color(fid)
	if mon.debug(): _print()
	# size avg
	_print(f"multigraph web_request_size_{hostid}.avg")
	_print(f"graph_title {host} request size average")
	_print('graph_args --base 1024 -l 0')
	_print('graph_category web_size')
	_print('graph_vlabel bytes per response')
	_print('graph_scale yes')
	fid = 0
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts.get(path, {}).keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path].get(method, {}).keys()):
				stid = mon.cleanfn(status)
				_print(f"req_{pathid}_{methid}_{stid}.label {status} {method} {path}")
				_print(f"req_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
				_print(f"req_{pathid}_{methid}_{stid}.min 0")
				fid = mon.color(fid)
	if mon.debug(): _print()

def report(hostid, sts):
	# size index
	_print(f"multigraph web_request_size_{hostid}")
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts.get(path, {}).keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path].get(method, {}).keys()):
				stid = mon.cleanfn(status)
				value = sts[path][method][status].get('size', 'U')
				_print(f"req_{pathid}_{methid}_{stid}.value {value}")
	if mon.debug(): _print()
	# size total
	_print(f"multigraph web_request_size_{hostid}.total")
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts.get(path, {}).keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path].get(method, {}).keys()):
				stid = mon.cleanfn(status)
				value = sts[path][method][status].get('size', 'U')
				_print(f"req_{pathid}_{methid}_{stid}.value {value}")
	if mon.debug(): _print()
	# size count
	_print(f"multigraph web_request_size_{hostid}.count")
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts.get(path, {}).keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path].get(method, {}).keys()):
				stid = mon.cleanfn(status)
				value = mon.derive(sts[path][method][status].get('size', 'U'))
				_print(f"req_{pathid}_{methid}_{stid}.value {value}")
	if mon.debug(): _print()
	# size avg
	_print(f"multigraph web_request_size_{hostid}.avg")
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts.get(path, {}).keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path].get(method, {}).keys()):
				stid = mon.cleanfn(status)
				s = sts[path][method][status].get('size', 'U')
				c = sts[path][method][status].get('count', 0)
				if c > 0:
					value = s / c
				else:
					value = s
				_print(f"req_{pathid}_{methid}_{stid}.value {value}")
	if mon.debug(): _print()
