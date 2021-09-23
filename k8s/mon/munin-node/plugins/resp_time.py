# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def config(cluster, host, hostid, sts):
	# time index
	print(f"multigraph web_response_time_{hostid}")
	print(f"graph_title {host} response time")
	print('graph_args --base 1000 -l 0')
	print('graph_category web_time')
	print('graph_vlabel total seconds')
	print('graph_scale yes')
	print('graph_total', cluster, 'total')
	fid = 0
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts[path].keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path][method].keys()):
				stid = mon.cleanfn(status)
				print(f"resp_{pathid}_{methid}_{stid}.label {status} {method} {path}")
				print(f"resp_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
				print(f"resp_{pathid}_{methid}_{stid}.draw AREASTACK")
				print(f"resp_{pathid}_{methid}_{stid}.min 0")
				fid += 1
	if mon.debug(): print()
	# time total
	print(f"multigraph web_response_time_{hostid}.total")
	print(f"graph_title {host} response time")
	print('graph_args --base 1000 -l 0')
	print('graph_category web_time')
	print('graph_vlabel total seconds')
	print('graph_scale yes')
	print('graph_total', cluster, 'total')
	fid = 0
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts[path].keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path][method].keys()):
				stid = mon.cleanfn(status)
				print(f"resp_{pathid}_{methid}_{stid}.label {status} {method} {path}")
				print(f"resp_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
				print(f"resp_{pathid}_{methid}_{stid}.draw AREASTACK")
				print(f"resp_{pathid}_{methid}_{stid}.min 0")
				fid += 1
	if mon.debug(): print()
	# time count
	print(f"multigraph web_response_time_{hostid}.count")
	print(f"graph_title {host} response time count")
	print('graph_args --base 1000 -l 0')
	print('graph_category web_time')
	print('graph_vlabel time per second')
	print('graph_scale no')
	print('graph_total', cluster, 'total')
	fid = 0
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts[path].keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path][method].keys()):
				stid = mon.cleanfn(status)
				print(f"resp_{pathid}_{methid}_{stid}.label {status} {method} {path}")
				print(f"resp_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
				print(f"resp_{pathid}_{methid}_{stid}.draw AREASTACK")
				print(f"resp_{pathid}_{methid}_{stid}.type DERIVE")
				print(f"resp_{pathid}_{methid}_{stid}.min 0")
				print(f"resp_{pathid}_{methid}_{stid}.cdef resp_{pathid}_{methid}_{stid},1000,/")
				fid += 1
	if mon.debug(): print()
	# time avg
	print(f"multigraph web_response_time_{hostid}.avg")
	print(f"graph_title {host} response time average")
	print('graph_args --base 1000 -l 0')
	print('graph_category web_time')
	print('graph_vlabel seconds per response')
	print('graph_scale no')
	fid = 0
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts[path].keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path][method].keys()):
				stid = mon.cleanfn(status)
				print(f"resp_{pathid}_{methid}_{stid}.label {status} {method} {path}")
				print(f"resp_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
				print(f"resp_{pathid}_{methid}_{stid}.min 0")
				fid += 1
	if mon.debug(): print()

def report(hostid, sts):
	# time index
	print(f"multigraph web_response_time_{hostid}")
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts[path].keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path][method].keys()):
				stid = mon.cleanfn(status)
				value = sts[path][method][status]['time']
				print(f"resp_{pathid}_{methid}_{stid}.value {value}")
	if mon.debug(): print()
	# time total
	print(f"multigraph web_response_time_{hostid}.total")
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts[path].keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path][method].keys()):
				stid = mon.cleanfn(status)
				value = sts[path][method][status]['time']
				print(f"resp_{pathid}_{methid}_{stid}.value {value}")
	if mon.debug(): print()
	# time count
	print(f"multigraph web_response_time_{hostid}.count")
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts[path].keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path][method].keys()):
				stid = mon.cleanfn(status)
				value = mon.derive(sts[path][method][status]['time'])
				print(f"resp_{pathid}_{methid}_{stid}.value {value}")
	if mon.debug(): print()
	# time avg
	print(f"multigraph web_response_time_{hostid}.avg")
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts[path].keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path][method].keys()):
				stid = mon.cleanfn(status)
				t = sts[path][method][status]['time']
				c = sts[path][method][status]['count']
				if c > 0:
					value = t / c
				else:
					value = t
				print(f"resp_{pathid}_{methid}_{stid}.value {value}")
	if mon.debug(): print()
