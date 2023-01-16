#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from unittest.mock import MagicMock

from contextlib import contextmanager

import unittest
import uwscli_t

import uwscli
import app_deploy
import custom_deploy

@contextmanager
def mock_wait(status = 0):
	_bup = app_deploy.wait
	try:
		app_deploy.wait = MagicMock(return_value = status)
		yield
	finally:
		app_deploy.wait = _bup

@contextmanager
def mock_rollback(status = 0):
	_bup = custom_deploy.rollback
	try:
		custom_deploy.rollback = MagicMock(return_value = status)
		yield
	finally:
		custom_deploy.rollback = _bup

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_deploy_error(t):
		with uwscli_t.mock_system(status = 99):
			with uwscli_t.mock_list_images(['0.999']):
				t.assertEqual(app_deploy.deploy('testing', '0.999'), 99)

	def test_deploy(t):
		with uwscli_t.mock_system():
			with uwscli_t.mock_list_images(['0.999']):
				t.assertEqual(app_deploy.deploy('testing', '0.999'), 0)

	def test_main_no_args(t):
		with t.assertRaises(SystemExit) as e:
			app_deploy.main()
		err = e.exception
		t.assertEqual(err.args[0], 2)

	def test_main(t):
		with uwscli_t.mock_list_images():
			t.assertEqual(app_deploy.main(['testing']), 0)
			t.assertEqual(uwscli_t.out().strip(), 'no available builds for testing')
		with uwscli_t.mock_list_images(['img-1']):
			t.assertEqual(app_deploy.main(['testing']), 0)
			t.assertEqual(uwscli_t.out().strip(), 'available testing builds:\n  img-1')
		with uwscli_t.mock_list_images(['0.999']):
			with uwscli_t.mock_system():
				t.assertEqual(app_deploy.main(['testing', '0.999']), 0)
				uwscli.system.assert_called_once_with('/usr/bin/sudo -H -n -u uws -- /srv/uws/deploy/cli/app-ctl.sh uws ktest test deploy 0.999',
					timeout = uwscli.system_ttl)

	def test_main_errors(t):
		with uwscli_t.mock_system(status = 99):
			with uwscli_t.mock_list_images(['0.999']):
				t.assertEqual(app_deploy.deploy('testing', '0.999'), 99)
		with uwscli_t.mock_list_images():
			t.assertEqual(app_deploy.main(['testing', '0.999']), 9)
		with uwscli_t.mock_list_images(['0.999']):
			with uwscli_t.mock_system(status = 99):
				t.assertEqual(app_deploy.main(['testing', '0.999']), 99)

	def test_wait(t):
		with uwscli_t.mock_system():
			with uwscli_t.mock_list_images(['0.999']):
				t.assertEqual(app_deploy.wait('testing'), 0)
			uwscli.system.assert_called_once_with('/usr/bin/sudo -H -n -u uws -- /srv/uws/deploy/cli/app-ctl.sh uws ktest test wait', timeout = uwscli.system_ttl)

	def test_main_wait(t):
		with uwscli_t.mock_system():
			with uwscli_t.mock_list_images(['0.999']):
				t.assertEqual(app_deploy.main(['--wait', 'testing', '0.999']), 0)

	def test_main_rollback(t):
		with uwscli_t.mock_system():
			with uwscli_t.mock_list_images(['0.999']):
				with mock_wait(status = 99):
					t.assertEqual(app_deploy.main(['--rollback', 'testing', '0.999']), 99)

	def test_main_rollback_error(t):
		with uwscli_t.mock_system():
			with uwscli_t.mock_list_images(['0.999']):
				with mock_wait(status = 99):
					with mock_rollback(status = 9):
						t.assertEqual(app_deploy.main(['--rollback', 'testing', '0.999']), 99)

if __name__ == '__main__':
	unittest.main()
