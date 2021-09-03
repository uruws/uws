#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import os
import sys

# load lib
MONLIB = os.getenv('MONLIB', '/srv/munin/plugins')
sys.path.insert(0, MONLIB)

import mon

# load env
__nginx_metrics = 'http://metrics.ingress-nginx.svc.cluster.local:10254/metrics'
METRICS_URL = os.getenv('NGINX_METRICS_URL', __nginx_metrics)

# load modules
import nginx_conn
import nginx_proc

# module parse

def metrics():
	mon.dbg('parse')
	for name, meta, value in mon.metrics(METRICS_URL):
		if nginx_conn.parse(name, meta, value):
			continue
		elif nginx_proc.parse(name, meta, value):
			continue

	# register stats
	return dict(
		nginx_conn = nginx_conn.sts,
		nginx_proc = nginx_proc.sts,
	)

# module config

def config():
	mon.dbg('config')
	sts = metrics()

	nginx_conn.config()
	nginx_proc.config()

	mon.cacheSet(sts)
	return 0

# module report

def report():
	mon.dbg('report')
	sts = mon.cacheGet()
	if sts is None:
		sts = metrics()

	nginx_conn.report(sts['nginx_conn'])
	nginx_proc.report(sts['nginx_proc'])

	return 0

# main

def main():
	try:
		if sys.argv[1] == 'config':
			return config()
	except IndexError:
		pass
	return report()

if __name__ == '__main__':
	sys.exit(main())
