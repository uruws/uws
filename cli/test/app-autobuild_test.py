#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib import contextmanager
from os import linesep
from pathlib import Path

import unittest
from unittest.mock import MagicMock, call

import uwscli_t

import uwscli
import app_autobuild

@contextmanager
def mock():
	sleep_bup = app_autobuild.sleep
	try:
		app_autobuild.sleep = MagicMock()
		uwscli.app['testing'].autobuild = True
		with uwscli_t.mock_chdir():
			with uwscli_t.mock_mkdir():
				yield
	finally:
		app_autobuild.sleep = sleep_bup
		uwscli.app['testing'].autobuild = False

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
		with uwscli_t.mock_mkdir(fail = True):
			t.assertEqual(app_autobuild.main(['testing']), app_autobuild.ESETUP)
		t.setUp()
		# disabled
		with mock():
			uwscli.app['testing'].autobuild = False
			t.assertEqual(app_autobuild.main(['testing']), app_autobuild.EDISABLED)
			t.assertEqual(uwscli_t.err().strip(),
				'[ERROR] testing: autobuild is disabled')
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

	def test_main(t):
		# done already
		with mock():
			with mock_status(st = 'OK'):
				with uwscli_t.mock_check_output(output = '0.999.0'):
					with uwscli_t.mock_system():
						t.assertEqual(app_autobuild.main(['testing']), 0)
						calls = [
							call('git fetch --prune --prune-tags --tags'),
						]
						uwscli.system.assert_has_calls(calls)

	def test_main_deploy(t):
		with uwscli_t.mock_system():
			with uwscli_t.mock_list_images(['0.999.0']):
				uwscli.app['testing'].autobuild = True
				t.assertEqual(app_autobuild.main(['testing', '--deploy', '0.999.0']), 0)

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

	def test_dispatch(t):
		calls = [
			call('/srv/home/uwscli/bin/app-build testing 0.999.0'),
			call('/usr/bin/nq -c -- /srv/home/uwscli/bin/app-autobuild testing --deploy 0.999.0', env={'NQDIR': app_autobuild._nqdir})
		]
		with mock():
			with uwscli_t.mock_system():
				t.assertEqual(app_autobuild._dispatch('testing', '0.999.0'), 0)
				uwscli.system.assert_has_calls(calls)

	def test_dispatch_errors(t):
		with mock():
			with uwscli_t.mock_system(status = 99):
				t.assertEqual(app_autobuild._dispatch('testing', '0.999.0'),
					app_autobuild.EBUILD_RUN)
			with uwscli_t.mock_system(fail_cmd = '/usr/bin/nq'):
				t.assertEqual(app_autobuild._dispatch('testing', '0.999.0'),
					app_autobuild.EDEPLOY_NQ)

	def test_build(t):
		with mock():
			with uwscli_t.mock_system():
				with uwscli_t.mock_check_output(output = '0.999.0'):
					t.assertEqual(app_autobuild._build('testing'), 0)

	def test_build_error(t):
		with uwscli_t.mock_chdir(fail = True):
			t.assertEqual(app_autobuild._build('testing'), app_autobuild.EBUILD)

	def test_latestBuild(t):
		with uwscli_t.mock_list_images(['0.999.0', '0.0.999']):
			t.assertEqual(app_autobuild._latestBuild('testing'), '0.999.0')

	def test_deploy(t):
		with uwscli_t.mock_system():
			with uwscli_t.mock_list_images(['0.999.0']):
				t.assertEqual(app_autobuild._deploy('testing', '0.999.0'), 0)
			uwscli.system.assert_called_once_with('/srv/home/uwscli/bin/app-deploy testing 0.999.0')
		with uwscli_t.mock_system():
			with uwscli_t.mock_list_images(['0.999.0']):
				t.assertEqual(app_autobuild._deploy('testing', '1.999.0'), 0)
			uwscli.system.assert_not_called()

	def test_deploy_error(t):
		with uwscli_t.mock_system(status = 99):
			with uwscli_t.mock_list_images(['0.999.0']):
				t.assertEqual(app_autobuild._deploy('testing', '0.999.0'),
					app_autobuild.EDEPLOY)

if __name__ == '__main__':
	unittest.main()
