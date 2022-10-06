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
			call('a_running.draw AREASTACK'),
			call('a_running.min 0'),
			call('a_running.max 5'),
			call('a_running.critical 2:4'),
			call('b_offline.label offline'),
			call('b_offline.colour COLOUR1'),
			call('b_offline.draw AREASTACK'),
			call('b_offline.min 0'),
			call('b_offline.max 5'),
			call('b_offline.critical 2:4'),
			call('c_error.label error'),
			call('c_error.colour COLOUR2'),
			call('c_error.draw AREASTACK'),
			call('c_error.min 0'),
			call('c_error.max 5'),
			call('c_error.critical 2:4'),
			call('d_size.label size'),
			call('d_size.colour COLOUR3'),
			call('d_size.draw AREASTACK'),
			call('d_size.min 0'),
			call('d_size.max 5'),
			call('d_size.critical 2:4'),
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
			call('d_size.value U'),
		]
		mnpl_utils.println.assert_has_calls(calls)
		t.assertEqual(mnpl_utils.println.call_count, len(calls))

	def test_main_report_error(t):
		with mnpl_t.mock_utils_GET(code = 599):
			t.assertEqual(offlinepage.main([]), 0)
		calls = [
			call('a_running.value', '1.0'),
			call('b_offline.value', '3.0'),
			call('c_error.value', '1.0'),
			call('d_size.value', '1.0'),
		]
		mnpl_utils.println.assert_has_calls(calls)
		t.assertEqual(mnpl_utils.println.call_count, len(calls))

	def test_main_report_size_error(t):
		with mnpl_t.mock_utils_GET(body = '\n'):
			t.assertEqual(offlinepage.main([]), 0)
		calls = [
			call('a_running.value', '1.0'),
			call('b_offline.value', '3.0'),
			call('c_error.value', '3.0'),
			call('d_size.value', '1.0'),
		]
		mnpl_utils.println.assert_has_calls(calls)
		t.assertEqual(mnpl_utils.println.call_count, len(calls))

	def test_main_report(t):
		bup_size_min = offlinepage._size_min
		bup_app_check = offlinepage._app_check
		try:
			offlinepage._size_min = 7
			offlinepage._app_check = 'testing'
			with mnpl_t.mock_utils_GET(body = 'testing\n') as resp:
				t.assertEqual(offlinepage.main([]), 0)
				resp.__enter__.assert_called_once()
				resp.readlines.assert_called_once()
				resp.__exit__.assert_called_once()
		finally:
			offlinepage._size_min = bup_size_min
			offlinepage._app_check = bup_app_check
		calls = [
			call('a_running.value', '3.0'),
			call('b_offline.value', '3.0'),
			call('c_error.value', '3.0'),
			call('d_size.value', '3.0'),
		]
		mnpl_utils.println.assert_has_calls(calls)
		t.assertEqual(mnpl_utils.println.call_count, len(calls))

	def test_main_report_offline(t):
		bup_size_min = offlinepage._size_min
		bup_offline_check = offlinepage._offline_check
		try:
			offlinepage._size_min = 7
			offlinepage._offline_check = 'testing'
			with mnpl_t.mock_utils_GET(body = 'testing\n'):
				t.assertEqual(offlinepage.main([]), 0)
		finally:
			offlinepage._size_min = bup_size_min
			offlinepage._offline_check = bup_offline_check
		calls = [
			call('a_running.value', '1.0'),
			call('b_offline.value', '1.0'),
			call('c_error.value', '3.0'),
			call('d_size.value', '3.0'),
		]
		mnpl_utils.println.assert_has_calls(calls)
		t.assertEqual(mnpl_utils.println.call_count, len(calls))

if __name__ == '__main__':
	unittest.main()
