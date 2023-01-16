#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
import uwscli_t

import uwscli
import custom_deploy

from uwscli_conf import CustomDeploy

def _newcfg():
	return custom_deploy.Config(app_name = 'testing', app_env = 'test')

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_config(t):
		c = _newcfg()
		t.assertTrue(c.check())
		t.assertEqual(c.app_name, 'testing')
		t.assertEqual(c.app_env, 'test')

	def test_config_check_error(t):
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
		# app_env: invalid
		with t.assertRaises(RuntimeError):
			c = _newcfg()
			c.app_env = 'invalid_app_env'
			c.check()

	def test_rollback(t):
		with uwscli_t.mock_system():
			t.assertEqual(custom_deploy.rollback('testing'), 0)
			uwscli.system.assert_called_once_with('/usr/bin/sudo -H -n -u uws -- /srv/uws/deploy/cli/app-ctl.sh uws ktest test rollback', timeout = uwscli.system_ttl)

	def test_rollback_list(t):
		with uwscli_t.mock_system():
			custom_deploy._do_rollback([CustomDeploy('testing')])
			uwscli.system.assert_called_once_with('/usr/bin/sudo -H -n -u uws -- /srv/uws/deploy/cli/app-ctl.sh uws ktest test rollback', timeout = uwscli.system_ttl)

	def test_main(t):
		with uwscli_t.mock_system():
			c = _newcfg()
			t.assertEqual(custom_deploy.main(['0.0.999'], c), 0)

	def test_main_config_check_error(t):
		c = _newcfg()
		c.app_env = ''
		t.assertEqual(custom_deploy.main(['0.0.999'], c), 9)

	def test_main_error(t):
		with uwscli_t.mock_system(status = 99):
			c = _newcfg()
			t.assertEqual(custom_deploy.main(['0.0.999'], c), 99)

if __name__ == '__main__':
	unittest.main()
