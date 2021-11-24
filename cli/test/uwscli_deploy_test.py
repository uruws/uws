#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from configparser import SectionProxy

import unittest

import uwscli_t
import uwscli_deploy

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_newConfig(t):
		c = uwscli_deploy._newConfig()
		t.assertIsInstance(c, SectionProxy)
		t.assertIsNone(c.get('testing'))
		t.assertEqual(c.get('testing', 'test'), 'test')
		t.assertEqual(c.get('version', 'UNSET'), '0')

if __name__ == '__main__':
	unittest.main()
