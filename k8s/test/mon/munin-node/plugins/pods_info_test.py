#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t

import pods_info

_bup_print = pods_info._print

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		pods_info._print = MagicMock()

	def tearDown(t):
		mon_t.tearDown()
		pods_info._print = _bup_print

	def test_print(t):
		_bup_print('testing')

if __name__ == '__main__':
	unittest.main()
