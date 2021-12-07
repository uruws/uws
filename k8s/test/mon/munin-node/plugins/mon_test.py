#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon

_bup_print = mon._print

class Test(unittest.TestCase):

	def setUp(t):
		mon._print = MagicMock()

	def tearDown(t):
		mon._print = None
		mon._print = _bup_print

	# logger

	def test_debug(t):
		t.assertFalse(mon.debug())
		try:
			mon._debug = True
			t.assertTrue(mon.debug())
		finally:
			mon._debug = False
		t.assertFalse(mon.debug())

	def test_print(t):
		_bup_print('testing')

	def test_log(t):
		mon.log('test', 'ing')
		mon._print.assert_called_once_with('test', 'ing')

	def test_dbg(t):
		mon.dbg('testing')
		mon._print.assert_not_called()
		try:
			mon._debug = True
			mon.dbg('test', 'ing')
			calls = [
				call('DEBUG: ', end = ''),
				call('test', 'ing'),
			]
			mon._print.assert_has_calls(calls)
		finally:
			mon._debug = False

	# utils

	def test_cleanfn(t):
		t.assertEqual(mon.cleanfn('testing'), 'testing')
		t.assertEqual(mon.cleanfn('test.ing'), 'test_ing')
		t.assertEqual(mon.cleanfn('_test.ing'), '_test_ing')
		t.assertEqual(mon.cleanfn('_test.in g'), '_test_in_g')
		t.assertEqual(mon.cleanfn('_te/st.in g'), '_te_st_in_g')

	def test_derive(t):
		t.assertEqual(mon.derive(0.0009), 1)
		t.assertEqual(mon.derive(0.009), 9)
		t.assertEqual(mon.derive(0.001), 1)
		t.assertEqual(mon.derive(1), 1000)
		t.assertEqual(mon.derive(1.3), 1300)
		t.assertEqual(mon.derive(1.7), 1700)
		t.assertEqual(mon.derive(1.9991), 2000)

	def test_cluster(t):
		t.assertIsNone(mon.cluster())

if __name__ == '__main__':
	unittest.main()
