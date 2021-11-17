#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys
import unittest

import uwscli_t
import uwscli

sys.path.insert(0, '/srv/uws/deploy/cli')
import git_deploy

from os import environ

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_main_no_args(t):
		with t.assertRaises(SystemExit):
			git_deploy.main()
		with t.assertRaises(SystemExit):
			git_deploy.main(['-r', 'testing'])
		with t.assertRaises(SystemExit):
			git_deploy.main(['-t', 'testing'])

	def test_getTag(t):
		t.assertEqual(git_deploy._getTag('refs/tags/test/0.999'), 'test/0.999')

	def test_getRepo(t):
		t.assertEqual(git_deploy._getRepo('/testing/path/repo.git'), 'repo')

	def test_getTestDir(t):
		t.assertEqual(git_deploy._getTestDir('repo'), '/srv/test/repo')

	def test_main_errors(t):
		t.assertEqual(git_deploy.main(['-r', 'testing.git', '-t', 'invalid']), 1)
		t.assertEqual(git_deploy.main(['-r', 'invalid', '-t', 'refs/tags/0.999']), 2)
		with uwscli_t.mock_chdir(faildir = '/srv/test'):
			with t.assertRaises(SystemExit) as e:
				git_deploy.main(['-r', 'testing.git', '-t', 'refs/tags/0.999'])
			err = e.exception
			t.assertEqual(err.args[0], 3)
		with uwscli_t.mock_chdir():
			with uwscli_t.mock_system(status = 99):
				t.assertEqual(git_deploy.main(['-r', 'testing.git', '-t', 'refs/tags/0.999']), 4)
		with uwscli_t.mock_chdir(faildir = '/srv/test/repo'):
			with uwscli_t.mock_system():
				with t.assertRaises(SystemExit) as e:
					git_deploy.main(['-r', 'repo.git', '-t', 'refs/tags/0.999'])
				err = e.exception
				t.assertEqual(err.args[0], 5)
			with uwscli_t.mock_system(fail_cmd = 'git fetch'):
				t.assertEqual(git_deploy.main(['-r', 'testing.git', '-t', 'refs/tags/0.999']), 6)
			with uwscli_t.mock_system(fail_cmd = 'git checkout'):
				t.assertEqual(git_deploy.main(['-r', 'testing.git', '-t', 'refs/tags/0.999']), 7)

	def test_main(t):
		t.assertEqual(environ.get('GIT_DIR', 'NONE'), 'NONE')
		with uwscli_t.mock_chdir():
			with uwscli_t.mock_system():
				t.assertEqual(git_deploy.main(['-r', 'testing.git', '-t', 'refs/tags/0.999']), 0)
				calls = [
					uwscli_t.call('git clone testing.git'),
					uwscli_t.call('git fetch --prune --prune-tags --tags'),
					uwscli_t.call('git checkout 0.999'),
				]
				uwscli.system.assert_has_calls(calls)
				t.assertEqual(uwscli.system.call_count, len(calls))
		t.assertEqual(environ.get('GIT_DIR', 'NONE'), '.')

if __name__ == '__main__':
	unittest.main()
