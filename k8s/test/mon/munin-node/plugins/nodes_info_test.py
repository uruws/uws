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

if __name__ == '__main__':
	unittest.main()
