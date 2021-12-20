#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import nginx

class Test(unittest.TestCase):

	def test_globals(t):
		t.assertEqual(nginx.MONLIB, '/srv/munin/plugins')
		t.assertEqual(nginx._nginx_metrics,
			'http://metrics.ingress-nginx.svc.cluster.local:10254/metrics')
		t.assertEqual(nginx.METRICS_URL, nginx._nginx_metrics)

	def test_imports(t):
		t.assertEqual(nginx.nginx_conn.__name__, 'nginx_conn')
		t.assertEqual(nginx.nginx_proc.__name__, 'nginx_proc')
		t.assertEqual(nginx.nginx_cfg.__name__, 'nginx_cfg')
		t.assertEqual(nginx.web_request.__name__, 'web_request')
		t.assertEqual(nginx.web_response.__name__, 'web_response')
		t.assertEqual(nginx.web_ingress.__name__, 'web_ingress')
		t.assertEqual(nginx.web_sent.__name__, 'web_sent')
		t.assertEqual(nginx.web_latency.__name__, 'web_latency')
		t.assertEqual(nginx.web_ssl.__name__, 'web_ssl')

if __name__ == '__main__':
	unittest.main()
