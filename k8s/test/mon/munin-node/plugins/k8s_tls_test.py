#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t
import mon_metrics

import k8s_tls

_bup_print = k8s_tls._print
_bup_sts = k8s_tls.sts.copy()

_metrics_fn = '/go/src/k8s/mon/testdata/k8s_metrics.txt'
_sts = dict(
	apiserver_tls_handshake_errors_total = 17328.0,
)

class Test(unittest.TestCase):
	metrics = None

	@classmethod
	def setUpClass(k):
		with open(_metrics_fn, 'rb') as fh:
			k.metrics = list(mon_metrics._metrics_parse(fh))

	def setUp(t):
		mon_t.setUp()
		k8s_tls._print = MagicMock()
		k8s_tls.sts = _bup_sts.copy()

	def tearDown(t):
		mon_t.tearDown()
		k8s_tls._print = _bup_print

	def test_globals(t):
		t.assertDictEqual(k8s_tls.sts, dict(
			apiserver_tls_handshake_errors_total = 'U',
		))

	def test_print(t):
		_bup_print('testing', '...')

	def test_parse(t):
		t.assertFalse(k8s_tls.parse('testing', None, None))

	def test_parse_data(t):
		t.maxDiff = None
		for name, meta, value in t.metrics:
			if _bup_sts.get(name, None) is not None:
				t.assertTrue(k8s_tls.parse(name, meta, value))
		t.assertDictEqual(k8s_tls.sts, _sts)

	def test_config(t):
		k8s_tls.config(_sts)
		config = [
			call('multigraph k8s_tls'),
			call('graph_title k8stest k8s apiserver TLS'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category k8s'),
			call('graph_vlabel number'),
			call('graph_scale yes'),
			call('errors.label errors'),
			call('errors.colour ff0000'),
			call('errors.draw AREA'),
			call('errors.min 0'),
			call('errors.type DERIVE'),
			call('errors.cdef errors,1000,/'),
		]
		k8s_tls._print.assert_has_calls(config)
		t.assertEqual(k8s_tls._print.call_count, len(config))

	def test_report(t):
		k8s_tls.report(_sts)
		report = [
			call('multigraph k8s_tls'),
			call('errors.value', 17328.0),
		]
		k8s_tls._print.assert_has_calls(report)
		t.assertEqual(k8s_tls._print.call_count, len(report))

if __name__ == '__main__':
	unittest.main()
