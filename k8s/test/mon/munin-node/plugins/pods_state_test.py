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
				'generateName': 'test-',
			},
			'status': {
				'containerStatuses': [
					{
						'name': 'test',
						'image': 'test.img',
						'ready': True,
						'started': True,
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
					{},
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
					{
						'name': 'test2',
						'image': 'testing/test2.img',
						'restartCount': 9,
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
				'image': {'test.img': 1},
				'state': {
					'Error': 0,
					'Failed': 0,
					'OOMKilled': 0,
					'Restarted': 0,
					'Running': 1,
				},
			},
			'test1': {
				'image': {'test1.img': 1},
				'state': {
					'Error': 1,
					'Failed': 1,
					'OOMKilled': 0,
					'Restarted': 0,
					'Running': 0,
				},
			},
			'test2': {
				'image': {'test2.img': 2},
				'state': {
					'Error': 0,
					'Failed': 2,
					'OOMKilled': 0,
					'Restarted': 1,
					'Running': 0,
					'Testing': 1,
				},
			},
		},
	},
	'total': {
		'Error': 1,
		'Failed': 3,
		'OOMKilled': 0,
		'Restarted': 1,
		'Running': 1,
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
				'Failed': 0,
				'OOMKilled': 0,
				'Restarted': 0,
				'Running': 0,
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
			call('s_Error.draw AREA'),
			call('s_Error.min 0'),
			call('s_Failed.label', 'Failed'),
			call('s_Failed.colour COLOUR1'),
			call('s_Failed.draw AREA'),
			call('s_Failed.min 0'),
			call('s_OOMKilled.label', 'OOMKilled'),
			call('s_OOMKilled.colour COLOUR2'),
			call('s_OOMKilled.draw AREA'),
			call('s_OOMKilled.min 0'),
			call('s_Restarted.label', 'Restarted'),
			call('s_Restarted.colour COLOUR3'),
			call('s_Restarted.draw AREA'),
			call('s_Restarted.min 0'),
			call('s_Running.label', 'Running'),
			call('s_Running.colour COLOUR4'),
			call('s_Running.draw AREA'),
			call('s_Running.min 0'),
			call('s_Testing.label', 'Testing'),
			call('s_Testing.colour COLOUR5'),
			call('s_Testing.draw AREA'),
			call('s_Testing.min 0'),
			# info
			call('multigraph pod_state.testns_test'),
			call('graph_title k8stest testns/test pods state'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category pod'),
			call('graph_vlabel number'),
			call('graph_printf %3.0lf'),
			call('graph_scale no'),
			call('f_Error.label', 'Error'),
			call('f_Error.colour COLOUR0'),
			call('f_Error.draw LINE1'),
			call('f_Error.min 0'),
			call('f_Failed.label', 'Failed'),
			call('f_Failed.colour COLOUR1'),
			call('f_Failed.draw LINE1'),
			call('f_Failed.min 0'),
			call('f_OOMKilled.label', 'OOMKilled'),
			call('f_OOMKilled.colour COLOUR2'),
			call('f_OOMKilled.draw LINE1'),
			call('f_OOMKilled.min 0'),
			call('f_Restarted.label', 'Restarted'),
			call('f_Restarted.colour COLOUR3'),
			call('f_Restarted.draw LINE1'),
			call('f_Restarted.min 0'),
			call('f_Running.label', 'Running'),
			call('f_Running.colour COLOUR4'),
			call('f_Running.draw LINE1'),
			call('f_Running.min 0'),
			call('z_test_img.label', 'test.img'),
			call('z_test_img.colour COLOUR5'),
			call('z_test_img.draw AREASTACK'),
			call('z_test_img.min 0'),
			call('multigraph pod_state.testns_test1'),
			call('graph_title k8stest testns/test1 pods state'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category pod'),
			call('graph_vlabel number'),
			call('graph_printf %3.0lf'),
			call('graph_scale no'),
			call('f_Error.label', 'Error'),
			call('f_Error.colour COLOUR0'),
			call('f_Error.draw LINE1'),
			call('f_Error.min 0'),
			call('f_Failed.label', 'Failed'),
			call('f_Failed.colour COLOUR1'),
			call('f_Failed.draw LINE1'),
			call('f_Failed.min 0'),
			call('f_OOMKilled.label', 'OOMKilled'),
			call('f_OOMKilled.colour COLOUR2'),
			call('f_OOMKilled.draw LINE1'),
			call('f_OOMKilled.min 0'),
			call('f_Restarted.label', 'Restarted'),
			call('f_Restarted.colour COLOUR3'),
			call('f_Restarted.draw LINE1'),
			call('f_Restarted.min 0'),
			call('f_Running.label', 'Running'),
			call('f_Running.colour COLOUR4'),
			call('f_Running.draw LINE1'),
			call('f_Running.min 0'),
			call('z_test1_img.label', 'test1.img'),
			call('z_test1_img.colour COLOUR5'),
			call('z_test1_img.draw AREASTACK'),
			call('z_test1_img.min 0'),
			call('multigraph pod_state.testns_test2'),
			call('graph_title k8stest testns/test2 pods state'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category pod'),
			call('graph_vlabel number'),
			call('graph_printf %3.0lf'),
			call('graph_scale no'),
			call('f_Error.label', 'Error'),
			call('f_Error.colour COLOUR0'),
			call('f_Error.draw LINE1'),
			call('f_Error.min 0'),
			call('f_Failed.label', 'Failed'),
			call('f_Failed.colour COLOUR1'),
			call('f_Failed.draw LINE1'),
			call('f_Failed.min 0'),
			call('f_OOMKilled.label', 'OOMKilled'),
			call('f_OOMKilled.colour COLOUR2'),
			call('f_OOMKilled.draw LINE1'),
			call('f_OOMKilled.min 0'),
			call('f_Restarted.label', 'Restarted'),
			call('f_Restarted.colour COLOUR3'),
			call('f_Restarted.draw LINE1'),
			call('f_Restarted.min 0'),
			call('f_Running.label', 'Running'),
			call('f_Running.colour COLOUR4'),
			call('f_Running.draw LINE1'),
			call('f_Running.min 0'),
			call('f_Testing.label', 'Testing'),
			call('f_Testing.colour COLOUR5'),
			call('f_Testing.draw LINE1'),
			call('f_Testing.min 0'),
			call('z_test2_img.label', 'test2.img'),
			call('z_test2_img.colour COLOUR6'),
			call('z_test2_img.draw AREASTACK'),
			call('z_test2_img.min 0'),
		]
		pods_state._print.assert_has_calls(config)
		t.assertEqual(pods_state._print.call_count, len(config))

	def test_report(t):
		pods_state.report(_state)
		report = [
			# total
			call('multigraph pod_state'),
			call('s_Error.value', 1),
			call('s_Failed.value', 3),
			call('s_OOMKilled.value', 0),
			call('s_Restarted.value', 1),
			call('s_Running.value', 1),
			call('s_Testing.value', 1),
			# info
			call('multigraph pod_state.testns_test'),
			call('f_Error.value', 0),
			call('f_Failed.value', 0),
			call('f_OOMKilled.value', 0),
			call('f_Restarted.value', 0),
			call('f_Running.value', 1),
			call('z_test_img.value', 1),
			call('multigraph pod_state.testns_test1'),
			call('f_Error.value', 1),
			call('f_Failed.value', 1),
			call('f_OOMKilled.value', 0),
			call('f_Restarted.value', 0),
			call('f_Running.value', 0),
			call('z_test1_img.value', 1),
			call('multigraph pod_state.testns_test2'),
			call('f_Error.value', 0),
			call('f_Failed.value', 2),
			call('f_OOMKilled.value', 0),
			call('f_Restarted.value', 1),
			call('f_Running.value', 0),
			call('f_Testing.value', 1),
			call('z_test2_img.value', 2),
		]
		pods_state._print.assert_has_calls(report)
		t.assertEqual(pods_state._print.call_count, len(report))

if __name__ == '__main__':
	unittest.main()
