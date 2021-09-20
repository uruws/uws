# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def config(host, hostid, sts):
	# total index
	print(f"multigraph web_request_{hostid}")
	print(f"graph_title {host} request")
	print('graph_args --base 1000 -l 0')
	print('graph_category web')
	print('graph_vlabel total number')
	print('graph_scale yes')
	print('graph_total total')
	fid = 0
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts[path].keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path][method].keys()):
				stid = mon.cleanfn(status)
				print(f"req_{pathid}_{methid}_{stid}.label {status} {method} {path}")
				print(f"req_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
				print(f"req_{pathid}_{methid}_{stid}.draw AREASTACK")
				print(f"req_{pathid}_{methid}_{stid}.min 0")
				fid = mon.color(fid)
	if mon.debug(): print()
	# total
	print(f"multigraph web_request_{hostid}.total")
	print(f"graph_title {host} request")
	print('graph_args --base 1000 -l 0')
	print('graph_category web')
	print('graph_vlabel total number')
	print('graph_scale yes')
	print('graph_total total')
	fid = 0
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts[path].keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path][method].keys()):
				stid = mon.cleanfn(status)
				print(f"req_{pathid}_{methid}_{stid}.label {status} {method} {path}")
				print(f"req_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
				print(f"req_{pathid}_{methid}_{stid}.draw AREASTACK")
				print(f"req_{pathid}_{methid}_{stid}.min 0")
				fid = mon.color(fid)
	if mon.debug(): print()
	# total count
	print(f"multigraph web_request_{hostid}.count")
	print(f"graph_title {host} request count")
	print('graph_args --base 1000 -l 0')
	print('graph_category web')
	print('graph_vlabel number per second')
	print('graph_scale no')
	print('graph_total total')
	fid = 0
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts[path].keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path][method].keys()):
				stid = mon.cleanfn(status)
				print(f"req_{pathid}_{methid}_{stid}.label {status} {method} {path}")
				print(f"req_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
				print(f"req_{pathid}_{methid}_{stid}.draw AREASTACK")
				print(f"req_{pathid}_{methid}_{stid}.type DERIVE")
				print(f"req_{pathid}_{methid}_{stid}.min 0")
				print(f"req_{pathid}_{methid}_{stid}.cdef req_{pathid}_{methid}_{stid},1000,/")
				fid = mon.color(fid)
	if mon.debug(): print()

def report(hostid, sts):
	# total index
	print(f"multigraph web_request_{hostid}")
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts[path].keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path][method].keys()):
				stid = mon.cleanfn(status)
				value = sts[path][method][status]['count']
				print(f"req_{pathid}_{methid}_{stid}.value {value}")
	if mon.debug(): print()
	# total
	print(f"multigraph web_request_{hostid}.total")
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts[path].keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path][method].keys()):
				stid = mon.cleanfn(status)
				value = sts[path][method][status]['count']
				print(f"req_{pathid}_{methid}_{stid}.value {value}")
	if mon.debug(): print()
	# total count
	print(f"multigraph web_request_{hostid}.count")
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts[path].keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts[path][method].keys()):
				stid = mon.cleanfn(status)
				value = mon.derive(sts[path][method][status]['count'])
				print(f"req_{pathid}_{methid}_{stid}.value {value}")
	if mon.debug(): print()
