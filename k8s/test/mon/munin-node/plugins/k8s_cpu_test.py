#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t
import mon_metrics

import k8s_cpu

_bup_print = k8s_cpu._print
_bup_sts = k8s_cpu.sts.copy()

_metrics_fn = '/go/src/k8s/mon/testdata/k8s_metrics.txt'
_sts = dict(
	go_info                    = 'go1.15.14',
	go_goroutines              = 3999.0,
	go_threads                 = 16.0,
	process_cpu_seconds_total  = 708413.19,
	process_start_time_seconds = 10147255.50999999,
	process_start_time_hours   = 2818.6820861111087,
)

class Test(unittest.TestCase):
	metrics = None

	@classmethod
	def setUpClass(k):
		with open(_metrics_fn, 'rb') as fh:
			k.metrics = list(mon_metrics._metrics_parse(fh))
		k8s_cpu.time = MagicMock(return_value = 1641005999)

	def setUp(t):
		mon_t.setUp()
		k8s_cpu._print = MagicMock()
		k8s_cpu.sts = _bup_sts.copy()

	def tearDown(t):
		mon_t.tearDown()
		k8s_cpu._print = _bup_print

	def test_globals(t):
		t.assertDictEqual(k8s_cpu.sts, dict(
			go_info                    = 'go_version',
			go_goroutines              = 'U',
			go_threads                 = 'U',
			process_cpu_seconds_total  = 'U',
			process_start_time_seconds = 'U',
			process_start_time_hours   = 'U',
		))

	def test_print(t):
		_bup_print('testing', '...')

	def test_parse(t):
		t.assertFalse(k8s_cpu.parse('testing', None, None))

	def test_parse_data(t):
		for name, meta, value in t.metrics:
			if _bup_sts.get(name, None) is not None:
				t.assertTrue(k8s_cpu.parse(name, meta, value))
		t.assertDictEqual(k8s_cpu.sts, _sts)

	def test_config(t):
		k8s_cpu.config(_sts)
		config = [
			# cpu
			call('multigraph k8s_cpu'),
			call('graph_title Kubernetes apiserver'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category k8s'),
			call('graph_vlabel number'),
			call('graph_scale yes'),
			call('f0_goroutines.label', 'go1.15.14'),
			call('f0_goroutines.colour COLOUR0'),
			call('f0_goroutines.min 0'),
			call('f1_threads.label threads'),
			call('f1_threads.colour COLOUR1'),
			call('f1_threads.min 0'),
			# cpu usage
			call('multigraph k8s_cpu_usage'),
			call('graph_title Kubernetes apiserver CPU'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category k8s'),
			call('graph_vlabel seconds'),
			call('graph_scale yes'),
			call('usage.label usage'),
			call('usage.colour COLOUR0'),
			call('usage.min 0'),
			call('usage.type DERIVE'),
			call('usage.cdef usage,1000,/'),
			# uptime
			call('multigraph k8s_cpu_uptime'),
			call('graph_title Kubernetes apiserver uptime'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category k8s'),
			call('graph_vlabel hours'),
			call('graph_scale yes'),
			call('uptime.label uptime'),
			call('uptime.colour COLOUR0'),
			call('uptime.min 0'),
		]
		k8s_cpu._print.assert_has_calls(config)
		t.assertEqual(k8s_cpu._print.call_count, len(config))

	def test_report(t):
		k8s_cpu.report(_sts)
		report = [
			# cpu
			call('multigraph k8s_cpu'),
			call('f0_goroutines.value', 3999.0),
			call('f1_threads.label', 16.0),
			# cpu usage
			call('multigraph k8s_cpu_usage'),
			call('usage.value', 708413190),
			# uptime
			call('multigraph k8s_cpu_uptime'),
			call('uptime.value', 2818.6820861111087),
		]
		k8s_cpu._print.assert_has_calls(report)
		t.assertEqual(k8s_cpu._print.call_count, len(report))

if __name__ == '__main__':
	unittest.main()
