#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
import uwscli_t

import custom_deploy

def _newcfg():
	return custom_deploy.Config('testing_app', app_name = 'tapp', app_env = 'tenv')

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

if __name__ == '__main__':
	unittest.main()
