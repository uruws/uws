#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

from contextlib import contextmanager
from email.headerregistry import Address

import alerts

@contextmanager
def mock(fileinput = []):
	fi_bup = alerts.fileinput
	sys_bup = alerts.sys
	try:
		# fileinput
		alerts.fileinput = MagicMock()
		alerts.fileinput.input = MagicMock(return_value = fileinput)
		# sys
		alerts.sys = MagicMock()
		alerts.sys.stderr = MagicMock()
		yield
	finally:
		alerts.fileinput = fi_bup
		alerts.sys = sys_bup

class Test(unittest.TestCase):

	def test_globals(t):
		t.assertEqual(alerts.QDIR, '/var/opt/munin-alert')
		t.assertEqual(alerts.MAILTO,
			Address('munin alert', 'munin-alert', 'uws.talkingpts.org'))

	def test_msgNew(t):
		m = alerts._msgNew()
		t.assertEqual(m.get_charset(), 'utf-8')
		t.assertTrue(m.get('Date', '') != '')
		t.assertTrue(m.get('Message-ID', '') != '')

	def test_getTitle(t):
		t.assertEqual(alerts._getTitle({}), 'NO_TITLE')
		t.assertEqual(alerts._getTitle({'title': 'testing'}), 'testing')
		t.assertEqual(alerts._getTitle({'title': 'testing :: item1 :: item2'}),
			'item2')

	def test_stateChanged(t):
		t.assertFalse(alerts._stateChanged({}))
		t.assertFalse(alerts._stateChanged({'state_changed': '0'}))
		t.assertTrue(alerts._stateChanged({'state_changed': '1'}))

	def test_msgFrom(t):
		t.assertEqual(alerts._msgFrom({'host': 'testing'}),
			Address('testing', 'munin-alert', 'testing'))

	def test_msgSubject(t):
		t.assertEqual(alerts._msgSubject({}), '[ERROR] NO_TITLE')
		t.assertEqual(alerts._msgSubject(
			{'worst': 'TEST', 'title': 'test', 'state_changed': '1'}),
			'[TEST] test')
		t.assertEqual(alerts._msgSubject({'worst': 'TEST', 'title': 'test'}),
			'TEST: test')

	def test_sleepingHours(t):
		alerts._sleepingHours()
		check = dict()
		for h in range(0, 25):
			check[h] = alerts._sleepingHours(h)
		t.assertDictEqual(check, {
			0: False,
			1: True,
			2: True,
			3: True,
			4: True,
			5: True,
			6: True,
			7: True,
			8: True,
			9: True,
			10: True,
			11: False,
			12: False,
			13: False,
			14: False,
			15: False,
			16: False,
			17: False,
			18: False,
			19: False,
			20: False,
			21: False,
			22: False,
			23: False,
			24: False,
		})

	def test_main_errors(t):
		with mock(fileinput = ['invalid']):
			t.assertEqual(alerts.main(), 0)
			alerts.sys.stderr.write.assert_has_calls([call('ERROR:')])

	def test_main(t):
		with mock():
			t.assertEqual(alerts.main(), 0)
			alerts.fileinput.input.assert_called_once_with('-')

if __name__ == '__main__':
	unittest.main()
