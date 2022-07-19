#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
import uwscli_t

import uwscli
import uwscli_user

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_defaults(t):
		t.assertDictEqual(uwscli_user.user, {})

	def test_mock_user(t):
		with uwscli_t.mock_users():
			t.assertDictEqual(uwscli_user.user, {
				'tuser': uwscli_user.AppUser(5000,
					name = 'tuser',
					groups = ['tapp', 'tapp1'],
					is_admin = True,
					is_operator = True,
					keyid = 't.key',
					remove = False,
				)
			})

if __name__ == '__main__':
	unittest.main()
