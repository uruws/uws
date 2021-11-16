#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
import uwscli_t

import uwscli
import app_scale

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_main_no_args(t):
		with t.assertRaises(SystemExit) as e:
			app_scale.main()
		err = e.exception
		t.assertEqual(err.args[0], 2)

	def test_main_errors(t):
		with uwscli_t.mock_system(status = 99):
			t.assertEqual(app_scale.main(['testing', '999']), 99)
		with uwscli_t.mock_system():
			t.assertEqual(app_scale.main(['testing', '0']), 9)
			t.assertEqual(uwscli_t.err().strip(), 'invalid number of replicas: 0')

	def test_main(t):
		with uwscli_t.mock_system():
			t.assertEqual(app_scale.main(['testing', '99']), 0)
			uwscli.system.assert_called_once_with('/usr/bin/sudo -H -n -u uws -- /srv/uws/deploy/cli/app-ctl.sh uws ktest test scale 99')

if __name__ == '__main__':
	unittest.main()
