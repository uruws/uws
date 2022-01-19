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

	def test_config(t):
		k8s_mem.config(_sts)
		config = [
			# mem
			call('multigraph k8s_mem'),
			call('graph_title Kubernetes apiserver memory'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category k8s'),
			call('graph_vlabel bytes'),
			call('graph_scale yes'),
			call('f0_resident.label resident'),
			call('f0_resident.colour COLOUR0'),
			call('f0_resident.min 0'),
			call('f1_virtual.label virtual'),
			call('f1_virtual.colour COLOUR1'),
			call('f1_virtual.min 0'),
			call('f2_allocated.label allocated'),
			call('f2_allocated.colour COLOUR2'),
			call('f2_allocated.min 0'),
			call('f3_profiling.label profiling'),
			call('f3_profiling.colour COLOUR3'),
			call('f3_profiling.min 0'),
		]
		k8s_mem._print.assert_has_calls(config)
		t.assertEqual(k8s_mem._print.call_count, len(config))

	def test_report(t):
		k8s_mem.report(_sts)
		report = [
			# mem
			call('multigraph k8s_mem'),
			call('f0_resident.value', 998387712.0),
			call('f1_virtual.value', 1782562816.0),
			call('f2_allocated.value', 532044520.0),
			call('f3_profiling.value', 28589700.0),
		]
		k8s_mem._print.assert_has_calls(report)
		t.assertEqual(k8s_mem._print.call_count, len(report))

if __name__ == '__main__':
	unittest.main()
