#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t

import nodes_top

_bup_print = nodes_top._print

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		nodes_top._print = MagicMock()

	def tearDown(t):
		mon_t.tearDown()
		nodes_top._print = _bup_print

	def test_print(t):
		_bup_print('testing')

	def test_parse(t):
		t.assertDictEqual(nodes_top.parse({}), {
			'count': 0,
			'cpu': 0,
			'cpup': 0,
			'mem': 0,
			'memp': 0,
		})

	def test_parse_error(t):
		t.assertDictEqual(nodes_top.parse(None), {
			'count': 0,
			'cpu': 0,
			'cpup': 0,
			'mem': 0,
			'memp': 0,
		})

	def test_config(t):
		nodes_top.config({})
		config = [
			# cpu
			call('multigraph nodes_top_cpu'),
			call('graph_title k8stest nodes CPU'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category nodes'),
			call('graph_vlabel millicores'),
			call('graph_printf %3.0lf'),
			call('graph_scale yes'),
			call('f0_total.label total'),
			call('f0_total.colour COLOUR0'),
			call('f0_total.draw AREASTACK'),
			call('f0_total.min 0'),
			call('f1_avg.label average'),
			call('f1_avg.colour COLOUR1'),
			call('f1_avg.min 0'),
			# cpu percentage
			call('multigraph nodes_top_cpup'),
			call('graph_title k8stest nodes CPU usage'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category nodes'),
			call('graph_vlabel percentage'),
			call('graph_printf %3.0lf'),
			call('graph_scale no'),
			call('f0_total.label total'),
			call('f0_total.colour COLOUR0'),
			call('f0_total.draw AREASTACK'),
			call('f0_total.min 0'),
			call('f0_total.max 100'),
			call('f1_avg.label average'),
			call('f1_avg.colour COLOUR1'),
			call('f1_avg.min 0'),
			call('f1_avg.max 100'),
			# mem
			call('multigraph nodes_top_mem'),
			call('graph_title k8stest nodes memory'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category nodes'),
			call('graph_vlabel MiB'),
			call('graph_printf %3.0lf'),
			call('graph_scale yes'),
			call('f0_total.label total'),
			call('f0_total.colour COLOUR0'),
			call('f0_total.draw AREASTACK'),
			call('f0_total.min 0'),
			call('f1_avg.label average'),
			call('f1_avg.colour COLOUR1'),
			call('f1_avg.min 0'),
			# mem percentage
			call('multigraph nodes_top_memp'),
			call('graph_title k8stest nodes memory usage'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category nodes'),
			call('graph_vlabel percentage'),
			call('graph_printf %3.0lf'),
			call('graph_scale no'),
			call('f0_total.label total'),
			call('f0_total.colour COLOUR0'),
			call('f0_total.draw AREASTACK'),
			call('f0_total.min 0'),
			call('f0_total.max 100'),
			call('f1_avg.label average'),
			call('f1_avg.colour COLOUR1'),
			call('f1_avg.min 0'),
			call('f1_avg.max 100'),
		]
		nodes_top._print.assert_has_calls(config)
		t.assertEqual(nodes_top._print.call_count, len(config))

if __name__ == '__main__':
	unittest.main()
