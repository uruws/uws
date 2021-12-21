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

if __name__ == '__main__':
	unittest.main()
