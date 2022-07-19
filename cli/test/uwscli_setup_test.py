#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from unittest.mock import call

import unittest
import uwscli_t

import uwscli
import uwscli_setup # type: ignore

_env = {'PATH': '/bin:/usr/bin:/sbin:/usr/sbin'}

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_main(t):
		uwscli.app['testing'].build.repo = 'testing.git'
		calls = [
			call('/srv/home/uwscli/sbin/uwscli_setup.sh', env = _env),
			call('/srv/home/uwscli/sbin/uwscli_app.sh app testing', env = _env),
			call('/srv/home/uwscli/sbin/uwsapp_auth.py', env = _env),
			call('/srv/home/uwscli/sbin/buildpack_setup.sh /srv/deploy/Buildpack git@github.com:TalkingPts/Buildpack.git', env = _env),
			call('/srv/home/uwscli/sbin/app_repo.sh testing.git /srv/deploy/Testing', env = _env),
		]
		with uwscli_t.mock_system():
			t.assertEqual(uwscli_setup.main(), 0)
			uwscli.system.assert_has_calls(calls)
			t.assertEqual(uwscli.system.call_count, len(calls))

	def test_main_error(t):
		calls = [
			call('/srv/home/uwscli/sbin/uwscli_setup.sh', env = _env),
		]
		with uwscli_t.mock_system(status = 99):
			t.assertEqual(uwscli_setup.main(), 99)
			uwscli.system.assert_has_calls(calls)
			t.assertEqual(uwscli.system.call_count, len(calls))

	def test_users(t):
		calls = [
			call('/srv/home/uwscli/sbin/uwscli_setup.sh', env = _env),
			call('/srv/home/uwscli/sbin/uwscli_app.sh app testing', env = _env),
			call('/srv/home/uwscli/sbin/uwscli_user.sh /home 5000 tuser', env = _env),
			call('/srv/home/uwscli/sbin/uwscli_user_groups.sh tuser tapp tapp1', env = _env),
			call('/srv/home/uwscli/sbin/uwscli_user_authkeys.sh /home tuser t.key', env = _env),
			call('/srv/home/uwscli/sbin/uwscli_admin.sh tuser', env = _env),
			call('/srv/home/uwscli/sbin/uwscli_operator.sh tuser', env = _env),
			call('/srv/home/uwscli/sbin/uwsapp_auth.py', env = _env),
			call('/srv/home/uwscli/sbin/buildpack_setup.sh /srv/deploy/Buildpack git@github.com:TalkingPts/Buildpack.git', env = _env),
		]
		with uwscli_t.mock_users():
			with uwscli_t.mock_system():
				t.assertEqual(uwscli_setup.main(), 0)
				uwscli.system.assert_has_calls(calls)
				t.assertEqual(uwscli.system.call_count, len(calls))

	def test_users_remove(t):
		calls = [
			call('/srv/home/uwscli/sbin/uwscli_setup.sh', env = _env),
			call('/srv/home/uwscli/sbin/uwscli_app.sh app testing', env = _env),
			call('/srv/home/uwscli/sbin/uwsapp_auth.py', env = _env),
			call('/srv/home/uwscli/sbin/uwscli_user_remove.sh tuser', env = _env),
			call('/srv/home/uwscli/sbin/buildpack_setup.sh /srv/deploy/Buildpack git@github.com:TalkingPts/Buildpack.git', env = _env),
		]
		with uwscli_t.mock_users_remove():
			with uwscli_t.mock_system():
				t.assertEqual(uwscli_setup.main(), 0)
				uwscli.system.assert_has_calls(calls)
				t.assertEqual(uwscli.system.call_count, len(calls))

	def test_run(t):
		calls = [
			call('/srv/home/uwscli/sbin/testing.sh', env = _env),
		]
		with uwscli_t.mock_system():
			uwscli_setup._run('testing.sh')
			uwscli.system.assert_has_calls(calls)
			t.assertEqual(uwscli.system.call_count, len(calls))

	def test_run_error(t):
		calls = [
			call('/srv/home/uwscli/sbin/testing.sh', env = _env),
		]
		with uwscli_t.mock_system(status = 99):
			with t.assertRaises(uwscli_setup._cmdFailed):
				uwscli_setup._run('testing.sh')
			uwscli.system.assert_has_calls(calls)
			t.assertEqual(uwscli.system.call_count, len(calls))

if __name__ == '__main__':
	unittest.main()
