#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t
import mon_metrics

import k8s_auth

_bup_print = k8s_auth._print
_bup_sts = k8s_auth.sts.copy()

_metrics_fn = '/go/src/k8s/mon/testdata/k8s_metrics.txt'
_sts = dict(
	authenticated_user_requests = dict(
		other = 219272074.0,
	),
	authentication_attempts = dict(
		error = 6.0,
		success = 219272074.0,
	),
)

class Test(unittest.TestCase):
	metrics = None

	@classmethod
	def setUpClass(k):
		with open(_metrics_fn, 'rb') as fh:
			k.metrics = list(mon_metrics._metrics_parse(fh))

	def setUp(t):
		mon_t.setUp()
		k8s_auth._print = MagicMock()
		k8s_auth.sts = _bup_sts.copy()

	def tearDown(t):
		mon_t.tearDown()
		k8s_auth._print = _bup_print

	def test_globals(t):
		t.assertDictEqual(k8s_auth.sts, dict(
			authenticated_user_requests = dict(),
			authentication_attempts = dict(),
		))

	def test_print(t):
		_bup_print('testing', '...')

	def test_parse(t):
		t.assertFalse(k8s_auth.parse('testing', None, None))

	def test_parse_data(t):
		t.maxDiff = None
		for name, meta, value in t.metrics:
			if _bup_sts.get(name, None) is not None:
				t.assertTrue(k8s_auth.parse(name, meta, value))
		t.assertDictEqual(k8s_auth.sts, _sts)

	def test_config(t):
		k8s_auth.config(_sts)
		config = [
			# attempts
			call('multigraph k8s_auth_attempts'),
			call('graph_title k8stest k8s apiserver auth attempts'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category number'),
			call('graph_vlabel bytes'),
			call('graph_scale yes'),
			call('error.label error'),
			call('error.colour COLOUR0'),
			call('error.min 0'),
			call('error.type DERIVE'),
			call('error.cdef error,1000,/'),
			call('success.label success'),
			call('success.colour COLOUR1'),
			call('success.min 0'),
			call('success.type DERIVE'),
			call('success.cdef success,1000,/'),
			# requests
			call('multigraph k8s_auth_requests'),
			call('graph_title k8stest k8s apiserver auth requests'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category number'),
			call('graph_vlabel bytes'),
			call('graph_scale yes'),
			call('user_other.label other'),
			call('user_other.colour COLOUR0'),
			call('user_other.min 0'),
			call('user_other.type DERIVE'),
			call('user_other.cdef other,1000,/'),
		]
		k8s_auth._print.assert_has_calls(config)
		t.assertEqual(k8s_auth._print.call_count, len(config))

	def test_report(t):
		k8s_auth.report(_sts)
		report = [
			# attempts
			call('multigraph k8s_auth_attempts'),
			call('error.value', 6000),
			call('success.value', 219272074000),
			# requests
			call('multigraph k8s_auth_requests'),
			call('user_other.value', 219272074000),
		]
		k8s_auth._print.assert_has_calls(report)
		t.assertEqual(k8s_auth._print.call_count, len(report))

if __name__ == '__main__':
	unittest.main()
