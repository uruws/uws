#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
import uwscli_t

import app_autobuild

class Test(unittest.TestCase):

	def test_main_no_args(t):
		with t.assertRaises(SystemExit) as e:
			app_autobuild.main()
		err = e.exception
		t.assertEqual(err.args[0], 2)

	def test_main(t):
		with t.assertRaises(FileNotFoundError):
			app_autobuild.main(['testing'])

if __name__ == '__main__':
	unittest.main()
