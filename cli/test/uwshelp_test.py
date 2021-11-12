#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
import uwscli_t

import uwscli
import uwshelp

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_main_no_args(t):
		t.assertEqual(uwshelp.main(), 0)

	def test_main_errors(t):
		with uwscli_t.mock_system(99):
			t.assertEqual(uwshelp.main(['testing']), 99)

	def test_main(t):
		with uwscli_t.mock_system(0):
			t.assertEqual(uwshelp.main(), 0)
		with uwscli_t.mock_system(0):
			t.assertEqual(uwshelp.main(['testing']), 0)
			uwscli.system.assert_called_once_with('/srv/home/uwscli/bin/testing --help')

if __name__ == '__main__':
	unittest.main()
