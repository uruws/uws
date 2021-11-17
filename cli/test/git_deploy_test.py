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

	def test_getDeployDir(t):
		t.assertEqual(git_deploy._getDeployDir('repo'), '/srv/deploy/repo')

	def test_main_errors(t):
		t.assertEqual(git_deploy.main(['-r', 'testing.git', '-t', 'invalid']),
			git_deploy.ETAGREF)
		t.assertEqual(git_deploy.main(['-r', 'invalid', '-t', 'refs/tags/0.999']),
			git_deploy.ERPATH)
		with uwscli_t.mock_chdir(faildir = '/srv/test'):
			with t.assertRaises(SystemExit) as e:
				git_deploy.main(['-r', 'testing.git', '-t', 'refs/tags/0.999'])
			err = e.exception
			t.assertEqual(err.args[0], git_deploy.ETESTDIR)
		with uwscli_t.mock_chdir():
			with uwscli_t.mock_system(status = 99):
				t.assertEqual(git_deploy.main(['-r', 'testing.git', '-t', 'refs/tags/0.999']),
					git_deploy.ETESTCLONE)
		with uwscli_t.mock_system():
			with uwscli_t.mock_chdir(faildir = '/srv/deploy'):
				with t.assertRaises(SystemExit) as e:
					git_deploy.main(['-r', 'testing.git', '-t', 'refs/tags/0.999'])
				err = e.exception
				t.assertEqual(err.args[0], git_deploy.EBASEDIR)
		# ~ with uwscli_t.mock_chdir():
			# ~ with uwscli_t.mock_system(fail_cmd = 'git clone testing.git'):
				# ~ t.assertEqual(git_deploy.main(['-r', 'testing.git', '-t', 'refs/tags/0.999']),
					# ~ git_deploy.ECLONE)
		with uwscli_t.mock_chdir(faildir = '/srv/test/repo'):
			with uwscli_t.mock_system():
				with t.assertRaises(SystemExit) as e:
					git_deploy.main(['-r', 'repo.git', '-t', 'refs/tags/0.999'])
				err = e.exception
				t.assertEqual(err.args[0], git_deploy.ERTEST_DIR)
			with uwscli_t.mock_system(fail_cmd = 'git fetch'):
				t.assertEqual(git_deploy.main(['-r', 'testing.git', '-t', 'refs/tags/0.999']),
					git_deploy.ERTEST_FETCH)
			with uwscli_t.mock_system(fail_cmd = 'git checkout'):
				t.assertEqual(git_deploy.main(['-r', 'testing.git', '-t', 'refs/tags/0.999']),
					git_deploy.ERTEST_CHECKOUT)

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
				# ~ t.assertEqual(uwscli.system.call_count, len(calls))
			calls = [
				uwscli_t.call('/srv/test', error_status = git_deploy.ETESTDIR),
				uwscli_t.call('/srv/deploy', error_status = git_deploy.EBASEDIR),
				uwscli_t.call('/srv/test/testing', error_status = 7),
			]
			uwscli.chdir.assert_has_calls(calls)
		t.assertEqual(environ.get('GIT_DIR', 'NONE'), '.')

if __name__ == '__main__':
	unittest.main()
