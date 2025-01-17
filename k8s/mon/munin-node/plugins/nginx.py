#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import os
import sys

# load lib

MONLIB = os.getenv('MONLIB', '/srv/munin/plugins')
sys.path.insert(0, MONLIB)

import mon_metrics as metrics

# load env

_nginx_metrics = 'http://metrics.ingress-nginx.svc.cluster.local:10254/metrics'
METRICS_URL = os.getenv('NGINX_METRICS_URL', _nginx_metrics)

# load modules

import nginx_conn
import nginx_proc
import nginx_cfg
import web_request
import web_response
import web_ingress
import web_sent
import web_latency
import web_ssl

if __name__ == '__main__': # pragma no cover
	mods = dict(
		nginx_conn = nginx_conn,
		nginx_proc = nginx_proc,
		nginx_cfg = nginx_cfg,
		web_request = web_request,
		web_response = web_response,
		web_ingress = web_ingress,
		web_sent = web_sent,
		web_latency = web_latency,
		web_ssl = web_ssl,
	)
	sys.exit(metrics.main(sys.argv[1:], METRICS_URL, mods))
