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

	def test_globals(t):
		t.assertEqual(uwscli_deploy._cfgfn, '.uwsci.conf')
		t.assertListEqual(uwscli_deploy._cfgFiles, [])

	def test_newConfig(t):
		t.assertListEqual(uwscli_deploy._cfgFiles, [])
		c = uwscli_deploy._newConfig()
		t.assertListEqual(uwscli_deploy._cfgFiles, [])
		t.assertIsInstance(c, SectionProxy)
		t.assertIsNone(c.get('testing'))
		t.assertEqual(c.get('testing', 'test'), 'test')
		t.assertEqual(c.get('version', 'UNSET'), '0')

	def test_cfgFiles(t):
		try:
			uwscli_deploy._cfgfn = 'testdata/uwsci.conf'
			uwscli_deploy._newConfig()
			t.assertListEqual(uwscli_deploy._cfgFiles, ['testdata/uwsci.conf'])
		finally:
			uwscli_deploy._cfgfn = '.uwsci.conf'
			uwscli_deploy._cfgFiles = []

if __name__ == '__main__':
	unittest.main()
