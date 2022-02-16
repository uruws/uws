#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib import contextmanager

import unittest
from unittest.mock import MagicMock

import uwscli_t
import uwscli_auth as auth

@contextmanager
def mock_noauth():
	bup = auth._check_app
	try:
		auth._check_app = MagicMock(return_value = auth.ECHECK)
		yield
	finally:
		auth._check_app = bup

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_user(t):
		u = auth.User('testing')
		t.assertEqual(u.name, 'testing')
		t.assertEqual(repr(u), 'testing')
		t.assertDictEqual(u.groups, {})

	def test_load_groups_errors(t):
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

	def test_user_auth(t):
		auth.getstatusoutput = MagicMock(return_value = (0, 'testing'))
		t.assertListEqual(auth.user_auth(auth.getuser(), ['testing']), ['testing'])

	def test_user_auth_no_apps(t):
		auth.getstatusoutput = MagicMock(return_value = (0, ''))
		t.assertListEqual(auth.user_auth(auth.getuser(), ['testing']), [])

	def test_user_auth_admin(t):
		t.assertListEqual(auth.user_auth(auth.getuser(), ['testing']), ['testing'])

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

	def test_user_check_args_error(t):
		t.assertEqual(auth.user_check('testing', '', '', ''), auth.EARGS)

	def test_user_check_build(t):
		t.assertEqual(auth.user_check('testing', 'testing', '', ''), 0)

	def test_user_check_build_error(t):
		with mock_noauth():
			t.assertEqual(auth.user_check('testing', 'testing', '', ''), auth.ECHECK)

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

if __name__ == '__main__':
	unittest.main()
