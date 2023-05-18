#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
import uwscli_t

import app_build
import uwscli
import uwscli_conf

from contextlib import contextmanager
from unittest.mock import MagicMock, call

@contextmanager
def mock_check_storage(status = 0):
	cs_bup = app_build.check_storage
	try:
		app_build.check_storage = MagicMock(return_value = status)
		yield
	finally:
		app_build.check_storage = cs_bup

@contextmanager
def mock_run():
	try:
		with mock_check_storage():
			with uwscli_t.mock_system():
				yield
	finally:
		pass

@contextmanager
def mock_run_error(check_storage_status = 0, build_status = 0):
	_bup_check_storage = app_build.check_storage
	_bup_build = app_build._build
	try:
		with mock_check_storage():
			with uwscli_t.mock_system():
				app_build.check_storage = MagicMock(return_value = check_storage_status)
				app_build._build = MagicMock(return_value = build_status)
				yield
	finally:
		app_build.check_storage = _bup_check_storage
		app_build._build = _bup_build

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_check_storage(t):
		with uwscli_t.mock_gso(output = '100'):
			t.assertEqual(app_build.check_storage(), 0)
			uwscli.gso.assert_called_once_with("df -kl /srv/docker | tail -n1 | awk '{ print $4 }'")
		with uwscli_t.mock_gso(output = '3'):
			t.assertEqual(app_build.check_storage(), 8)

	def test_check_storage_error(t):
		with uwscli_t.mock_gso(output = 'testing'):
			t.assertEqual(app_build.check_storage(), 9)
		t.assertEqual(uwscli_t.err().strip(), 'value error: testing')
		with uwscli_t.mock_gso(status = 2, output = 'mock_error'):
			t.assertEqual(app_build.check_storage(), 2)
		t.assertEqual(uwscli_t.err().strip(), 'mock_error')

	def test_nq(t):
		with uwscli_t.mock_system():
			t.assertEqual(app_build.nq('testing', '0.999'), 0)
			t.assertEqual(uwscli.app['testing'].build.type, 'cli')
			try:
				uwscli.app['testing'].build.type = 'pack'
				t.assertEqual(app_build.nq('testing', '0.999'), 0)
			finally:
				uwscli.app['testing'].build.type = 'cli'

	def test_nq_errors(t):
		with uwscli_t.mock_system(status = 99):
			t.assertEqual(app_build.nq('testing', '0.999'), 99)

	def test_main_no_args(t):
		with t.assertRaises(SystemExit) as e:
			app_build.main()
		err = e.exception
		t.assertEqual(err.args[0], 2)

	def test_main_errors(t):
		t.assertEqual(app_build.main(['testing', '0.999']), 9)
		with mock_check_storage(status = 99):
			t.assertEqual(app_build.main(['testing', '0.999']), 99)
		with mock_check_storage():
			with uwscli_t.mock_system(status = 99):
				t.assertEqual(app_build.main(['testing', '0.999']), 99)

	def test_main(t):
		calls = [
			call('/usr/bin/sudo -H -n -u uws -- /srv/uws/deploy/cli/uwsnq.sh uws /srv/uws/deploy/cli/app-build.sh testing /srv/deploy/Testing build.sh 0.999',
				timeout = 600),
		]
		with mock_check_storage():
			with uwscli_t.mock_system():
				t.assertEqual(app_build.main(['testing', '0.999']), 0)
				uwscli.system.assert_has_calls(calls)
		with mock_check_storage():
			with uwscli_t.mock_system():
				try:
					uwscli.app['app'] = uwscli_conf.App(True,
						cluster = 'ktest',
						desc = 'App',
						pod = 'app',
						build = uwscli_conf.AppBuild('/srv/deploy/App', 'build.sh'),
						deploy = uwscli_conf.AppDeploy('app'),
						groups = ['app'],
					)
					t.assertEqual(app_build.main(['app', '0.999']), 0)
				finally:
					del uwscli.app['app']

	def test_run(t):
		calls = [
			call('/usr/bin/sudo -H -n -u uws -- /srv/uws/deploy/cli/app-build.sh testing /srv/deploy/Testing build.sh 0.999', timeout = 3600),
		]
		with mock_run():
			t.assertEqual(app_build.run('testing', '0.999'), 0)
			uwscli.system.assert_has_calls(calls)

	def test_run_pack(t):
		calls = [
			call('/usr/bin/sudo -H -n -u uws -- /srv/uws/deploy/cli/buildpack.sh /srv/deploy/App app 0.999', timeout = 3600),
		]
		with mock_run():
			try:
				uwscli.app['app'] = uwscli_conf.App(True,
					cluster = 'ktest',
					desc = 'App',
					pod = 'app',
					build = uwscli_conf._buildpack('/srv/deploy/App', 'app'),
					deploy = uwscli_conf.AppDeploy('app'),
				)
				t.assertEqual(app_build.run('app', '0.999'), 0)
				uwscli.system.assert_has_calls(calls)
			finally:
				del uwscli.app['app']

	def test_run_errors(t):
		with mock_run_error(check_storage_status = 99):
			t.assertEqual(app_build.run('testing', '0.999'), 99)
		with mock_run_error(build_status = 99):
			t.assertEqual(app_build.run('testing', '0.999'), 99)

	def test_version_blacklist(t):
		with mock_check_storage():
			t.assertEqual(app_build.main(['testing', '2.98.8']), 9)

if __name__ == '__main__':
	unittest.main()
