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

if __name__ == '__main__':
	unittest.main()
