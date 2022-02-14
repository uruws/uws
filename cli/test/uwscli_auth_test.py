#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import uwscli_t

import uwscli_auth as auth

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_user_auth(t):
		t.assertListEqual(auth.user_auth(auth.getuser(), ['testing']), ['testing'])

if __name__ == '__main__':
	unittest.main()
