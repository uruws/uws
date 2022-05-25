#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib import contextmanager

import unittest
from unittest.mock import MagicMock

import uwscli_t
import uwscli_auth as auth
import uwscli_conf as conf
import uwscli

@contextmanager
def mock_noauth():
	bup = auth._check_app
	try:
		auth._check_app = MagicMock(return_value = auth.ECHECK)
		yield
	finally:
		auth._check_app = bup

@contextmanager
def mock_unauth_operator(group = 'testing'):
	try:
		auth.getstatusoutput = MagicMock(return_value = (0, group))
		yield
	finally:
		pass

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_user(t):
		u = auth.User('testing')
		t.assertEqual(u.name, 'testing')
		t.assertEqual(repr(u), 'testing')
		t.assertDictEqual(u.groups, {})

	def test_user_load_groups_errors(t):
		# user_auth
		u = auth.User(name = 'testing')
		u.load_groups = MagicMock(return_value = 99)
		t.assertListEqual(auth.user_auth(u, 'testing'), [])
		# user_check
		bup = auth.User
		try:
			auth.User = MagicMock()
			auth.User.load_groups = MagicMock(return_value = 99)
			t.assertEqual(auth.user_check('testing', '', '', ''), auth.EGROUPS)
		finally:
			auth.User = bup

	def test_user_root_admin(t):
		u = auth.User(name = 'root')
		t.assertFalse(u.is_admin)
		t.assertFalse(u.is_operator)
		with mock_unauth_operator():
			t.assertEqual(u.load_groups(), 0)
		t.assertTrue(u.is_admin)
		t.assertTrue(u.is_operator)

	def test_check_app(t):
		u = auth.User('testing')
		u.groups['testing'] = True
		t.assertEqual(auth._check_app(u, 'testing'), 0)

	def test_check_app_admin(t):
		u = auth.User('testing')
		u.is_admin = True
		t.assertEqual(auth._check_app(u, 'testing'), 0)

	def test_check_app_error(t):
		u = auth.User('testing')
		t.assertEqual(auth._check_app(u, 'testing'), auth.ECHECK)

	def test_check_app_operator(t):
		u = auth.User('testing')
		u.is_operator = True
		u.groups['testing'] = True
		t.assertEqual(auth._check_app(u, 'testing', ops = 'test'), 0)

	def test_user_auth(t):
		auth.getstatusoutput = MagicMock(return_value = (0, 'testing'))
		t.assertListEqual(auth.user_auth(auth.getuser(), ['testing']), ['testing'])

	def test_user_auth_no_apps(t):
		auth.getstatusoutput = MagicMock(return_value = (0, ''))
		t.assertListEqual(auth.user_auth(auth.getuser(), ['testing']), [])

	def test_user_auth_admin(t):
		t.assertListEqual(auth.user_auth(auth.getuser(), ['testing']), ['testing'])

	def test_user_auth_app_groups(t):
		uwscli.app['app0'] = uwscli.app['testing']
		uwscli.app['app0'].groups = ['testing', 'gtest']
		uwscli.app['app1'] = uwscli.app['testing']
		uwscli.app['app1'].groups = ['testing', 'gtest']
		auth.getstatusoutput = MagicMock(return_value = (0, 'gtest'))
		t.assertListEqual(auth.user_auth(auth.getuser(),
			['app0', 'app1']), ['app0', 'app1'])

	def test_check_pod(t):
		u = auth.User('testing')
		u.groups['testing'] = True
		t.assertEqual(auth._check_pod(u, 'test'), 0)

	def test_check_pod_error(t):
		u = auth.User('testing')
		t.assertEqual(auth._check_pod(u, 'test'), auth.EPOD)

	def test_check_workdir(t):
		u = auth.User('testing')
		u.groups['testing'] = True
		t.assertEqual(auth._check_workdir(u, '/srv/deploy/Testing'), 0)

	def test_check_workdir_error(t):
		u = auth.User('testing')
		u.groups['testing'] = True
		t.assertEqual(auth._check_workdir(u, 'test'), auth.EWKDIR)

	def test_check_workdir_buildpack(t):
		u = auth.User('testing')
		u.is_admin = True
		uwscli.app['testing'].build.type = 'pack'
		uwscli.app['testing'].build.src = 'app/src'
		t.assertEqual(auth._check_workdir(u, 'app/src'), 0)

	def test_user_check_args_error(t):
		t.assertEqual(auth.user_check('testing', '', '', ''), auth.EARGS)

	def test_user_check_build(t):
		t.assertEqual(auth.user_check('testing', 'testing', '', ''), 0)

	def test_user_check_build_error(t):
		with mock_noauth():
			t.assertEqual(auth.user_check('testing', 'testing', '', ''), auth.ECHECK)

	def test_user_check_build_operator(t):
		with mock_unauth_operator(group = 'uwsapp_testing'):
			t.assertEqual(auth.user_check('testing', 'testing', '', ''), 0)

	def test_user_check_pod(t):
		t.assertEqual(auth.user_check('testing', '', 'test', ''), 0)

	def test_user_check_pod_error(t):
		with mock_noauth():
			t.assertEqual(auth.user_check('testing', '', 'test', ''), auth.EPOD)

	def test_user_check_workdir(t):
		t.assertEqual(auth.user_check('testing', '', '', '/srv/deploy/Testing'), 0)

	def test_user_check_workdir_error(t):
		with mock_noauth():
			t.assertEqual(auth.user_check('testing', '', '', 'test'), auth.EWKDIR)

	def test_user_check_unauth_operation(t):
		with mock_unauth_operator():
			t.assertEqual(auth.user_check('testing', 'testing', '', '', 'test'), auth.EOPS)

	def test_user_check_operator_build_deploy(t):
		t.assertEqual(auth.user_check('testing', 'test', '', '', 'deploy'), 0)

if __name__ == '__main__':
	unittest.main()
