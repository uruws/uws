#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys
import unittest

import uwscli_t
import uwscli

sys.path.insert(0, '/srv/uws/deploy/cli')
import git_deploy

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
			t.assertEqual(git_deploy.main(['-r', 'testing.git', '-t', 'refs/tags/0.999']), 3)
		with uwscli_t.mock_chdir():
			with uwscli_t.mock_system(99):
				t.assertEqual(git_deploy.main(['-r', 'testing.git', '-t', 'refs/tags/0.999']), 4)
		with uwscli_t.mock_chdir(faildir = '/srv/test/repo'):
			with uwscli_t.mock_system():
				t.assertEqual(git_deploy.main(['-r', 'repo.git', '-t', 'refs/tags/0.999']), 5)

	def test_main(t):
		with uwscli_t.mock_chdir():
			with uwscli_t.mock_system():
				t.assertEqual(git_deploy.main(['-r', 'testing.git', '-t', 'refs/tags/0.999']), 0)

if __name__ == '__main__':
	unittest.main()
