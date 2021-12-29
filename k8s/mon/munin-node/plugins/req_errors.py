# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

def _print(*args):
	print(*args)

def config(cluster, host, hostid, sts):
	# per second
	_print(f"multigraph web_request_{hostid}.errors")
	_print(f"graph_title {host} request errors")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category web')
	_print('graph_vlabel number per second')
	_print('graph_scale no')
	_print('graph_total', cluster, 'total')
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		fc = 0
		for status in sorted(sts[path].keys()):
			stid = mon.cleanfn(status)
			_print(f"req_{pathid}_{stid}.label {status} {path}")
			_print(f"req_{pathid}_{stid}.colour COLOUR{fc}")
			_print(f"req_{pathid}_{stid}.draw AREASTACK")
			_print(f"req_{pathid}_{stid}.type DERIVE")
			_print(f"req_{pathid}_{stid}.min 0")
			_print(f"req_{pathid}_{stid}.cdef req_{pathid}_{stid},1000,/")
			fc = mon.color(fc)
	if mon.debug(): _print()
	# per minute
	_print(f"multigraph web_request_{hostid}.errors_per_minute")
	_print(f"graph_title {host} request errors")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category web')
	_print('graph_vlabel number per minute')
	_print('graph_scale no')
	_print('graph_total', cluster, 'total')
	_print('graph_period minute')
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		fc = 0
		for status in sorted(sts[path].keys()):
			stid = mon.cleanfn(status)
			_print(f"req_{pathid}_{stid}.label {status} {path}")
			_print(f"req_{pathid}_{stid}.colour COLOUR{fc}")
			_print(f"req_{pathid}_{stid}.draw AREASTACK")
			_print(f"req_{pathid}_{stid}.type DERIVE")
			_print(f"req_{pathid}_{stid}.min 0")
			_print(f"req_{pathid}_{stid}.cdef req_{pathid}_{stid},1000,/")
			fc = mon.color(fc)
	if mon.debug(): _print()
	# per minute avg
	_print(f"multigraph web_request_{hostid}.errors_per_minute_avg")
	_print(f"graph_title {host} request errors average")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category web')
	_print('graph_vlabel number per minute')
	_print('graph_scale no')
	_print('graph_period minute')
	_print('req_avg.label average')
	_print('req_avg.colour COLOUR0')
	_print('req_avg.draw AREASTACK')
	_print('req_avg.type DERIVE')
	_print('req_avg.min 0')
	_print('req_avg.cdef req_avg,1000,/')
	_print('req_avg.warning 1')
	_print('req_avg.critical 2')
	if mon.debug(): _print()

def report(hostid, sts, sts_total):
	# per second
	_print(f"multigraph web_request_{hostid}.errors")
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for status in sorted(sts[path].keys()):
			stid = mon.cleanfn(status)
			value = mon.derive(sts[path][status])
			_print(f"req_{pathid}_{stid}.value", value)
	# per minute
	errors = 0
	_print(f"multigraph web_request_{hostid}.errors_per_minute")
	for path in sorted(sts.keys()):
		pathid = mon.cleanfn(path)
		for status in sorted(sts[path].keys()):
			stid = mon.cleanfn(status)
			value = mon.derive(sts[path][status])
			if value != 'U':
				errors += value
			_print(f"req_{pathid}_{stid}.value", value)
	# per minute avg
	total = 0
	for path in sorted(sts_total.keys()):
		pathid = mon.cleanfn(path)
		for method in sorted(sts_total.get(path, {}).keys()):
			methid = mon.cleanfn(method)
			for status in sorted(sts_total[path].get(method, {}).keys()):
				stid = mon.cleanfn(status)
				value = mon.derive(sts_total[path][method][status].get('count', 'U'))
				if value != 'U':
					total += value
	avg = 0
	if total > 0:
		avg = errors / total
	_print(f"multigraph web_request_{hostid}.errors_per_minute_avg")
	_print(f"req_avg.value", avg)
