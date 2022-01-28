#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from pathlib import Path

import unittest
from unittest.mock import MagicMock
from unittest.mock import call

import mnpl_t
import mnpl

class Test(unittest.TestCase):

	def setUp(t):
		mnpl_t.setup()

	def tearDown(t):
		mnpl_t.teardown()

	def test_log_disabled(t):
		t.assertFalse(mnpl._log)
		mnpl.log('testing', '...')
		t.assertEqual(mnpl_t.log_string(), '')

	def test_log_enabled(t):
		mnpl._log = True
		mnpl.log('testing', '...')
		t.assertEqual(mnpl_t.log_string(), 'testing ...')

	def test_error_log(t):
		mnpl.error('testing', '...')
		t.assertEqual(mnpl_t.log_string(), '[E] testing ...')

	def test_cleanfn(t):
		t.assertEqual(mnpl.cleanfn('k8s-test'), 'k8s_test')

	def test_print(t):
		mnpl_t.bup_print('testing', '...')

	def test_clusters(t):
		t.assertEqual(mnpl._clusters_fn, Path('/uws/etc/cluster.json'))
		t.assertListEqual(mnpl.clusters(), [
			{'host': 'k8stest', 'name': 'k8stest'},
		])

	def test_getpw(t):
		t.assertEqual(mnpl._getpw(), 'pwd')
		mnpl._tls_cert = 'test-id'
		t.assertEqual(mnpl._getpw(), '')

	def test_tls_context_auth(t):
		mnpl._tls_cert = mnpl_t.bup_tls_cert
		mnpl._tls_conf = mnpl_t.bup_tls_conf
		ctx = mnpl._context(True)
		t.assertIs(mnpl._ctx_auth, ctx)

	def test_GET(t):
		t.assertIsNone(mnpl.GET('k8stest', mnpl.Config(auth = False)))

	def test_config(t):
		cfg = mnpl.Config()
		t.assertEqual(mnpl.config(cfg), 0)
		calls = [
			call('multigraph k8s_k8stest___200'),
			call('graph_title k8s k8stest /'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category', 'k8stest'),
			call('graph_vlabel', 'number'),
			call('graph_scale yes'),
			call('a_latency.label latency seconds'),
			call('a_latency.colour COLOUR0'),
			call('a_latency.draw AREA'),
			call('a_latency.min 0'),
			call('a_latency.warning', 3),
			call('a_latency.critical', 5),
			call('a_latency.info', 'https://k8stest.uws.talkingpts.org/'),
			call('b_status.label status:', 200),
			call('b_status.colour COLOUR1'),
			call('b_status.draw LINE'),
			call('b_status.min 0'),
			call('b_status.max 1'),
			call('b_status.critical 1:'),
		]
		mnpl._print.assert_has_calls(calls)
		t.assertEqual(mnpl._print.call_count, len(calls))

	def test_config_no_auth(t):
		cfg = mnpl.Config(auth = False)
		t.assertEqual(mnpl.config(cfg), 0)
		calls = [
			call('graph_title k8s k8stest / (no auth)'),
		]
		mnpl._print.assert_has_calls(calls)

	def test_report(t):
		mnpl._ctx_auth = MagicMock()
		cfg = mnpl.Config()
		t.assertEqual(mnpl.report(cfg), 0)
		calls = [
			call('multigraph k8s_k8stest___200'),
			call('a_latency.value', 0.0),
			call('b_status.value', 0.0),
		]
		mnpl._print.assert_has_calls(calls)
		t.assertEqual(mnpl._print.call_count, len(calls))

	def test_report_no_auth(t):
		mnpl._ctx_auth = MagicMock()
		cfg = mnpl.Config(auth = False)
		t.assertEqual(mnpl.report(cfg), 0)
		calls = [
			call('multigraph k8s_k8stest___200_no_auth'),
		]
		mnpl._print.assert_has_calls(calls)

if __name__ == '__main__':
	unittest.main()
