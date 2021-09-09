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
import nginx_cfg
# ~ import web
import web_response
import web_bytes_sent
import web_latency
import web_request

if __name__ == '__main__':
	mods = dict(
		nginx_conn = nginx_conn,
		nginx_proc = nginx_proc,
		nginx_cfg = nginx_cfg,
		# ~ web = web,
		web_response = web_response,
		web_bytes_sent = web_bytes_sent,
		web_latency = web_latency,
		web_request = web_request,
	)
	sys.exit(mon.main(METRICS_URL, mods))
