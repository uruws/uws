#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t
import mon_metrics

import k8s_service

_bup_print = k8s_service._print
_bup_sts = k8s_service.sts.copy()

_metrics_fn = '/go/src/k8s/mon/testdata/k8s_metrics.txt'
_sts = dict(
	aggregator_unavailable_apiservice_total = {
		'MissingEndpoints': {'v1beta1.metrics.k8s.io': 15.0},
	},
)

class Test(unittest.TestCase):
	metrics = None

	@classmethod
	def setUpClass(k):
		with open(_metrics_fn, 'rb') as fh:
			k.metrics = list(mon_metrics._metrics_parse(fh))

	def setUp(t):
		mon_t.setUp()
		k8s_service._print = MagicMock()
		k8s_service.sts = _bup_sts.copy()

	def tearDown(t):
		mon_t.tearDown()
		k8s_service._print = _bup_print

	def test_globals(t):
		t.assertDictEqual(k8s_service.sts, dict(
			aggregator_unavailable_apiservice_total = dict(),
		))

	def test_print(t):
		_bup_print('testing', '...')

	def test_parse(t):
		t.assertFalse(k8s_service.parse('testing', None, None))

	def test_parse_data(t):
		t.maxDiff = None
		for name, meta, value in t.metrics:
			if _bup_sts.get(name, None) is not None:
				t.assertTrue(k8s_service.parse(name, meta, value))
		t.assertDictEqual(k8s_service.sts, _sts)

if __name__ == '__main__':
	unittest.main()
