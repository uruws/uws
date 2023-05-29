#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t

import nodes_info

_bup_print = nodes_info._print

_nodes = {
	'condition': {'Prod': 0, 'Ready': 0, 'Testing': 1, 'Unknown': 1},
	'nodes': 2,
	'nodes_type': {'testing': 1, 'unknown': 1},
}

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		nodes_info._print = MagicMock()

	def tearDown(t):
		mon_t.tearDown()
		nodes_info._print = _bup_print

	def test_print(t):
		_bup_print('testing')

	def test_parse(t):
		t.assertDictEqual(nodes_info.parse({}), {
			'condition': {
				'Unknown': 0,
			},
			'nodes': 0,
			'nodes_type': {},
		})

	def test_parse_data(t):
		nodes = {
			'items': [
				{
					'kind': 'Node',
					'metadata': {
						'labels': {
							'node.kubernetes.io/instance-type': 'testing',
						},
					},
				},
				{
					'kind': 'Node',
					'status': {
						'conditions': [
							{
								'status': 'True',
								'type': 'Testing',
							},
							{
								'status': 'False',
								'type': 'Prod',
							},
							{
								'status': 'Unknown',
								'type': 'Ready',
							},
						],
					},
				},
			],
		}
		t.assertDictEqual(nodes_info.parse(nodes), _nodes)

	def test_config(t):
		nodes_info.config(_nodes)
		config = [
			# nodes
			call('multigraph nodes'),
			call('graph_title k8stest nodes'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category nodes'),
			call('graph_vlabel number'),
			call('graph_printf %3.0lf'),
			call('graph_scale yes'),
			call('a_total.label nodes'),
			call('a_total.colour COLOUR0'),
			call('a_total.draw AREASTACK'),
			call('a_total.min 0'),
			call('t_testing.label', 'testing'),
			call('t_testing.colour COLOUR1'),
			call('t_testing.min 0'),
			call('t_unknown.label', 'unknown'),
			call('t_unknown.colour COLOUR2'),
			call('t_unknown.min 0'),
			# condition
			call('multigraph nodes_condition'),
			call('graph_title k8stest nodes condition'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category nodes'),
			call('graph_vlabel number'),
			call('graph_printf %3.0lf'),
			call('graph_scale yes'),
			call('graph_total total'),
			call('c_prod.label Prod'),
			call('c_prod.colour COLOUR0'),
			call('c_prod.draw AREASTACK'),
			call('c_prod.min 0'),
			call('c_ready.label Ready'),
			call('c_ready.colour COLOUR1'),
			call('c_ready.draw AREASTACK'),
			call('c_ready.min 0'),
			call('c_testing.label Testing'),
			call('c_testing.colour COLOUR2'),
			call('c_testing.draw AREASTACK'),
			call('c_testing.min 0'),
			call('c_unknown.label Unknown'),
			call('c_unknown.colour COLOUR3'),
			call('c_unknown.draw AREASTACK'),
			call('c_unknown.min 0'),
			call('c_unknown.warning', 3),
			call('c_unknown.critical', 5),
		]
		nodes_info._print.assert_has_calls(config)
		t.assertEqual(nodes_info._print.call_count, len(config))

	def test_report(t):
		nodes_info.report(_nodes)
		report = [
			# nodes
			call('multigraph nodes'),
			call('a_total.value', 2),
			call('t_testing.value', 1),
			call('t_unknown.value', 1),
			# condition
			call('multigraph nodes_condition'),
			call('c_prod.value', 0),
			call('c_ready.value', 0),
			call('c_testing.value', 1),
			call('c_unknown.value', 1),
		]
		nodes_info._print.assert_has_calls(report)
		t.assertEqual(nodes_info._print.call_count, len(report))

if __name__ == '__main__':
	unittest.main()
