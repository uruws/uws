#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t
import mon_metrics

import k8s_etcd

_bup_print = k8s_etcd._print
_bup_sts = k8s_etcd.sts.copy()

_metrics_fn = '/go/src/k8s/mon/testdata/k8s_metrics.txt'
_endpoint = 'http://internal-eks-1847b-EtcdLoad-1W9LAUN8VTRY8-2061453668.us-east-2.elb.amazonaws.com:2379'
_sts = dict(
	etcd_db_total_size_in_bytes = 54943744.0,
	etcd_db_endpoint = _endpoint,
)

class Test(unittest.TestCase):
	metrics = None

	@classmethod
	def setUpClass(k):
		with open(_metrics_fn, 'rb') as fh:
			k.metrics = list(mon_metrics._metrics_parse(fh))

	def setUp(t):
		mon_t.setUp()
		k8s_etcd._print = MagicMock()
		k8s_etcd.sts = _bup_sts.copy()

	def tearDown(t):
		mon_t.tearDown()
		k8s_etcd._print = _bup_print

	def test_globals(t):
		t.assertDictEqual(k8s_etcd.sts, dict(
			etcd_db_total_size_in_bytes = 'U',
			etcd_db_endpoint = None,
		))

	def test_print(t):
		_bup_print('testing', '...')

	def test_parse(t):
		t.assertFalse(k8s_etcd.parse('testing', None, None))

	def test_parse_data(t):
		t.maxDiff = None
		for name, meta, value in t.metrics:
			if _bup_sts.get(name, None) is not None:
				t.assertTrue(k8s_etcd.parse(name, meta, value))
		t.assertDictEqual(k8s_etcd.sts, _sts)

	def test_config(t):
		k8s_etcd.config(_sts)
		config = [
			call('multigraph k8s_etcd'),
			call('graph_title k8stest k8s apiserver etcd'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category k8s'),
			call('graph_vlabel bytes'),
			call('graph_scale yes'),
			call('db_size.label db size'),
			call('db_size.colour COLOUR0'),
			call('db_size.min 0'),
			call('db_size.draw AREA'),
			call('db_size.info endpoint:', _endpoint),
		]
		k8s_etcd._print.assert_has_calls(config)
		t.assertEqual(k8s_etcd._print.call_count, len(config))

	def test_report(t):
		k8s_etcd.report(_sts)
		report = [
			call('multigraph k8s_etcd'),
			call('db_size.value', 54943744.0),
		]
		k8s_etcd._print.assert_has_calls(report)
		t.assertEqual(k8s_etcd._print.call_count, len(report))

if __name__ == '__main__':
	unittest.main()
