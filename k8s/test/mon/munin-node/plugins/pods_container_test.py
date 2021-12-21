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

if __name__ == '__main__':
	unittest.main()
