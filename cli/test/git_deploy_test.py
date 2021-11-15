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

if __name__ == '__main__':
	unittest.main()
