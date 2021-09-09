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
	mon.dbg('parse web_response:', name, host, path, method, status)
	sts[host][path][method][status][name] += value
	return True

def parse(name, meta, value):
	if name == 'nginx_ingress_controller_response_duration_seconds_sum':
		return __parse('time', meta, value)
	elif name == 'nginx_ingress_controller_response_duration_seconds_count':
		return __parse('count', meta, value)
	elif name == 'nginx_ingress_controller_response_size_sum':
		return __parse('size', meta, value)
	return False

def config(sts):
	mon.dbg('config web_response')
	for host in sorted(sts.keys()):
		hostid = mon.cleanfn(host)
		# total index
		print(f"multigraph web_response_{hostid}")
		print(f"graph_title {host} response total")
		print('graph_args --base 1000 -l 0')
		print('graph_category web_resp')
		print('graph_vlabel number')
		print('graph_scale yes')
		print('graph_total total')
		fid = 0
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					print(f"resp_{pathid}_{methid}_{stid}.label {method} {path} - {status}")
					print(f"resp_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
					print(f"resp_{pathid}_{methid}_{stid}.draw AREASTACK")
					print(f"resp_{pathid}_{methid}_{stid}.min 0")
					fid += 1
		if mon.debug(): print()
		# total
		print(f"multigraph web_response_{hostid}.total")
		print(f"graph_title {host} response total")
		print('graph_args --base 1000 -l 0')
		print('graph_category web_resp')
		print('graph_vlabel number')
		print('graph_scale yes')
		print('graph_total total')
		fid = 0
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					print(f"resp_{pathid}_{methid}_{stid}.label {method} {path} - {status}")
					print(f"resp_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
					print(f"resp_{pathid}_{methid}_{stid}.draw AREASTACK")
					print(f"resp_{pathid}_{methid}_{stid}.min 0")
					fid += 1
		if mon.debug(): print()
		# total count
		print(f"multigraph web_response_{hostid}.count")
		print(f"graph_title {host} response")
		print('graph_args --base 1000 -l 0')
		print('graph_category web_resp')
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
					print(f"resp_{pathid}_{methid}_{stid}.label {method} {path} - {status}")
					print(f"resp_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
					print(f"resp_{pathid}_{methid}_{stid}.draw AREASTACK")
					print(f"resp_{pathid}_{methid}_{stid}.type DERIVE")
					print(f"resp_{pathid}_{methid}_{stid}.min 0")
					fid += 1
		if mon.debug(): print()
		# time index
		print(f"multigraph web_response_time_{hostid}")
		print(f"graph_title {host} response time total")
		print('graph_args --base 1000 -l 0')
		print('graph_category web_resp')
		print('graph_vlabel seconds')
		print('graph_scale yes')
		print('graph_total total')
		fid = 0
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					print(f"resp_{pathid}_{methid}_{stid}.label {method} {path} - {status}")
					print(f"resp_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
					print(f"resp_{pathid}_{methid}_{stid}.draw AREASTACK")
					print(f"resp_{pathid}_{methid}_{stid}.min 0")
					fid += 1
		if mon.debug(): print()
		# time total
		print(f"multigraph web_response_time_{hostid}.total")
		print(f"graph_title {host} response time total")
		print('graph_args --base 1000 -l 0')
		print('graph_category web_resp')
		print('graph_vlabel seconds')
		print('graph_scale yes')
		print('graph_total total')
		fid = 0
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					print(f"resp_{pathid}_{methid}_{stid}.label {method} {path} - {status}")
					print(f"resp_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
					print(f"resp_{pathid}_{methid}_{stid}.draw AREASTACK")
					print(f"resp_{pathid}_{methid}_{stid}.min 0")
					fid += 1
		if mon.debug(): print()
		# time count
		print(f"multigraph web_response_time_{hostid}.count")
		print(f"graph_title {host} response time")
		print('graph_args --base 1000 -l 0')
		print('graph_category web_resp')
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
					print(f"resp_{pathid}_{methid}_{stid}.label {method} {path} - {status}")
					print(f"resp_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
					print(f"resp_{pathid}_{methid}_{stid}.draw AREASTACK")
					print(f"resp_{pathid}_{methid}_{stid}.type DERIVE")
					print(f"resp_{pathid}_{methid}_{stid}.min 0")
					fid += 1
		if mon.debug(): print()
		# time avg
		print(f"multigraph web_response_time_{hostid}.avg")
		print(f"graph_title {host} response time average")
		print('graph_args --base 1000 -l 0')
		print('graph_category web_resp')
		print('graph_vlabel seconds')
		print('graph_scale yes')
		fid = 0
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					print(f"resp_{pathid}_{methid}_{stid}.label {method} {path} - {status}")
					print(f"resp_{pathid}_{methid}_{stid}.colour COLOUR{fid}")
					print(f"resp_{pathid}_{methid}_{stid}.min 0")
					fid += 1
		if mon.debug(): print()

def report(sts):
	mon.dbg('report web_response')
	for host in sorted(sts.keys()):
		hostid = mon.cleanfn(host)
		# total index
		print(f"multigraph web_response_{hostid}")
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					value = sts[host][path][method][status]['count']
					print(f"resp_{pathid}_{methid}_{stid}.value {value}")
		if mon.debug(): print()
		# total
		print(f"multigraph web_response_{hostid}.total")
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					value = sts[host][path][method][status]['count']
					print(f"resp_{pathid}_{methid}_{stid}.value {value}")
		if mon.debug(): print()
		# total count
		print(f"multigraph web_response_{hostid}.count")
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					value = sts[host][path][method][status]['count']
					print(f"resp_{pathid}_{methid}_{stid}.value {value}")
		if mon.debug(): print()
		# time index
		print(f"multigraph web_response_time_{hostid}")
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					value = sts[host][path][method][status]['time']
					print(f"resp_{pathid}_{methid}_{stid}.value {value}")
		if mon.debug(): print()
		# time total
		print(f"multigraph web_response_time_{hostid}.total")
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					value = sts[host][path][method][status]['time']
					print(f"resp_{pathid}_{methid}_{stid}.value {value}")
		if mon.debug(): print()
		# time count
		print(f"multigraph web_response_time_{hostid}.count")
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					value = sts[host][path][method][status]['time']
					print(f"resp_{pathid}_{methid}_{stid}.value {value}")
		if mon.debug(): print()
		# time avg
		print(f"multigraph web_response_time_{hostid}.avg")
		for path in sorted(sts[host].keys()):
			pathid = mon.cleanfn(path)
			for method in sorted(sts[host][path].keys()):
				methid = mon.cleanfn(method)
				for status in sorted(sts[host][path][method].keys()):
					stid = mon.cleanfn(status)
					t = sts[host][path][method][status]['time']
					c = sts[host][path][method][status]['count']
					value = t / c
					print(f"resp_{pathid}_{methid}_{stid}.value {value}")
		if mon.debug(): print()
