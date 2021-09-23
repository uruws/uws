# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon
import resp_total
import resp_time

def config(cluster, host, hostid, sts):
	# size index
	print(f"multigraph web_response_size_{hostid}")
	print(f"graph_title {host} response size")
	print('graph_args --base 1024 -l 0')
	print('graph_category web_size')
	print('graph_vlabel total bytes')
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
	# size total
	print(f"multigraph web_response_size_{hostid}.total")
	print(f"graph_title {host} response size")
	print('graph_args --base 1024 -l 0')
	print('graph_category web_size')
	print('graph_vlabel total bytes')
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
	# size count
	print(f"multigraph web_response_size_{hostid}.count")
	print(f"graph_title {host} response size count")
	print('graph_args --base 1024 -l 0')
	print('graph_category web_size')
	print('graph_vlabel bytes per second')
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
				print(f"resp_{pathid}_{methid}_{stid}.type DERIVE")
				print(f"resp_{pathid}_{methid}_{stid}.min 0")
				print(f"resp_{pathid}_{methid}_{stid}.cdef resp_{pathid}_{methid}_{stid},1000,/")
				fid += 1
	if mon.debug(): print()
	# size avg
	print(f"multigraph web_response_size_{hostid}.avg")
	print(f"graph_title {host} response size average")
	print('graph_args --base 1024 -l 0')
	print('graph_category web_size')
	print('graph_vlabel bytes per response')
	print('graph_scale yes')
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
	# size index
	print(f"multigraph web_response_size_{hostid}")
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts[path].keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path][method].keys()):
				stid = mon.cleanfn(status)
				value = sts[path][method][status]['size']
				print(f"resp_{pathid}_{methid}_{stid}.value {value}")
	if mon.debug(): print()
	# size total
	print(f"multigraph web_response_size_{hostid}.total")
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts[path].keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path][method].keys()):
				stid = mon.cleanfn(status)
				value = sts[path][method][status]['size']
				print(f"resp_{pathid}_{methid}_{stid}.value {value}")
	if mon.debug(): print()
	# size count
	print(f"multigraph web_response_size_{hostid}.count")
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts[path].keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path][method].keys()):
				stid = mon.cleanfn(status)
				value = mon.derive(sts[path][method][status]['size'])
				print(f"resp_{pathid}_{methid}_{stid}.value {value}")
	if mon.debug(): print()
	# size avg
	print(f"multigraph web_response_size_{hostid}.avg")
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts[path].keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path][method].keys()):
				stid = mon.cleanfn(status)
				s = sts[path][method][status]['size']
				c = sts[path][method][status]['count']
				if c > 0:
					value = s / c
				else:
					value = s
				print(f"resp_{pathid}_{methid}_{stid}.value {value}")
	if mon.debug(): print()
