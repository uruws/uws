# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from typing import Any

import mon

import resp_total
import resp_time
import resp_size

sts: dict[str, Any] = dict()

def __parse(name: str, meta: dict[str, str], value: float) -> bool:
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

TIME  = 'nginx_ingress_controller_response_duration_seconds_sum'
COUNT = 'nginx_ingress_controller_response_duration_seconds_count'
SIZE  = 'nginx_ingress_controller_response_size_sum'

def parse(name: str, meta: dict[str, str], value: float) -> bool:
	if name == TIME:
		return __parse('time', meta, value)
	elif name == COUNT:
		return __parse('count', meta, value)
	elif name == SIZE:
		return __parse('size', meta, value)
	return False

def config(sts: dict[str, Any]):
	mon.dbg('config web_response')
	cluster = mon.cluster()
	for host in sorted(sts.keys()):
		hostid = mon.cleanfn(host)
		# total
		resp_total.config(cluster, host, hostid, sts[host])
		# time
		resp_time.config(cluster, host, hostid, sts[host])
		# size
		resp_size.config(cluster, host, hostid, sts[host])

def report(sts: dict[str, Any]):
	mon.dbg('report web_response')
	for host in sorted(sts.keys()):
		hostid = mon.cleanfn(host)
		# total
		resp_total.report(hostid, sts[host])
		# time
		resp_time.report(hostid, sts[host])
		# size
		resp_size.report(hostid, sts[host])
