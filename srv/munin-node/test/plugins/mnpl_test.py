#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from pathlib      import Path
from urllib.error import HTTPError

import unittest
from unittest.mock import MagicMock
from unittest.mock import call

from contextlib import contextmanager

import mnpl_t
import mnpl_utils
import mnpl

@contextmanager
def mock_main():
	_bup_config = mnpl.config
	_bup_report = mnpl.report
	try:
		mnpl.config = MagicMock(return_value = 0)
		mnpl.report = MagicMock(return_value = 0)
		yield
	finally:
		mnpl.config = _bup_config
		mnpl.report = _bup_report

@contextmanager
def mock_report_host(fail = False):
	def _fail(*args, **kwargs):
		raise Exception('mock_report_error')
	_bup_report = mnpl._report
	try:
		if fail:
			mnpl._report = MagicMock(side_effect = _fail)
		else:
			mnpl._report = MagicMock(return_value = (0.0, 1.0))
		yield
	finally:
		mnpl._report = _bup_report

class Test(unittest.TestCase):

	def setUp(t):
		mnpl_t.setup()

	def tearDown(t):
		mnpl_t.teardown()

	def test_clusters(t):
		t.assertEqual(mnpl._clusters_fn, Path('/uws/etc/cluster.json'))
		t.assertListEqual(mnpl.clusters(), [
			{'host': 'k8stest', 'name': 'k8stest'},
		])

	def test_tls_getpw(t):
		t.assertEqual(mnpl_utils._tls_getpw(), 'pwd')
		mnpl_utils._tls_cert = 'test-id'
		t.assertEqual(mnpl_utils._tls_getpw(), '')

	def test_tls_context_auth(t):
		mnpl_utils._tls_cert = mnpl_t.bup_tls_cert
		mnpl_utils._tls_conf = mnpl_t.bup_tls_conf
		ctx = mnpl_utils._tls_context(True)
		t.assertIs(mnpl_utils._ctx_auth, ctx)

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
			call('a_latency.warning', 13),
			call('a_latency.critical', 15),
			call('a_latency.info', 'https://k8stest.uws.talkingpts.org/'),
			call('b_status.label status:', 200),
			call('b_status.colour COLOUR1'),
			call('b_status.draw LINE'),
			call('b_status.min 0'),
			call('b_status.max 1'),
			call('b_status.critical 1:'),
		]
		mnpl_utils.println.assert_has_calls(calls)
		t.assertEqual(mnpl_utils.println.call_count, len(calls))

	def test_config_no_auth(t):
		cfg = mnpl.Config(
			auth = False,
		)
		t.assertEqual(mnpl.config(cfg), 0)
		calls = [
			call('graph_title k8s k8stest / (no auth)'),
		]
		mnpl_utils.println.assert_has_calls(calls)

	def test_config_title(t):
		cfg = mnpl.Config(
			title = 'testing title',
		)
		t.assertEqual(mnpl.config(cfg), 0)
		calls = [
			call('graph_title k8s k8stest testing title'),
		]
		mnpl_utils.println.assert_has_calls(calls)

	def test_config_category(t):
		cfg = mnpl.Config(
			category = 'testing category',
		)
		t.assertEqual(mnpl.config(cfg), 0)
		calls = [
			call('graph_category', 'testing category'),
		]
		mnpl_utils.println.assert_has_calls(calls)

	def test_report(t):
		resp = MagicMock()
		resp.getcode = MagicMock(return_value = 200)
		mnpl_utils.urlopen.return_value = resp
		mnpl_utils._ctx_auth = MagicMock()
		cfg = mnpl.Config()
		t.assertEqual(mnpl.report(cfg), 0)
		calls = [
			call('multigraph k8s_k8stest___200'),
			call('a_latency.value', '0.0'),
			call('b_status.value', '1.0'),
		]
		mnpl_utils.println.assert_has_calls(calls)
		t.assertEqual(mnpl_utils.println.call_count, len(calls))

	def test_report_no_auth(t):
		mnpl_utils.urlopen.return_value = MagicMock()
		mnpl_utils._ctx_auth = MagicMock()
		cfg = mnpl.Config(auth = False)
		t.assertEqual(mnpl.report(cfg), 0)
		calls = [
			call('multigraph k8s_k8stest___200_no_auth'),
			call('a_latency.value', '0.0'),
			call('b_status.value', '0.0'),
		]
		mnpl_utils.println.assert_has_calls(calls)

	def test_report_error(t):
		def _error(*args, **kwargs):
			raise HTTPError('testing', 404, 'mock_error', {}, None)
		mnpl_utils.urlopen.side_effect = _error
		cfg = mnpl.Config(auth = False, status = 404)
		t.assertEqual(mnpl._report('k8stest', cfg), (1.0, 0.0))

	def test_report_host(t):
		with mock_report_host():
			mnpl.report_host(mnpl.HostConfig(
				name = 'test',
				host = 'htest',
			), mnpl.Config())
			calls = [
				call('a_latency.value', '1.0'),
				call('b_status.value', '0.0'),
			]
			mnpl_utils.println.assert_has_calls(calls)

	def test_report_host_error(t):
		with mock_report_host(fail = True):
			mnpl.report_host(mnpl.HostConfig(
				name = 'test',
				host = 'htest',
			), mnpl.Config())
			calls = [
				call('a_latency.value', 'U'),
				call('b_status.value', 'U'),
			]
			mnpl_utils.println.assert_has_calls(calls)

	def test_main_config(t):
		with mock_main():
			t.assertEqual(mnpl.main(['config'], None), 0)
			mnpl.config.assert_called_once_with(None)
			mnpl.report.assert_not_called()

	def test_main_report(t):
		with mock_main():
			t.assertEqual(mnpl.main([], None), 0)
			mnpl.report.assert_called_once_with(None)
			mnpl.config.assert_not_called()

if __name__ == '__main__':
	unittest.main()
