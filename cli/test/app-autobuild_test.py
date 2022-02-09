#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib import contextmanager
from os import linesep
from pathlib import Path

import unittest
from unittest.mock import MagicMock, call

import uwscli_t
import app_build_test

import uwscli
import app_autobuild

from uwscli_conf import App, AppDeploy

@contextmanager
def mock():
	try:
		uwscli.app['testing'].autobuild = True
		uwscli.app['testing'].autobuild_deploy = ['test-1']
		with uwscli_t.mock_chdir():
			with uwscli_t.mock_mkdir():
				yield
	finally:
		uwscli.app['testing'].autobuild = False
		uwscli.app['testing'].autobuild_deploy = []

@contextmanager
def mock_status(app = 'testing', st = 'FAIL', ver = '0.999.0', fail = False):
	gs_bup = app_autobuild._getStatus
	def __getStatus(app):
		raise FileNotFoundError('mock_error')
	Path(app_autobuild._status_dir).mkdir(mode = 0o750, exist_ok = True)
	f = Path(app_autobuild._status_dir, f"{app}.status")
	try:
		if fail:
			app_autobuild._getStatus = MagicMock(side_effect = __getStatus)
		f.write_text(f"{st}:{ver}{linesep}")
		yield f
	finally:
		if fail:
			app_autobuild._getStatus = gs_bup
		f.unlink()

