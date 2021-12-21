#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t

import pods_container

_bup_print = pods_container._print

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		pods_container._print = MagicMock()

	def tearDown(t):
		mon_t.tearDown()
		pods_container._print = _bup_print

	def test_print(t):
		_bup_print('testing')

	def test_globals(t):
		t.assertDictEqual(pods_container.limits, {
			'failed_ratio': {
				'warning': 1,
				'critical': 2,
			},
			'restart_ratio': {
				'warning': 1,
				'critical': 2,
			},
		})

	def test_parse(t):
		t.assertDictEqual(pods_container.parse({}), {
			'index': {},
			'info': {},
			'status': {},
		})

	def test_parse_data(t):
		t.maxDiff = None
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
						'phase': 'testing',
					},
				},
			],
		}
		# ~ pods_container.parse(pods)
		t.assertDictEqual(pods_container.parse(pods), {
			'index': {
				'failed': 0,
				'failed_ratio': 0,
				'pending': 0,
				'ready': 0,
				'restart': 0,
				'restart_ratio': 0,
				'restarted': 0,
				'running': 0,
				'spec': 0,
				'started': 0,
				'testing': 0,
			},
			'info': {
				'ns': {
					'test': {
						'spec': {},
						'status': {
							'testing': {},
						},
					},
				},
			},
			'status': {
				'ns': {
					'test': {
						'failed': 0,
						'failed_ratio': 0,
						'pending': 0,
						'ready': 0,
						'restart': 0,
						'restart_ratio': 0,
						'restarted': 0,
						'running': 0,
						'spec': 0,
						'started': 0,
						'testing': 0,
					},
				},
			},
		})

	def test_parse_container_info(t):
		t.maxDiff = None
		pods = {
			'items': [
				{
					'kind': 'Pod',
					'metadata': {
						'namespace': 'ns',
						'generateName': 'test',
					},
					'status': {
						'phase': 'testing',
						'containerStatuses': [{'image': 'testing.img'}],
					},
					'spec': {
						'containers': [{'image': 'testing.img'}],
					},
				},
			],
		}
		t.assertDictEqual(pods_container.parse(pods), {
			'index': {
				'failed': 0,
				'failed_ratio': 0,
				'pending': 0,
				'ready': 0,
				'restart': 0,
				'restart_ratio': 0,
				'restarted': 0,
				'running': 0,
				'spec': 1,
				'started': 0,
				'testing': 1,
			},
			'info': {
				'ns': {
					'test': {
						'spec': {'testing.img': True},
						'status': {
							'testing': {'testing.img': 1},
						},
					},
				},
			},
			'status': {
				'ns': {
					'test': {
						'failed': 0,
						'failed_ratio': 0,
						'pending': 0,
						'ready': 0,
						'restart': 0,
						'restart_ratio': 0,
						'restarted': 0,
						'running': 0,
						'spec': 1,
						'started': 0,
						'testing': 1,
					},
				},
			},
		})

	def test_parse_container_status(t):
		t.maxDiff = None
		pods = {
			'items': [
				{
					'kind': 'Pod',
					'metadata': {
						'namespace': 'ns',
						'generateName': 'test',
					},
					'status': {
						'phase': 'Running',
						'containerStatuses': [{
							'image': 'testing.img',
							'restartCount': 1,
							'ready': True,
							'started': True,
						}],
					},
					'spec': {
						'containers': [{'image': 'testing.img'}],
					},
				},
			],
		}
		t.assertDictEqual(pods_container.parse(pods), {
			'index': {
				'failed': 0,
				'failed_ratio': 0.0,
				'pending': 0,
				'ready': 1,
				'restart': 1,
				'restart_ratio': 1.0,
				'restarted': 1,
				'running': 1,
				'spec': 1,
				'started': 1,
			},
			'info': {
				'ns': {
					'test': {
						'spec': {'testing.img': True},
						'status': {
							'running': {'testing.img': 1},
						},
					},
				},
			},
			'status': {
				'ns': {
					'test': {
						'failed': 0,
						'failed_ratio': 0.0,
						'pending': 0,
						'ready': 1,
						'restart': 1,
						'restart_ratio': 1.0,
						'restarted': 1,
						'running': 1,
						'spec': 1,
						'started': 1,
					},
				},
			},
		})

	def test_config(t):
		pods = {
			'index': {
				'abc': 1,
			},
			'info': {
				'ns': {
					'test': {
						'spec': {'testing.img': True},
						'status': {
							'testing': {'testing.img': 1},
						},
					},
				},
			},
			'status': {
				'ns': {
					'test': {
						'abc': 1,
						'failed_ratio': 0,
					},
				},
			},
		}
		pods_container.config(pods)
		config = [
			# index
			call('multigraph pod_container'),
			call('graph_title k8stest pods containers'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category pod'),
			call('graph_vlabel number'),
			call('graph_scale no'),
			call('abc.label', 'abc'),
			call('abc.colour COLOUR0'),
			call('abc.min 0'),
			# status
			call('multigraph pod_container.ns_test'),
			call('graph_title k8stest ns/test'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category pod'),
			call('graph_vlabel containers number'),
			call('graph_scale no'),
			call('abc.label', 'abc'),
			call('abc.colour COLOUR0'),
			call('abc.min 0'),
			call('failed_ratio.label', 'failed ratio'),
			call('failed_ratio.colour COLOUR1'),
			call('failed_ratio.min 0'),
			# limits
			call('failed_ratio.warning', 1),
			call('failed_ratio.critical', 2),
			# info
			# spec
			call('zza_spec_0000.label S', 'testing.img'),
			call('zza_spec_0000.colour COLOUR2'),
			call('zza_spec_0000.min 0'),
			# status
			call('zzz_testing_0000.label', 'T', 'testing.img'),
			call('zzz_testing_0000.colour COLOUR3'),
			call('zzz_testing_0000.min 0'),
		]
		pods_container._print.assert_has_calls(config)
		t.assertEqual(pods_container._print.call_count, len(config))

if __name__ == '__main__':
	unittest.main()
