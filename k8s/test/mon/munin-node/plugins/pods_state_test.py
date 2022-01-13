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
		t.assertDictEqual(pods_state.parse({}), {})

	def test_parse_data(t):
		t.assertDictEqual(pods_state.parse(_pods), _state)

if __name__ == '__main__':
	unittest.main()