@contextmanager
def mock_deploy(build = '0.999.0', status = 0):
	lb_bup = app_autobuild._latestBuild
	try:
		app_autobuild._latestBuild = MagicMock(return_value = build)
		uwscli.app['testing'].autobuild_deploy = ['test-1']
		uwscli.app['test-1'] = App(True,
			cluster = 'ktest',
			desc = 'Testing',
			pod = 'test',
			deploy = AppDeploy('test'),
		)
		with uwscli_t.mock_system(status = status):
			yield
	finally:
		app_autobuild._latestBuild = lb_bup
		uwscli.app['testing'].autobuild_deploy = []
		del uwscli.app['test-1']

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_globals(t):
		t.assertEqual(app_autobuild._status_dir, '/run/uwscli/build')
		t.assertEqual(app_autobuild._nqdir, '/run/uwscli/nq')

	def test_main_no_args(t):
		with t.assertRaises(SystemExit) as e:
			app_autobuild.main()
		err = e.exception
		t.assertEqual(err.args[0], 2)

	def test_invalid_app(t):
		with t.assertRaises(SystemExit) as e:
			app_autobuild.main(['noapp'])
		err = e.exception
		t.assertEqual(err.args[0], 2)

	def test_main_errors(t):
		# setup
		with mock():
			with uwscli_t.mock_mkdir(fail = True):
				t.assertEqual(app_autobuild.main(['testing']), app_autobuild.ESETUP)
		t.setUp()
		# chdir
		with uwscli_t.mock_mkdir():
			uwscli.app['testing'].autobuild = True
			t.assertEqual(app_autobuild.main(['testing']), app_autobuild.EBUILD)
			t.assertEqual(uwscli_t.err().strip(),
				'[ERROR] chdir not found: /srv/deploy/Testing')
		with mock():
			# git fetch
			with uwscli_t.mock_system(status = 99):
				t.assertEqual(app_autobuild.main(['testing']), 99)
			# latest tag
			with uwscli_t.mock_system():
				with uwscli_t.mock_check_output(output = 'Testing'):
					t.assertEqual(app_autobuild.main(['testing']), app_autobuild.ETAG)

	def test_main_steps(t):
		calls = [
			call('/usr/bin/sudo -H -n -u uws -- /srv/uws/deploy/cli/app-fetch.sh .', timeout=600),
			call('/usr/bin/sudo -H -n -u uws -- /srv/uws/deploy/cli/app-build.sh testing /srv/deploy/Testing build.sh 1.999.0', timeout=3600),
			call('/usr/bin/sudo -H -n -u uws -- /srv/uws/deploy/cli/uwsnq.sh uws /srv/uws/deploy/cli/app-clean-build.sh testing'),
			call('/usr/bin/sudo -H -n -u uws -- /srv/uws/deploy/cli/app-ctl.sh uws ktest test deploy 1.999.0-bp99', timeout=600),
		]
		with app_build_test.mock_run():
			with uwscli_t.mock_check_output(output = '1.999.0'):
				with mock_deploy(build = '1.999.0-bp99'):
					with mock():
						with uwscli_t.mock_list_images(['1.999.0-bp99']):
							t.assertEqual(app_autobuild.main(['testing']), 0)
							uwscli.system.assert_has_calls(calls)

	def test_main_done(t):
		calls = [
			call('/usr/bin/sudo -H -n -u uws -- /srv/uws/deploy/cli/app-fetch.sh .', timeout=600),
		]
		with mock():
			with mock_status(st = 'OK'):
				with uwscli_t.mock_check_output(output = '0.999.0'):
					with mock_deploy():
						t.assertEqual(app_autobuild.main(['testing']), 0)
						uwscli.system.assert_has_calls(calls)

	def test_latestTag(t):
		with uwscli_t.mock_check_output(output = linesep.join(['0.0.0', '0.1.0'])):
			t.assertEqual(app_autobuild._latestTag('src/test'), '0.1.0')

	def test_latestTag_errors(t):
		with uwscli_t.mock_check_output(output = linesep.join(['0.1.0', 'Testing', 't0', '0.0.0'])):
			t.assertEqual(app_autobuild._latestTag('src/test'), '0.1.0')
		with uwscli_t.mock_check_output(output = linesep.join(['Testing', 't0'])):
			with t.assertRaises(ValueError):
				app_autobuild._latestTag('src/test')

	def test_getStatus(t):
		with mock_status(st = 'OK'):
			st, ver = app_autobuild._getStatus('testing')
		t.assertEqual(st, 'OK')
		t.assertEqual(ver, '0.999.0')

	def test_getStatus_errors(t):
		with t.assertRaises(FileNotFoundError):
			app_autobuild._getStatus('testing')

	def test_checkVersion(t):
		t.assertFalse(app_autobuild._checkVersion('0.888.0', '0.999.0'))
		t.assertTrue(app_autobuild._checkVersion('0.999.0', '0.888.0'))

	def test_isBuildingOrDone(t):
		with mock_status(st = 'OK'):
			t.assertFalse(app_autobuild._isBuildingOrDone('testing', '1.999.0'))
			t.assertTrue(app_autobuild._isBuildingOrDone('testing', '0.888.0'))
		with mock_status(fail = True):
			t.assertFalse(app_autobuild._isBuildingOrDone('testing', '0.888.0'))

	def test_build(t):
		with mock():
			with uwscli_t.mock_system():
				with uwscli_t.mock_check_output(output = '0.999.0'):
					with app_build_test.mock_run():
						t.assertEqual(app_autobuild._build('testing'), (0, '0.999.0'))

	def test_build_error(t):
		with uwscli_t.mock_chdir(fail = True):
			t.assertEqual(app_autobuild._build('testing'), (app_autobuild.EBUILD, ''))

	def test_latestBuild(t):
		with uwscli_t.mock_list_images(['0.999.0', '0.0.999']):
			t.assertEqual(app_autobuild._latestBuild('testing'), '0.999.0')

	def test_latestBuild_error(t):
		with uwscli_t.mock_list_images([]):
			t.assertEqual(app_autobuild._latestBuild('testing'), '')
		with uwscli_t.mock_list_images(['220208']):
			t.assertEqual(app_autobuild._latestBuild('testing'), '')

	def test_deploy(t):
		with mock_deploy():
			with uwscli_t.mock_list_images(['0.999.0']):
				t.assertEqual(app_autobuild._deploy('testing', '0.999.0'), 0)
				uwscli.system.assert_called_once_with('/usr/bin/sudo -H -n -u uws -- /srv/uws/deploy/cli/app-ctl.sh uws ktest test deploy 0.999.0', timeout=600)
		with uwscli_t.mock_system():
			with uwscli_t.mock_list_images(['0.999.0']):
				t.assertEqual(app_autobuild._deploy('testing', '1.999.0'), 0)
			uwscli.system.assert_not_called()

	def test_deploy_error(t):
		# deploy error
		with mock_deploy(status = 99):
			with uwscli_t.mock_list_images(['0.999.0']):
				t.assertEqual(app_autobuild._deploy('testing', '0.999.0'),
					app_autobuild.EDEPLOY)
		# nothing to do
		with mock_deploy():
			t.assertEqual(app_autobuild._deploy('testing', '999.0.0'), 0)
			t.assertEqual(uwscli_t.out().strip().splitlines()[-1],
				'nothing to do for app: test-1 - ver: 0.999.0 - tag: 999.0.0')
		# no build
		with mock_deploy(build = ''):
			t.assertEqual(app_autobuild._deploy('testing', '0.666.0'), 0)
			t.assertEqual(uwscli_t.out().strip().splitlines()[-1],
				'no build to deploy for app: test-1')

	def test_deploy_buildpack(t):
		with uwscli_t.mock_list_images(['0.999.0']):
			with mock_deploy():
				t.assertEqual(app_autobuild._deploy('testing', '0.999.0'), 0)
				uwscli.system.assert_called_once_with('/usr/bin/sudo -H -n -u uws -- /srv/uws/deploy/cli/app-ctl.sh uws ktest test deploy 0.999.0', timeout=600)
				app_autobuild._latestBuild.assert_called_once_with('test-1')
		with uwscli_t.mock_list_images(['0.999.0-bp999']):
			with mock_deploy(build = '0.999.0-bp999'):
				t.assertEqual(app_autobuild._deploy('testing', '0.999.0'), 0)
				uwscli.system.assert_called_once_with('/usr/bin/sudo -H -n -u uws -- /srv/uws/deploy/cli/app-ctl.sh uws ktest test deploy 0.999.0-bp999', timeout=600)
				app_autobuild._latestBuild.assert_called_once_with('test-1')

if __name__ == '__main__':
	unittest.main()
