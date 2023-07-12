#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t

import nodes_taint

_bup_print = nodes_taint._print

_nodes = {
	'NoExecute': 1,
	'NoSchedule': 0,
	'PreferNoSchedule': 0,
	'Testing': 1,
	'Unknown': 1,
	'Total': 2,
}

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		nodes_taint._print = MagicMock()

	def tearDown(t):
		mon_t.tearDown()
		nodes_taint._print = _bup_print

	def test_print(t):
		_bup_print('testing', '...')

	def test_parse(t):
		t.assertDictEqual(nodes_taint.parse({}), {
			'NoExecute': 0,
			'NoSchedule': 0,
			'PreferNoSchedule': 0,
			'Total': 0,
			'Unknown': 0,
		})

	def test_parse_data(t):
		nodes = {
			'items': [
				{
					'kind': 'Node',
					'spec': {
						'taints': [
							{
								'effect': 'Testing',
							},
							{
								'effect': 'NoExecute',
								'key': 'testing',
							},
						],
					},
				},
				{
					'kind': 'Node',
					'spec': {
						'taints': [{}],
					},
				},
			],
		}
		t.assertDictEqual(nodes_taint.parse(nodes), _nodes)

	def test_config_alert_levels(t):
		n = {
			'Testing': 1,
			'Total':   0,
		}
		nodes_taint.config(n)
		config = [
			call('multigraph nodes_taint'),
			call('graph_title k8stest nodes taint'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category nodes'),
			call('graph_vlabel number'),
			call('graph_printf %3.0lf'),
			call('graph_scale yes'),
			call('t_testing.label Testing'),
			call('t_testing.colour COLOUR0'),
			call('t_testing.draw LINE'),
			call('t_testing.min 0'),
			call('t_testing.warning', 1),
			call('t_testing.critical', 1),
		]
		nodes_taint._print.assert_has_calls(config)
		t.assertEqual(nodes_taint._print.call_count, len(config))

	def test_config(t):
		nodes_taint.config(_nodes)
		config = [
			call('multigraph nodes_taint'),
			call('graph_title k8stest nodes taint'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category nodes'),
			call('graph_vlabel number'),
			call('graph_printf %3.0lf'),
			call('graph_scale yes'),
			call('t_noexecute.label NoExecute'),
			call('t_noexecute.colour COLOUR0'),
			call('t_noexecute.draw LINE'),
			call('t_noexecute.min 0'),
			call('t_noexecute.warning', 1),
			call('t_noexecute.critical', 1),
			call('t_noschedule.label NoSchedule'),
			call('t_noschedule.colour COLOUR1'),
			call('t_noschedule.draw LINE'),
			call('t_noschedule.min 0'),
			call('t_noschedule.warning', 1),
			call('t_noschedule.critical', 1),
			call('t_prefernoschedule.label PreferNoSchedule'),
			call('t_prefernoschedule.colour COLOUR2'),
			call('t_prefernoschedule.draw LINE'),
			call('t_prefernoschedule.min 0'),
			call('t_testing.label Testing'),
			call('t_testing.colour COLOUR3'),
			call('t_testing.draw LINE'),
			call('t_testing.min 0'),
			call('t_testing.warning', 1),
			call('t_testing.critical', 1),
			call('t_unknown.label Unknown'),
			call('t_unknown.colour COLOUR4'),
			call('t_unknown.draw LINE'),
			call('t_unknown.min 0'),
			call('t_unknown.warning', 1),
			call('t_unknown.critical', 1),
		]
		nodes_taint._print.assert_has_calls(config)
		t.assertEqual(nodes_taint._print.call_count, len(config))

	def test_report(t):
		nodes_taint.report(_nodes)
		report = [
			call('multigraph nodes_taint'),
			call('t_noexecute.value', 1),
			call('t_noschedule.value', 0),
			call('t_prefernoschedule.value', 0),
			call('t_testing.value', 1),
			call('t_unknown.value', 1),
		]
		nodes_taint._print.assert_has_calls(report)
		t.assertEqual(nodes_taint._print.call_count, len(report))

if __name__ == '__main__':
	unittest.main()
