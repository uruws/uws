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
	process_resident_memory_bytes   = 'U',
	process_virtual_memory_bytes    = 'U',
	go_memstats_alloc_bytes         = 'U',
	go_memstats_buck_hash_sys_bytes = 'U',
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

if __name__ == '__main__':
	unittest.main()
