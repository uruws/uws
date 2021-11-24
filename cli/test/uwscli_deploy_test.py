#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from configparser import ConfigParser

import unittest

import uwscli_t
import uwscli_deploy

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_newConfig(t):
		c = uwscli_deploy._newConfig()
		t.assertIsInstance(c, ConfigParser)

if __name__ == '__main__':
	unittest.main()
