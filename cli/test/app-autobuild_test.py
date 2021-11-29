#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
import uwscli_t

import uwscli
import app_autobuild

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_main_no_args(t):
		with t.assertRaises(SystemExit) as e:
			app_autobuild.main()
		err = e.exception
		t.assertEqual(err.args[0], 2)

	def test_invalid_app(t):
		with t.assertRaises(SystemExit) as e:
			app_autobuild.main(['noapp'])
		err = e.exception
		t.assertEqual(err.args[0], 2)

	def test_main_errors(t):
		with t.assertRaises(SystemExit) as e:
			app_autobuild.main(['testing'])
		err = e.exception
		t.assertEqual(err.args[0], 2)
		t.assertEqual(uwscli_t.err().strip(),
			'[ERROR] chdir not found: /srv/deploy/Testing')
		with uwscli_t.mock_chdir():
			with uwscli_t.mock_system(status = 99):
				t.assertEqual(app_autobuild.main(['testing']), 99)

	def test_main(t):
		with uwscli_t.mock_chdir():
			with uwscli_t.mock_system():
				t.assertEqual(app_autobuild.main(['testing']), 0)

if __name__ == '__main__':
	unittest.main()
