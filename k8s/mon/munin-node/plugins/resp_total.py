# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def _print(*args):
	print(*args)

def config(cluster, host, hostid, sts):
	# total index
	_print(f"multigraph web_response_{hostid}")
	_print(f"graph_title {host} response")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category web_resp')
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
				_print(f"resp_{pathid}_{methid}_{stid}.label {status} {method} {path}")
				_print(f"resp_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
				_print(f"resp_{pathid}_{methid}_{stid}.draw AREASTACK")
				_print(f"resp_{pathid}_{methid}_{stid}.min 0")
				fid = mon.color(fid)
	if mon.debug(): _print()
	# total
	_print(f"multigraph web_response_{hostid}.total")
	_print(f"graph_title {host} response")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category web_resp')
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
				_print(f"resp_{pathid}_{methid}_{stid}.label {status} {method} {path}")
				_print(f"resp_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
				_print(f"resp_{pathid}_{methid}_{stid}.draw AREASTACK")
				_print(f"resp_{pathid}_{methid}_{stid}.min 0")
				fid = mon.color(fid)
	if mon.debug(): _print()
	# total count
	_print(f"multigraph web_response_{hostid}.count")
	_print(f"graph_title {host} response count")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category web_resp')
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
				_print(f"resp_{pathid}_{methid}_{stid}.label {status} {method} {path}")
				_print(f"resp_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
				_print(f"resp_{pathid}_{methid}_{stid}.draw AREASTACK")
				_print(f"resp_{pathid}_{methid}_{stid}.type DERIVE")
				_print(f"resp_{pathid}_{methid}_{stid}.min 0")
				_print(f"resp_{pathid}_{methid}_{stid}.cdef resp_{pathid}_{methid}_{stid},1000,/")
				fid = mon.color(fid)
	if mon.debug(): _print()

def report(hostid, sts):
	# total index
	_print(f"multigraph web_response_{hostid}")
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts.get(path, {}).keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path].get(method, {}).keys()):
				stid = mon.cleanfn(status)
				value = sts[path][method][status].get('count', 'U')
				_print(f"resp_{pathid}_{methid}_{stid}.value {value}")
	if mon.debug(): _print()
	# total
	_print(f"multigraph web_response_{hostid}.total")
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts.get(path, {}).keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path].get(method, {}).keys()):
				stid = mon.cleanfn(status)
				value = sts[path][method][status].get('count', 'U')
				_print(f"resp_{pathid}_{methid}_{stid}.value {value}")
	if mon.debug(): _print()
	# total count
	_print(f"multigraph web_response_{hostid}.count")
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts.get(path, {}).keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path].get(method, {}).keys()):
				stid = mon.cleanfn(status)
				value = mon.derive(sts[path][method][status].get('count', 'U'))
				_print(f"resp_{pathid}_{methid}_{stid}.value {value}")
	if mon.debug(): _print()
