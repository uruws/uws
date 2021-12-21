#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t

import pods_condition

_bup_print = pods_condition._print

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		pods_condition._print = MagicMock()

	def tearDown(t):
		mon_t.tearDown()
		pods_condition._print = _bup_print

	def test_print(t):
		_bup_print('testing')

	def test_parse(t):
		t.assertDictEqual(pods_condition.parse({}), {
			'cond': {},
			'index': {
				'ContainersReady': 0,
				'Initialized': 0,
				'PodScheduled': 0,
				'Ready': 0,
			},
		})

	def test_parse_data(t):
		pods = {
			'items': [
				{
					'kind': 'Testing',
				},
				{
					'kind': 'Pod',
					'metadata': {
						'namespace': 'ns',
						'generateName': 'test',
					},
					'status': {
						'conditions': [
							{
								'status': 'True',
								'type': 'Testing',
							},
						],
					},
				},
			],
		}
		t.assertDictEqual(pods_condition.parse(pods), {
			'cond': {
				'ns': {
					'test': {
						'ContainersReady': 0,
						'Initialized': 0,
						'PodScheduled': 0,
						'Ready': 0,
						'Testing': 1,
					},
				},
			},
			'index': {
				'ContainersReady': 0,
				'Initialized': 0,
				'PodScheduled': 0,
				'Ready': 0,
				'Testing': 1,
			},
		})

	def test_config(t):
		pods = {
			'cond': {
				'ns': {
					'test': {
						'ContainersReady': 0,
						'Initialized': 0,
						'PodScheduled': 0,
						'Ready': 0,
						'Testing': 1,
					},
				},
			},
			'index': {
				'ContainersReady': 0,
				'Initialized': 0,
				'PodScheduled': 0,
				'Ready': 0,
				'Testing': 1,
			},
		}
		pods_condition.config(pods)
		config = [
			# index
			call('multigraph pod_condition'),
			call('graph_title k8stest pods condition'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category pod'),
			call('graph_vlabel number'),
			call('graph_printf %3.0lf'),
			call('graph_scale yes'),
			call('c_containersready.label', 'ContainersReady'),
			call('c_containersready.colour COLOUR0'),
			call('c_containersready.min 0'),
			call('c_initialized.label', 'Initialized'),
			call('c_initialized.colour COLOUR1'),
			call('c_initialized.min 0'),
			call('c_podscheduled.label', 'PodScheduled'),
			call('c_podscheduled.colour COLOUR2'),
			call('c_podscheduled.min 0'),
			call('c_ready.label', 'Ready'),
			call('c_ready.colour COLOUR3'),
			call('c_ready.min 0'),
			call('c_testing.label', 'Testing'),
			call('c_testing.colour COLOUR4'),
			call('c_testing.min 0'),
			# status
			call('multigraph pod_condition.ns_test'),
			call('graph_title k8stest ns/test condition'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category pod'),
			call('graph_vlabel number of pods'),
			call('graph_printf %3.0lf'),
			call('graph_scale yes'),
			call('c_containersready.label', 'ContainersReady'),
			call('c_containersready.colour COLOUR0'),
			call('c_containersready.min 0'),
			call('c_initialized.label', 'Initialized'),
			call('c_initialized.colour COLOUR1'),
			call('c_initialized.min 0'),
			call('c_podscheduled.label', 'PodScheduled'),
			call('c_podscheduled.colour COLOUR2'),
			call('c_podscheduled.min 0'),
			call('c_ready.label', 'Ready'),
			call('c_ready.colour COLOUR3'),
			call('c_ready.min 0'),
			call('c_testing.label', 'Testing'),
			call('c_testing.colour COLOUR4'),
			call('c_testing.min 0'),
		]
		pods_condition._print.assert_has_calls(config)
		t.assertEqual(pods_condition._print.call_count, len(config))

	def test_report(t):
		pods = {
			'cond': {
				'ns': {
					'test': {
						'ContainersReady': 0,
						'Initialized': 0,
						'PodScheduled': 0,
						'Ready': 0,
						'Testing': 1,
					},
				},
			},
			'index': {
				'ContainersReady': 0,
				'Initialized': 0,
				'PodScheduled': 0,
				'Ready': 0,
				'Testing': 1,
			},
		}
		pods_condition.report(pods)
		report = [
			# index
			call('multigraph pod_condition'),
			call('c_containersready.value', 0),
			call('c_initialized.value', 0),
			call('c_podscheduled.value', 0),
			call('c_ready.value', 0),
			call('c_testing.value', 1),
			# status
			call('multigraph pod_condition.ns_test'),
			call('c_containersready.value', 0),
			call('c_initialized.value', 0),
			call('c_podscheduled.value', 0),
			call('c_ready.value', 0),
			call('c_testing.value', 1),
		]
		pods_condition._print.assert_has_calls(report)
		t.assertEqual(pods_condition._print.call_count, len(report))

if __name__ == '__main__':
	unittest.main()
