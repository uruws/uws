#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t

import nodes_top

_bup_print = nodes_top._print

_nodes = {
	'count':    3,
	'cpu':      198,
	'cpu_min':  62,
	'cpu_max':  73,
	'cpup':     9,
	'cpup_min': 3,
	'cpup_max': 3,
	'mem':      2509,
	'mem_min':  731,
	'mem_max':  891,
	'memp':     34,
	'memp_min': 10,
	'memp_max': 12,
}

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		nodes_top._print = MagicMock()

	def tearDown(t):
		mon_t.tearDown()
		nodes_top._print = _bup_print

	def test_print(t):
		_bup_print('testing', '...')

	def test_parse(t):
		t.assertDictEqual(nodes_top.parse({}), {
			'count':    0,
			'cpu':      0,
			'cpu_min':  0,
			'cpu_max':  0,
			'cpup':     0,
			'cpup_min': 0,
			'cpup_max': 0,
			'mem':      0,
			'mem_min':  0,
			'mem_max':  0,
			'memp':     0,
			'memp_min': 0,
			'memp_max': 0,
		})

	def test_parse_error(t):
		t.assertDictEqual(nodes_top.parse(None), {
			'count':    0,
			'cpu':      0,
			'cpu_min':  0,
			'cpu_max':  0,
			'cpup':     0,
			'cpup_min': 0,
			'cpup_max': 0,
			'mem':      0,
			'mem_min':  0,
			'mem_max':  0,
			'memp':     0,
			'memp_min': 0,
			'memp_max': 0,
		})

	def test_config(t):
		nodes_top.config(_nodes)
		config = [
			# cpu
			call('multigraph nodes_top_cpu'),
			call('graph_title k8stest nodes CPU'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category nodes'),
			call('graph_vlabel millicores'),
			call('graph_scale yes'),
			call('f1_avg.label average'),
			call('f1_avg.colour COLOUR1'),
			call('f1_avg.min 0'),
			call('f2_min.label min'),
			call('f2_min.colour COLOUR2'),
			call('f2_min.min 0'),
			call('f3_max.label max'),
			call('f3_max.colour COLOUR3'),
			call('f3_max.min 0'),
			# cpu percentage
			call('multigraph nodes_top_cpup'),
			call('graph_title k8stest nodes CPU usage'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category nodes'),
			call('graph_vlabel percentage'),
			call('graph_scale no'),
			call('f1_min.label min'),
			call('f1_min.colour COLOUR1'),
			call('f1_min.min 0'),
			call('f1_min.max 100'),
			call('f2_max.label max'),
			call('f2_max.colour COLOUR2'),
			call('f2_max.min 0'),
			call('f2_max.max 100'),
			# mem
			call('multigraph nodes_top_mem'),
			call('graph_title k8stest nodes memory'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category nodes'),
			call('graph_vlabel MiB'),
			call('graph_scale yes'),
			call('f1_avg.label average'),
			call('f1_avg.colour COLOUR1'),
			call('f1_avg.min 0'),
			call('f2_min.label min'),
			call('f2_min.colour COLOUR2'),
			call('f2_min.min 0'),
			call('f3_max.label max'),
			call('f3_max.colour COLOUR3'),
			call('f3_max.min 0'),
			# mem percentage
			call('multigraph nodes_top_memp'),
			call('graph_title k8stest nodes memory usage'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category nodes'),
			call('graph_vlabel percentage'),
			call('graph_scale no'),
			call('f1_min.label min'),
			call('f1_min.colour COLOUR1'),
			call('f1_min.min 0'),
			call('f1_min.max 100'),
			call('f2_max.label max'),
			call('f2_max.colour COLOUR2'),
			call('f2_max.min 0'),
			call('f2_max.max 100'),
		]
		nodes_top._print.assert_has_calls(config)
		t.assertEqual(nodes_top._print.call_count, len(config))

	def test_report(t):
		nodes_top.report({})
		report = [
			# cpu
			call('multigraph nodes_top_cpu'),
			call('f1_avg.value', 'U'),
			call('f2_min.value', 'U'),
			call('f3_max.value', 'U'),
			# cpu percentage
			call('multigraph nodes_top_cpup'),
			call('f1_min.value', 'U'),
			call('f2_max.value', 'U'),
			# mem
			call('multigraph nodes_top_mem'),
			call('f1_avg.value', 'U'),
			call('f2_min.value', 'U'),
			call('f3_max.value', 'U'),
			# mem percentage
			call('multigraph nodes_top_memp'),
			call('f1_min.value', 'U'),
			call('f2_max.value', 'U'),
		]
		nodes_top._print.assert_has_calls(report)
		t.assertEqual(nodes_top._print.call_count, len(report))

	def test_report_data(t):
		nodes_top.report(_nodes)
		report = [
			# cpu
			call('multigraph nodes_top_cpu'),
			call('f1_avg.value', 66.0),
			call('f2_min.value', 62),
			call('f3_max.value', 73),
			# cpu percentage
			call('multigraph nodes_top_cpup'),
			call('f1_min.value', 3),
			call('f2_max.value', 3),
			# mem
			call('multigraph nodes_top_mem'),
			call('f1_avg.value', 836.3333333333334),
			call('f2_min.value', 731),
			call('f3_max.value', 891),
			# mem percentage
			call('multigraph nodes_top_memp'),
			call('f1_min.value', 10),
			call('f2_max.value', 12),
		]
		nodes_top._print.assert_has_calls(report)
		t.assertEqual(nodes_top._print.call_count, len(report))

if __name__ == '__main__':
	unittest.main()
