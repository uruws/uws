#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
import uwscli_t

import app_build
import uwscli

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_main_no_args(t):
		with t.assertRaises(SystemExit) as e:
			app_build.main()
		err = e.exception
		t.assertEqual(err.args[0], 2)

	def test_main(t):
		t.assertEqual(app_build.main(['testing', '0.999']), 9)

	def test_check_storage(t):
		with uwscli_t.mock_gso(output = '100'):
			t.assertEqual(app_build.check_storage(), 0)
			uwscli.gso.assert_called_once_with("df -kl /srv/docker | tail -n1 | awk '{ print $4 }'")
		with uwscli_t.mock_gso(output = '3'):
			t.assertEqual(app_build.check_storage(), 8)

	def test_check_storage_error(t):
		with uwscli_t.mock_gso(output = 'testing'):
			t.assertEqual(app_build.check_storage(), 9)
		t.assertEqual(uwscli_t.err().strip(), 'value error: testing')
		with uwscli_t.mock_gso(status = 2, output = 'mock_error'):
			t.assertEqual(app_build.check_storage(), 2)
		t.assertEqual(uwscli_t.err().strip(), 'mock_error')

if __name__ == '__main__':
	unittest.main()
