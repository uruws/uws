#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import uwscli_t
import uwscli
import uwscli_log

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_log(t):
		uwscli.log('testing', '...', sep = '')
		t.assertEqual(uwscli_t.out().strip(), 'testing...')
		uwscli.log('testing', '...')
		t.assertEqual(uwscli_t.out().strip(), 'testing ...')

	def test_log_disable(t):
		with uwscli_t.log_disable():
			uwscli.log('testing3')
		t.assertEqual(uwscli_t.out().strip(), '')

	def test_info(t):
		uwscli.info('testing', '...')
		t.assertEqual(uwscli_t.out().strip(), 'testing ...')

	def test_debug(t):
		uwscli_log._debug = True
		uwscli.debug('testing', '...')
		t.assertTrue(uwscli_t.out().strip().endswith(': testing ...'))

	def test_error(t):
		uwscli.error('testing', '...')
		t.assertEqual(uwscli_t.err().strip(), 'testing ...')
		with uwscli_t.log_disable():
			# errors should print anyway
			uwscli.error('testing')
		t.assertEqual(uwscli_t.err().strip(), 'testing')

if __name__ == '__main__':
	unittest.main()
