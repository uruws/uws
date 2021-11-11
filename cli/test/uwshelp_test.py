#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
import uwscli_t

import uwshelp

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_main_no_args(t):
		t.assertEqual(uwshelp.main(), 0)

	def test_main(t):
		t.assertEqual(uwshelp.main(['testing']), 127)

if __name__ == '__main__':
	unittest.main()
