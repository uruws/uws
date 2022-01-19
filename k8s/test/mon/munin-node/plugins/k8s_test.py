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

	def test_imports(t):
		t.assertListEqual([i for i in dir(k8s) if not i.startswith('_')], [
			'METRICS_URL',
			'MONLIB',
			'k8s_cpu',
			'k8s_mem',
			'metrics',
			'os',
			'sys',
		])

if __name__ == '__main__':
	unittest.main()
