#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib import contextmanager

import unittest
from unittest.mock import MagicMock, call

import mon_t

import deploy_condition

_bup_print = deploy_condition._print

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		deploy_condition._print = MagicMock()

	def tearDown(t):
		mon_t.tearDown()
		deploy_condition._print = _bup_print

	def test_parse(t):
		info = {
			'status': {
				'conditions': [
					{'status': 'True', 'type': 'Testing'},
				],
			},
		}
		sts = {}
		deploy_condition.parse(sts, 'ns', 'name', info)
		t.assertDictEqual(sts, {
			'condition': {'ns': {'name': {'Testing': 1}}},
			'condition_index': {'Testing': 1},
		})

	def test_print(t):
		_bup_print('testing')

if __name__ == '__main__':
	unittest.main()
