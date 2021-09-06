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
import web_bytes_sent

if __name__ == '__main__':
	__mod = dict(
		nginx_conn = nginx_conn,
		nginx_proc = nginx_proc,
		nginx_cfg = nginx_cfg,
		web_bytes_sent = web_bytes_sent,
	)
	sys.exit(mon.main(METRICS_URL, __mod))
