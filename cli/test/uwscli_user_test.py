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

if __name__ == '__main__':
	unittest.main()
