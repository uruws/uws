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

if __name__ == '__main__':
	unittest.main()
