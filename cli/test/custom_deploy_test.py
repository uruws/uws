#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
import uwscli_t

import custom_deploy

def _newcfg():
	return custom_deploy.Config('testing_app', app_name = 'testing', app_env = 'test')

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_config(t):
		c = _newcfg()
		t.assertTrue(c.check())
		t.assertEqual(c.fn, 'testing_app')

	def test_config_check_error(t):
		# fn
		with t.assertRaises(RuntimeError):
			c = _newcfg()
			c.fn = ''
			c.check()
		# app_name
		with t.assertRaises(RuntimeError):
			c = _newcfg()
			c.app_name = ''
			c.check()
		# app_env
		with t.assertRaises(RuntimeError):
			c = _newcfg()
			c.app_env = ''
			c.check()
		# app_name: invalid
		with t.assertRaises(RuntimeError):
			c = _newcfg()
			c.app_name = 'invalid_app_name'
			c.check()

	def test_main(t):
		c = _newcfg()
		t.assertEqual(custom_deploy.main([], c), 0)

	def test_main_config_check_error(t):
		c = _newcfg()
		c.app_env = ''
		t.assertEqual(custom_deploy.main([], c), 9)

if __name__ == '__main__':
	unittest.main()
