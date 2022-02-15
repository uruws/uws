#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock

import uwscli_t

import uwscli_auth as auth

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_load_groups_errors(t):
		# user_auth
		u = auth.User(name = 'testing')
		u.load_groups = MagicMock(return_value = 99)
		t.assertListEqual(auth.user_auth(u, 'testing'), [])
		# user_check
		bup = auth.User
		try:
			auth.User = MagicMock()
			auth.User.load_groups = MagicMock(return_value = 99)
			t.assertEqual(auth.user_check('testing', '', '', ''), auth.EGROUPS)
		finally:
			auth.User = bup

	def test_user_auth(t):
		t.assertListEqual(auth.user_auth(auth.getuser(), ['testing']), ['testing'])

if __name__ == '__main__':
	unittest.main()
