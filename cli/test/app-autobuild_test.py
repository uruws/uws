#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib import contextmanager
from os import linesep

import unittest
from unittest.mock import call

import uwscli_t

import uwscli
import app_autobuild

@contextmanager
def mock():
	try:
		with uwscli_t.mock_chdir():
			with uwscli_t.mock_mkdir():
				yield
	finally:
		pass

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_globals(t):
		t.assertEqual(app_autobuild._status_dir, '/run/uwscli/build')

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
		with mock():
			with uwscli_t.mock_check_output(output = '0.999.0'):
				with uwscli_t.mock_system():
					t.assertEqual(app_autobuild.main(['testing']), 0)
					calls = [
						call('git fetch --prune --prune-tags --tags'),
						call('/srv/home/uwscli/bin/app-build testing 0.999.0'),
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

if __name__ == '__main__':
	unittest.main()
