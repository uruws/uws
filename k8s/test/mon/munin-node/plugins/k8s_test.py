#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import k8s

class Test(unittest.TestCase):

	def test_globals(t):
		t.assertEqual(k8s.MONLIB, '/srv/munin/plugins')
		t.assertEqual(k8s._k8s_metrics,
			'http://k8s.mon.svc.cluster.local:2800/kube/k8s_metrics')
		t.assertEqual(k8s.METRICS_URL, k8s._k8s_metrics)

	# ~ def test_imports(t):
		# ~ t.assertEqual(k8s.k8s_metrics.__name__, 'k8s_metrics')

if __name__ == '__main__':
	unittest.main()
