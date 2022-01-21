#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import mnpl_t
import mnpl

class Test(unittest.TestCase):

	def setUp(t):
		mnpl_t.setup()

	def tearDown(t):
		mnpl_t.teardown()

	def test_log_disabled(t):
		t.assertFalse(mnpl._log)
		mnpl.log('testing', '...')
		t.assertEqual(mnpl_t.log_string(), '')

	def test_log_enabled(t):
		mnpl._log = True
		mnpl.log('testing', '...')
		t.assertEqual(mnpl_t.log_string(), 'testing ...')

	def test_error_log(t):
		mnpl.error('testing', '...')
		t.assertEqual(mnpl_t.log_string(), '[E] testing ...')

if __name__ == '__main__':
	unittest.main()
