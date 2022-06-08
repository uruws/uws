#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from unittest.mock import call

import unittest
import uwscli_t

import uwscli
import uwsapp_auth # type: ignore

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_fake(t):
		pass

if __name__ == '__main__':
	unittest.main()
