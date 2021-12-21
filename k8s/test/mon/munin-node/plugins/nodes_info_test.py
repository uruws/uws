#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t

import nodes_info

_bup_print = nodes_info._print

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
			'condition': {},
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
						],
					},
				},
			],
		}
		t.assertDictEqual(nodes_info.parse(nodes), {
			'condition': {'Prod': 0, 'Testing': 1},
			'nodes': 2,
			'nodes_type': {'testing': 1, 'unknown': 1},
		})

	def test_config(t):
		nodes_info.config({
			'nodes_type': {
				'testing': 1,
			},
			'condition': {
				'Testing': 1,
			}
		})
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
			# condition
			call('multigraph nodes_condition'),
			call('graph_title k8stest nodes condition'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category nodes'),
			call('graph_vlabel number'),
			call('graph_printf %3.0lf'),
			call('graph_scale yes'),
			call('graph_total total'),
			call('c_testing.label Testing'),
			call('c_testing.colour COLOUR0'),
			call('c_testing.draw AREASTACK'),
			call('c_testing.min 0'),
		]
		nodes_info._print.assert_has_calls(config)
		t.assertEqual(nodes_info._print.call_count, len(config))

	def test_report(t):
		nodes_info.report({
			'nodes_type': {
				'testing': 1,
			},
			'condition': {
				'Testing': 1,
			}
		})
		report = [
			# nodes
			call('multigraph nodes'),
			call('a_total.value', 'U'),
			call('t_testing.value', 1),
			# condition
			call('multigraph nodes_condition'),
			call('c_testing.value', 1),
		]
		nodes_info._print.assert_has_calls(report)
		t.assertEqual(nodes_info._print.call_count, len(report))

if __name__ == '__main__':
	unittest.main()
