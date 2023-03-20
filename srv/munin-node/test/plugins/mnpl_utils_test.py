#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import mnpl_t
import mnpl_utils

class Test(unittest.TestCase):

	def setUp(t):
		mnpl_t.setup()

	def tearDown(t):
		mnpl_t.teardown()

	def test_log_disabled(t):
		t.assertFalse(mnpl_utils._log)
		mnpl_utils.log('testing', '...')
		t.assertEqual(mnpl_t.log_string(), '')

	def test_log_enabled(t):
		mnpl_utils._log = True
		mnpl_utils.log('testing', '...')
		t.assertEqual(mnpl_t.log_string(), 'testing ...')

	def test_error_log(t):
		mnpl_utils.error('testing', '...')
		t.assertEqual(mnpl_t.log_string(), '[E] testing ...')

	def test_cleanfn(t):
		t.assertEqual(mnpl_utils.cleanfn('k8s-test'), 'k8s_test')

	def test_println(t):
		mnpl_t.bup_println('testing', '...')

if __name__ == '__main__':
	unittest.main()
