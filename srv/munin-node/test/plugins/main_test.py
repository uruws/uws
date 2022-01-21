#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import mnpl_t
import main

class Test(unittest.TestCase):

	def setUp(t):
		mnpl_t.setup()

	def tearDown(t):
		mnpl_t.teardown()

	def test_main_error(t):
		t.assertEqual(main.run(['']), 1)

	def test_main(t):
		t.assertEqual(main.run(['testing']), 0)

if __name__ == '__main__':
	unittest.main()
