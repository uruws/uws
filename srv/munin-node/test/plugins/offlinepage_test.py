#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import call

import mnpl_t
import mnpl_utils
import offlinepage

class Test(unittest.TestCase):

	def setUp(t):
		mnpl_t.setup()

	def tearDown(t):
		mnpl_t.teardown()

	def test_main_config(t):
		t.assertEqual(offlinepage.main(['config']), 0)
		calls = [
			call('graph_title offline page', 'http://localhost'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category', 'network'),
			call('graph_vlabel', 'app'),
			call('a_running.label running'),
			call('a_running.colour COLOUR0'),
			call('a_running.draw AREA'),
			call('a_running.min 0'),
			call('a_running.critical 1'),
			call('b_offline.label offline'),
			call('b_offline.colour COLOUR1'),
			call('b_offline.draw AREA'),
			call('b_offline.min 0'),
			call('b_offline.critical 1'),
			call('c_error.label error'),
			call('c_error.colour COLOUR2'),
			call('c_error.draw AREA'),
			call('c_error.min 0'),
			call('c_error.critical 1'),
		]
		mnpl_utils.println.assert_has_calls(calls)
		t.assertEqual(mnpl_utils.println.call_count, len(calls))

	def test_main_report(t):
		with mnpl_t.mock_utils_GET():
			t.assertEqual(offlinepage.main([]), 0)
		calls = [
			call('a_running.value U'),
			call('b_offline.value U'),
			call('c_error.value U'),
		]
		mnpl_utils.println.assert_has_calls(calls)
		t.assertEqual(mnpl_utils.println.call_count, len(calls))

	def test_main_report_timeout_error(t):
		with mnpl_t.mock_utils_GET(timeout_error = True):
			bup = offlinepage._timeout
			try:
				offlinepage._timeout = 'testing'
				t.assertEqual(offlinepage.main([]), 1)
			finally:
				offlinepage._timeout = bup
			mnpl_utils.GET.assert_called_once_with('http://localhost', timeout = 7, auth = True)
		calls = [
			call('a_running.value U'),
			call('b_offline.value U'),
			call('c_error.value U'),
		]
		mnpl_utils.println.assert_has_calls(calls)
		t.assertEqual(mnpl_utils.println.call_count, len(calls))

if __name__ == '__main__':
	unittest.main()
