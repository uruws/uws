#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
import uwscli_t

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_fake(t):
		pass

if __name__ == '__main__':
	unittest.main()
