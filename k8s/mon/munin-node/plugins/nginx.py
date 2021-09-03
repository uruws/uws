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
# ~ import nginx_cfg

__mod = dict(
	nginx_conn = nginx_conn,
	nginx_proc = nginx_proc,
)

# module parse

def metrics():
	mon.dbg('parse')
	sts = dict()
	for name, meta, value in mon.metrics(METRICS_URL):
		for modname in __mod.keys():
			mod = __mod.get(modname)
			if mod.parse(name, meta, value):
				mon.dbg('mod parse:', modname)
				sts[modname] = mod.sts.copy()
				continue
	return sts

# module config

def config():
	mon.dbg('config')
	sts = metrics()
	for modname in __mod.keys():
		mod = __mod.get(modname)
		mon.dbg('mod config:', modname)
		mod.config(sts)
	mon.cacheSet(sts)
	return 0

# module report

def report():
	mon.dbg('report')
	sts = mon.cacheGet()
	if sts is None:
		sts = metrics()
	for modname in __mod.keys():
		mod = __mod.get(modname)
		mon.dbg('mod report:', modname)
		mod.report(sts[modname])
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
