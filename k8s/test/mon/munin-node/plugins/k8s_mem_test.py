#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t
import mon_metrics

import k8s_mem

_bup_print = k8s_mem._print
_bup_sts = k8s_mem.sts.copy()

_metrics_fn = '/go/src/k8s/mon/testdata/k8s_metrics.txt'
_sts = dict(
	process_resident_memory_bytes   = 998387712.0,
	process_virtual_memory_bytes    = 1782562816.0,
	go_memstats_alloc_bytes         = 532044520.0,
	go_memstats_buck_hash_sys_bytes = 28589700.0,
)

class Test(unittest.TestCase):
	metrics = None

	@classmethod
	def setUpClass(k):
		with open(_metrics_fn, 'rb') as fh:
			k.metrics = list(mon_metrics._metrics_parse(fh))
		k8s_mem.time = MagicMock(return_value = 1641005999)

	def setUp(t):
		mon_t.setUp()
		k8s_mem._print = MagicMock()
		k8s_mem.sts = _bup_sts.copy()

	def tearDown(t):
		mon_t.tearDown()
		k8s_mem._print = _bup_print

	def test_globals(t):
		t.assertDictEqual(k8s_mem.sts, dict(
			process_resident_memory_bytes   = 'U',
			process_virtual_memory_bytes    = 'U',
			go_memstats_alloc_bytes         = 'U',
			go_memstats_buck_hash_sys_bytes = 'U',
		))

	def test_print(t):
		_bup_print('testing', '...')

	def test_parse(t):
		t.assertFalse(k8s_mem.parse('testing', None, None))

	def test_parse_data(t):
		t.maxDiff = None
		for name, meta, value in t.metrics:
			if _bup_sts.get(name, None) is not None:
				t.assertTrue(k8s_mem.parse(name, meta, value))
		t.assertDictEqual(k8s_mem.sts, _sts)

if __name__ == '__main__':
	unittest.main()
