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
		with uwscli_t.mock_chdir():
			with uwscli_t.mock_mkdir():
				yield
	finally:
		app_autobuild.sleep = sleep_bup

@contextmanager
def mock_status(app = 'testing', st = 'FAIL', ver = '0.999.0'):
	Path(app_autobuild._status_dir).mkdir(mode = 0o750, exist_ok = True)
	f = Path(app_autobuild._status_dir, f"{app}.status")
	try:
		f.write_text(f"{st}:{ver}{linesep}")
		yield f
	finally:
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
		# chdir
		with uwscli_t.mock_mkdir():
			with t.assertRaises(SystemExit) as e:
				app_autobuild.main(['testing'])
			err = e.exception
			t.assertEqual(err.args[0], 2)
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

	def test_latestTag_errors(t):
		with uwscli_t.mock_check_output(output = linesep.join(['0.1.0', 'Testing', 't0', '0.0.0'])):
			t.assertEqual(app_autobuild._latestTag('src/test'), '0.1.0')
		with uwscli_t.mock_check_output(output = linesep.join(['Testing', 't0'])):
			with t.assertRaises(ValueError):
				app_autobuild._latestTag('src/test')

	def test_latestTag(t):
		with uwscli_t.mock_check_output(output = linesep.join(['0.0.0', '0.1.0'])):
			t.assertEqual(app_autobuild._latestTag('src/test'), '0.1.0')

	def test_getStatus_errors(t):
		with t.assertRaises(FileNotFoundError):
			app_autobuild._getStatus('testing')

	def test_getStatus(t):
		with mock_status(st = 'OK'):
			st, ver = app_autobuild._getStatus('testing')
		t.assertEqual(st, 'OK')
		t.assertEqual(ver, '0.999.0')

if __name__ == '__main__':
	unittest.main()
