#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.
from contextlib    import contextmanager
from unittest.mock import MagicMock

import unittest
import uwscli_t

import uwscli
import custom_deploy

from uwscli_conf import CustomDeploy

@contextmanager
def mock_build_list(build_list = ['testing']):
	bup = uwscli.build_list
	try:
		uwscli.build_list = MagicMock(return_value = build_list)
		yield
	finally:
		uwscli.build_list = bup

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

	def test_config_check_build_list(t):
		with mock_build_list():
			c = _newcfg()
			c.check()
			uwscli.build_list.assert_called_once_with()

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
			uwscli.system.assert_called_once_with('/srv/home/uwscli/bin/app-deploy --wait --rollback testing 0.0.999')

	def test_main_config_check_error(t):
		c = _newcfg()
		c.app_env = ''
		t.assertEqual(custom_deploy.main(['0.0.999'], c), 10)

	def test_main_error(t):
		with uwscli_t.mock_system(status = 99):
			c = _newcfg()
			t.assertEqual(custom_deploy.main(['0.0.999'], c), 99)

	def test_main_show_builds(t):
		c = _newcfg()
		t.assertEqual(custom_deploy.main([], c), 0)

	def test_status(t):
		with uwscli_t.mock_system():
			c = _newcfg()
			t.assertEqual(custom_deploy.status([], c), 0)
			uwscli.system.assert_called_once_with('/srv/home/uwscli/bin/app-status testing')

	def test_status_config_check_error(t):
		c = _newcfg()
		c.app_name = ''
		t.assertEqual(custom_deploy.status([], c), 11)

if __name__ == '__main__':
	unittest.main()
