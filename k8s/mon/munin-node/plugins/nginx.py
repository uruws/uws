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
# ~ import nginx_proc

# module parse

def metrics():
	mon.dbg('parse')
	for name, meta, value in mon.metrics(METRICS_URL):
		# connections
		if name == 'nginx_ingress_controller_nginx_process_connections':
			nginx_conn.parse(meta, value)
		# connections total
		elif name == 'nginx_ingress_controller_nginx_process_connections_total':
			nginx_conn.parse(meta, value)
	# register stats
	return dict(
		nginx_conn = nginx_conn.sts,
	)

# module config

def config():
	mon.dbg('config')
	sts = metrics()

	# connections
	nginx_conn.config()

	mon.cacheSet(sts)
	return 0

# module report

def report():
	mon.dbg('report')
	sts = mon.cacheGet()
	if sts is None:
		sts = metrics()

	# connections
	nginx_conn.report(sts['nginx_conn'])

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
