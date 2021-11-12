#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
import uwscli_t

import app_deploy

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_deploy_error(t):
		t.assertEqual(app_deploy.deploy('testing', '0.999'), 127)
		with uwscli_t.mock_system(status = 99):
			t.assertEqual(app_deploy.deploy('testing', '0.999'), 99)

	def test_deploy(t):
		with uwscli_t.mock_system():
			t.assertEqual(app_deploy.deploy('testing', '0.999'), 0)

	def test_main_no_args(t):
		with t.assertRaises(SystemExit) as e:
			app_deploy.main()
		err = e.exception
		t.assertEqual(err.args[0], 2)

	def test_main(t):
		t.assertEqual(app_deploy.main(['testing']), 0)
		t.assertEqual(uwscli_t.out().strip(), 'no available builds for testing')
		with uwscli_t.mock_list_images(['img-1']):
			t.assertEqual(app_deploy.main(['testing']), 0)
			t.assertEqual(uwscli_t.out().strip(), 'available testing builds:\n  img-1')

if __name__ == '__main__':
	unittest.main()
