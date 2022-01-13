#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t

import pods_state

_bup_print = pods_state._print

_pods = {
	'items': [
		{},
		{
			'kind': 'Pod',
			'metadata': {
				'namespace': 'testns',
			},
			'status': {
				'containerStatuses': [
					{},
					{
						'name': 'test',
						'image': 'test.img',
						'lastState': {
							'terminated': {
								'reason': '',
							},
						},
					},
				],
			},
		},
		{
			'kind': 'Pod',
		},
		{
			'kind': 'Pod',
			'metadata': {
				'namespace': 'testns',
			},
			'status': {
				'containerStatuses': [
					{
						'name': 'test1',
						'image': 'test1.img',
						'lastState': {
							'terminated': {
								'reason': 'Error',
							},
						},
					},
					{
						'name': 'test2',
						'image': 'test2.img',
						'lastState': {
							'terminated': {
								'reason': 'Testing',
							},
						},
					},
				],
			},
		},
	],
}

_state = {
	'info': {
		'testns': {
			'test': {
				'image': 'test.img',
				'state': {
					'Error': 0,
					'OOMKilled': 0,
				},
			},
			'test1': {
				'image': 'test1.img',
				'state': {
					'Error': 1,
					'OOMKilled': 0,
				},
			},
			'test2': {
				'image': 'test2.img',
				'state': {
					'Error': 0,
					'OOMKilled': 0,
					'Testing': 1,
				},
			},
		},
	},
	'total': {
		'Error': 1,
		'OOMKilled': 0,
		'Testing': 1,
	},
}

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		pods_state._print = MagicMock()

	def tearDown(t):
		mon_t.tearDown()
		pods_state._print = _bup_print

	def test_print(t):
		_bup_print('test', 'ing')

	def test_parse(t):
		t.assertDictEqual(pods_state.parse({}), {
			'info': {},
			'total': {
				'Error': 0,
				'OOMKilled': 0,
			},
		})

	def test_parse_data(t):
		t.maxDiff = None
		t.assertDictEqual(pods_state.parse(_pods), _state)

	def test_config(t):
		pods_state.config(_state)
		config = [
			# total
			call('multigraph pod_state'),
			call('graph_title k8stest pods state'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category pod'),
			call('graph_vlabel number'),
			call('graph_printf %3.0lf'),
			call('graph_scale no'),
			call('s_Error.label', 'Error'),
			call('s_Error.colour COLOUR0'),
			call('s_Error.min 0'),
			call('s_OOMKilled.label', 'OOMKilled'),
			call('s_OOMKilled.colour COLOUR1'),
			call('s_OOMKilled.min 0'),
			call('s_Testing.label', 'Testing'),
			call('s_Testing.colour COLOUR2'),
			call('s_Testing.min 0'),
			# info
			call('multigraph pod_state.testns_test'),
			call('graph_title k8stest testns/test pods state'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category pod'),
			call('graph_vlabel number'),
			call('graph_printf %3.0lf'),
			call('graph_scale no'),
			call('s_Error.label', 'Error'),
			call('s_Error.colour COLOUR0'),
			call('s_Error.min 0'),
			call('s_Error.info', 'test.img'),
			call('s_OOMKilled.label', 'OOMKilled'),
			call('s_OOMKilled.colour COLOUR1'),
			call('s_OOMKilled.min 0'),
			call('s_OOMKilled.info', 'test.img'),
			call('multigraph pod_state.testns_test1'),
			call('graph_title k8stest testns/test1 pods state'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category pod'),
			call('graph_vlabel number'),
			call('graph_printf %3.0lf'),
			call('graph_scale no'),
			call('s_Error.label', 'Error'),
			call('s_Error.colour COLOUR0'),
			call('s_Error.min 0'),
			call('s_Error.info', 'test1.img'),
			call('s_OOMKilled.label', 'OOMKilled'),
			call('s_OOMKilled.colour COLOUR1'),
			call('s_OOMKilled.min 0'),
			call('s_OOMKilled.info', 'test1.img'),
			call('multigraph pod_state.testns_test2'),
			call('graph_title k8stest testns/test2 pods state'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category pod'),
			call('graph_vlabel number'),
			call('graph_printf %3.0lf'),
			call('graph_scale no'),
			call('s_Error.label', 'Error'),
			call('s_Error.colour COLOUR0'),
			call('s_Error.min 0'),
			call('s_Error.info', 'test2.img'),
			call('s_OOMKilled.label', 'OOMKilled'),
			call('s_OOMKilled.colour COLOUR1'),
			call('s_OOMKilled.min 0'),
			call('s_OOMKilled.info', 'test2.img'),
			call('s_Testing.label', 'Testing'),
			call('s_Testing.colour COLOUR2'),
			call('s_Testing.min 0'),
			call('s_Testing.info', 'test2.img'),
		]
		pods_state._print.assert_has_calls(config)
		t.assertEqual(pods_state._print.call_count, len(config))

	def test_report(t):
		pods_state.report(_state)
		report = [
			# total
			call('multigraph pod_state'),
			call('s_Error.value', 1),
			call('s_OOMKilled.value', 0),
			call('s_Testing.value', 1),
		]
		pods_state._print.assert_has_calls(report)
		t.assertEqual(pods_state._print.call_count, len(report))

if __name__ == '__main__':
	unittest.main()
