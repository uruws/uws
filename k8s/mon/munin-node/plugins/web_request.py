# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

import req_total
import req_by_path
import req_errors
import req_time
import req_size

sts = dict()

def __parse(name, meta, value):
	global sts
	host = meta.get('host', '_')
	if host == '_':
		host = 'default'
	if not sts.get(host, None):
		sts[host] = dict(
			all = dict(),
			by_path = dict(),
			errors = dict(),
		)
	# all
	path = meta.get('path', '')
	if path == '':
		path = 'default'
	if not sts[host]['all'].get(path, None):
		sts[host]['all'][path] = dict()
	method = meta.get('method', '')
	if method == '':
		method = 'default'
	if not sts[host]['all'][path].get(method, None):
		sts[host]['all'][path][method] = dict()
	status = meta.get('status', '')
	if status == '':
		status = 'unknown'
	if not sts[host]['all'][path][method].get(status, None):
		sts[host]['all'][path][method][status] = dict(
			count = 0, size = 0, time = 0)
	mon.dbg('parse web_request:', name, host, path, method, status)
	sts[host]['all'][path][method][status][name] += value
	# count
	if name == 'count':
		# by_path
		if not sts[host]['by_path'].get(path, None):
			sts[host]['by_path'][path] = 0
		sts[host]['by_path'][path] += value
		# errors
		try:
			st = int(status)
		except ValueError as err:
			mon.log('ERROR:', err)
			return False
		if st >= 400 or st < 100:
			if not sts[host]['errors'].get(path, None):
				sts[host]['errors'][path] = dict()
			if not sts[host]['errors'][path].get(status, None):
				sts[host]['errors'][path][status] = 0
			sts[host]['errors'][path][status] += value
	return True

TIME  = 'nginx_ingress_controller_request_duration_seconds_sum'
COUNT = 'nginx_ingress_controller_request_duration_seconds_count'
SIZE  = 'nginx_ingress_controller_request_size_sum'

def parse(name, meta, value):
	if name == TIME:
		return __parse('time', meta, value)
	elif name == COUNT:
		return __parse('count', meta, value)
	elif name == SIZE:
		return __parse('size', meta, value)
	return False

def config(sts):
	mon.dbg('config web_request')
	cluster = mon.cluster()
	for host in sorted(sts.keys()):
		hostid = mon.cleanfn(host)
		# total
		req_total.config(cluster, host, hostid, sts[host].get('all', {}))
		# by_path
		req_by_path.config(cluster, host, hostid, sts[host].get('by_path', {}))
		# errors
		req_errors.config(cluster, host, hostid, sts[host].get('errors', {}))
		# time
		req_time.config(cluster, host, hostid, sts[host].get('all', {}))
		# size
		req_size.config(cluster, host, hostid, sts[host].get('all', {}))

def report(sts):
	mon.dbg('report web_request')
	for host in sorted(sts.keys()):
		hostid = mon.cleanfn(host)
		# total
		req_total.report(hostid, sts[host].get('all', {}))
		# by_path
		req_by_path.report(hostid, sts[host].get('by_path', {}))
		# errors
		req_errors.report(hostid, sts[host].get('errors', {}), sts[host].get('all', {}))
		# time
		req_time.report(hostid, sts[host].get('all', {}))
		# size
		req_size.report(hostid, sts[host].get('all', {}))
