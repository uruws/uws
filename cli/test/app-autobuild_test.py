#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
import uwscli_t

import uwscli
import app_autobuild

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_lastTag(t):
		with uwscli_t.mock_gso():
			rc, out = app_autobuild.lastTag('testing')
			t.assertEqual(rc, 0)
			t.assertEqual(out, 'mock_output')
			uwscli.gso.assert_called_once_with('git -C . describe --abbrev=0 --tags origin/HEAD')

	def test_main_no_args(t):
		with t.assertRaises(SystemExit) as e:
			app_autobuild.main()
		err = e.exception
		t.assertEqual(err.args[0], 2)

	def test_main_errors(t):
		t.assertEqual(app_autobuild.main(['testing']), 9)
		t.assertEqual(uwscli_t.err().strip(),
			'[ERROR] app build dir not found: /srv/deploy/Testing')

if __name__ == '__main__':
	unittest.main()
