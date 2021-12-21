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

if __name__ == '__main__':
	unittest.main()
