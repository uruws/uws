#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys
import unittest

import uwscli_t

sys.path.insert(0, '/srv/uws/deploy/cli')
import uwspass

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_args_error(t):
		t.assertEqual(uwspass.main(['--user', 'invalid']), 8)

if __name__ == '__main__':
	unittest.main()
