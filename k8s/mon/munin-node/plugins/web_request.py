# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from time import time

import mon
import req_total
import req_time
import req_size

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
		# total
		req_total.config(host, hostid, sts[host])
		# time
		req_time.config(host, hostid, sts[host])
		# size
		req_size.config(host, hostid, sts[host])

def report(sts):
	mon.dbg('report web_request')
	for host in sorted(sts.keys()):
		hostid = mon.cleanfn(host)
		# total
		req_total.report(hostid, sts[host])
		# time
		req_time.report(hostid, sts[host])
		# size
		req_size.report(hostid, sts[host])
