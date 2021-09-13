# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

from time import time

sts = dict()

def __parse(name, meta, value):
	global sts
	host = meta.get('host', '_')
	if host == '_':
		host = 'default'
	if not sts.get(host, None):
		sts[host] = dict()
	path = meta.get('path', '')
	if path == '':
		path = 'default'
	if not sts[host].get(path, None):
		sts[host][path] = dict()
	method = meta.get('method', '')
	if method == '':
		method = 'default'
	if not sts[host][path].get(method, None):
		sts[host][path][method] = dict()
	status = meta.get('status', '')
	if status == '':
		status = 'unknown'
	if not sts[host][path][method].get(status, None):
		sts[host][path][method][status] = dict(
			count = 0, size = 0, time = 0)
	mon.dbg('parse web_request:', name, host, path, method, status)
	sts[host][path][method][status][name] += value
	return True

def parse(name, meta, value):
	if name == 'nginx_ingress_controller_request_duration_seconds_sum':
		return __parse('time', meta, value)
	elif name == 'nginx_ingress_controller_request_duration_seconds_count':
		return __parse('count', meta, value)
	elif name == 'nginx_ingress_controller_request_size_sum':
		return __parse('size', meta, value)
	return False

def config(sts):
	mon.dbg('config web_request')
	for host in sorted(sts.keys()):
		hostid = mon.cleanfn(host)
		# total index
		print(f"multigraph web_request_{hostid}")
		print(f"graph_title {host} request")
		print('graph_args --base 1000 -l 0')
		print('graph_category web')
		print('graph_vlabel total number')
		print('graph_scale yes')
		print('graph_total total')
		fid = 0
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					print(f"req_{pathid}_{methid}_{stid}.label {status} {method} {path}")
					print(f"req_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
					print(f"req_{pathid}_{methid}_{stid}.draw AREASTACK")
					print(f"req_{pathid}_{methid}_{stid}.min 0")
					fid += 1
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
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					print(f"req_{pathid}_{methid}_{stid}.label {status} {method} {path}")
					print(f"req_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
					print(f"req_{pathid}_{methid}_{stid}.draw AREASTACK")
					print(f"req_{pathid}_{methid}_{stid}.min 0")
					fid += 1
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
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					print(f"req_{pathid}_{methid}_{stid}.label {status} {method} {path}")
					print(f"req_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
					print(f"req_{pathid}_{methid}_{stid}.draw AREASTACK")
					print(f"req_{pathid}_{methid}_{stid}.type DERIVE")
					print(f"req_{pathid}_{methid}_{stid}.min 0")
					print(f"req_{pathid}_{methid}_{stid}.cdef req_{pathid}_{methid}_{stid},1000,/")
					fid += 1
		if mon.debug(): print()
		# time index
		print(f"multigraph web_request_time_{hostid}")
		print(f"graph_title {host} request time")
		print('graph_args --base 1000 -l 0')
		print('graph_category web_time')
		print('graph_vlabel total seconds')
		print('graph_scale yes')
		print('graph_total total')
		fid = 0
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					print(f"req_{pathid}_{methid}_{stid}.label {status} {method} {path}")
					print(f"req_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
					print(f"req_{pathid}_{methid}_{stid}.draw AREASTACK")
					print(f"req_{pathid}_{methid}_{stid}.min 0")
					fid += 1
		if mon.debug(): print()
		# time total
		print(f"multigraph web_request_time_{hostid}.total")
		print(f"graph_title {host} request time")
		print('graph_args --base 1000 -l 0')
		print('graph_category web_time')
		print('graph_vlabel total seconds')
		print('graph_scale yes')
		print('graph_total total')
		fid = 0
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					print(f"req_{pathid}_{methid}_{stid}.label {status} {method} {path}")
					print(f"req_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
					print(f"req_{pathid}_{methid}_{stid}.draw AREASTACK")
					print(f"req_{pathid}_{methid}_{stid}.min 0")
					fid += 1
		if mon.debug(): print()
		# time count
		print(f"multigraph web_request_time_{hostid}.count")
		print(f"graph_title {host} request time count")
		print('graph_args --base 1000 -l 0')
		print('graph_category web_time')
		print('graph_vlabel time per second')
		print('graph_scale no')
		print('graph_total total')
		fid = 0
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					print(f"req_{pathid}_{methid}_{stid}.label {status} {method} {path}")
					print(f"req_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
					print(f"req_{pathid}_{methid}_{stid}.draw AREASTACK")
					print(f"req_{pathid}_{methid}_{stid}.type DERIVE")
					print(f"req_{pathid}_{methid}_{stid}.min 0")
					print(f"req_{pathid}_{methid}_{stid}.cdef req_{pathid}_{methid}_{stid},1000,/")
					fid += 1
		if mon.debug(): print()
		# time avg
		print(f"multigraph web_request_time_{hostid}.avg")
		print(f"graph_title {host} request time average")
		print('graph_args --base 1000 -l 0')
		print('graph_category web_time')
		print('graph_vlabel seconds per response')
		print('graph_scale no')
		fid = 0
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					print(f"req_{pathid}_{methid}_{stid}.label {status} {method} {path}")
					print(f"req_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
					print(f"req_{pathid}_{methid}_{stid}.min 0")
					fid += 1
		if mon.debug(): print()
		# size index
		print(f"multigraph web_request_size_{hostid}")
		print(f"graph_title {host} request size")
		print('graph_args --base 1024 -l 0')
		print('graph_category web_size')
		print('graph_vlabel total bytes')
		print('graph_scale yes')
		print('graph_total total')
		fid = 0
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					print(f"req_{pathid}_{methid}_{stid}.label {status} {method} {path}")
					print(f"req_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
					print(f"req_{pathid}_{methid}_{stid}.draw AREASTACK")
					print(f"req_{pathid}_{methid}_{stid}.min 0")
					fid += 1
		if mon.debug(): print()
		# size total
		print(f"multigraph web_request_size_{hostid}.total")
		print(f"graph_title {host} request size")
		print('graph_args --base 1024 -l 0')
		print('graph_category web_size')
		print('graph_vlabel total bytes')
		print('graph_scale yes')
		print('graph_total total')
		fid = 0
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					print(f"req_{pathid}_{methid}_{stid}.label {status} {method} {path}")
					print(f"req_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
					print(f"req_{pathid}_{methid}_{stid}.draw AREASTACK")
					print(f"req_{pathid}_{methid}_{stid}.min 0")
					fid += 1
		if mon.debug(): print()
		# size count
		print(f"multigraph web_request_size_{hostid}.count")
		print(f"graph_title {host} request size count")
		print('graph_args --base 1024 -l 0')
		print('graph_category web_size')
		print('graph_vlabel bytes per second')
		print('graph_scale yes')
		print('graph_total total')
		fid = 0
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					print(f"req_{pathid}_{methid}_{stid}.label {status} {method} {path}")
					print(f"req_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
					print(f"req_{pathid}_{methid}_{stid}.draw AREASTACK")
					print(f"req_{pathid}_{methid}_{stid}.type DERIVE")
					print(f"req_{pathid}_{methid}_{stid}.min 0")
					print(f"req_{pathid}_{methid}_{stid}.cdef req_{pathid}_{methid}_{stid},1000,/")
					fid += 1
		if mon.debug(): print()
		# size avg
		print(f"multigraph web_request_size_{hostid}.avg")
		print(f"graph_title {host} request size average")
		print('graph_args --base 1024 -l 0')
		print('graph_category web_size')
		print('graph_vlabel bytes per response')
		print('graph_scale yes')
		fid = 0
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					print(f"req_{pathid}_{methid}_{stid}.label {status} {method} {path}")
					print(f"req_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
					print(f"req_{pathid}_{methid}_{stid}.min 0")
					fid += 1
		if mon.debug(): print()

def report(sts):
	mon.dbg('report web_request')
	for host in sorted(sts.keys()):
		hostid = mon.cleanfn(host)
		# total index
		print(f"multigraph web_request_{hostid}")
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					value = sts[host][path][method][status]['count']
					print(f"req_{pathid}_{methid}_{stid}.value {value}")
		if mon.debug(): print()
		# total
		print(f"multigraph web_request_{hostid}.total")
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					value = sts[host][path][method][status]['count']
					print(f"req_{pathid}_{methid}_{stid}.value {value}")
		if mon.debug(): print()
		# total count
		print(f"multigraph web_request_{hostid}.count")
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					value = mon.derive(sts[host][path][method][status]['count'])
					print(f"req_{pathid}_{methid}_{stid}.value {value}")
		if mon.debug(): print()
		# time index
		print(f"multigraph web_request_time_{hostid}")
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					value = sts[host][path][method][status]['time']
					print(f"req_{pathid}_{methid}_{stid}.value {value}")
		if mon.debug(): print()
		# time total
		print(f"multigraph web_request_time_{hostid}.total")
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					value = sts[host][path][method][status]['time']
					print(f"req_{pathid}_{methid}_{stid}.value {value}")
		if mon.debug(): print()
		# time count
		print(f"multigraph web_request_time_{hostid}.count")
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					value = mon.derive(sts[host][path][method][status]['time'])
					print(f"req_{pathid}_{methid}_{stid}.value {value}")
		if mon.debug(): print()
		# time avg
		print(f"multigraph web_request_time_{hostid}.avg")
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					t = sts[host][path][method][status]['time']
					c = sts[host][path][method][status]['count']
					if c > 0:
						value = t / c
					else:
						value = t
					print(f"req_{pathid}_{methid}_{stid}.value {value}")
		if mon.debug(): print()
		# size index
		print(f"multigraph web_request_size_{hostid}")
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					value = sts[host][path][method][status]['size']
					print(f"req_{pathid}_{methid}_{stid}.value {value}")
		if mon.debug(): print()
		# size total
		print(f"multigraph web_request_size_{hostid}.total")
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					value = sts[host][path][method][status]['size']
					print(f"req_{pathid}_{methid}_{stid}.value {value}")
		if mon.debug(): print()
		# size count
		print(f"multigraph web_request_size_{hostid}.count")
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					value = mon.derive(sts[host][path][method][status]['size'])
					print(f"req_{pathid}_{methid}_{stid}.value {value}")
		if mon.debug(): print()
		# size avg
		print(f"multigraph web_request_size_{hostid}.avg")
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					s = sts[host][path][method][status]['size']
					c = sts[host][path][method][status]['count']
					if c > 0:
						value = s / c
					else:
						value = s
					print(f"req_{pathid}_{methid}_{stid}.value {value}")
		if mon.debug(): print()
