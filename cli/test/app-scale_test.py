#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
import uwscli_t

import app_scale

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_main_no_args(t):
		with t.assertRaises(SystemExit) as e:
			app_scale.main()
		err = e.exception
		t.assertEqual(err.args[0], 2)

	def test_main(t):
		t.assertEqual(app_scale.main(['testing', '999']), 127)

if __name__ == '__main__':
	unittest.main()
