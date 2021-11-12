#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
import uwscli_t

import uwscli
import app_restart

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_main_no_args(t):
		with t.assertRaises(SystemExit) as e:
			app_restart.main()
		err = e.exception
		t.assertEqual(err.args[0], 2)

	def test_main_errors(t):
		with uwscli_t.mock_system(99):
			t.assertEqual(app_restart.main(['testing']), 99)

	def test_main(t):
		with uwscli_t.mock_system():
			t.assertEqual(app_restart.main(['testing']), 0)
			uwscli.system.assert_called_once_with('/usr/bin/sudo -H -n -u uws -- /srv/uws/deploy/cli/app-ctl.sh uws ktest test restart')

if __name__ == '__main__':
	unittest.main()
