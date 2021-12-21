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
		_bup_print('test', 'ing')

if __name__ == '__main__':
	unittest.main()
