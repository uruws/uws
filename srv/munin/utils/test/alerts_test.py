#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import os

import unittest
from unittest.mock import MagicMock, call

from contextlib import contextmanager
from email.headerregistry import Address
from email.message import EmailMessage
from io import StringIO, BytesIO
from time import localtime
from time import tzset

import alerts

@contextmanager
def mock(fileinput = [], ctrl_c = False):
	def __ctrl_c(*args):
		raise KeyboardInterrupt
	fi_bup = alerts.fileinput
	sys_bup = alerts.sys
	try:
		# fileinput
		alerts.fileinput = MagicMock()
		if ctrl_c:
			alerts.fileinput.input = MagicMock(side_effect = __ctrl_c)
		else:
			alerts.fileinput.input = MagicMock(return_value = fileinput)
		# sys
		alerts.sys = MagicMock()
		alerts.sys.stderr = MagicMock()
		yield
	finally:
		alerts.fileinput = fi_bup
		alerts.sys = sys_bup

@contextmanager
def mock_nq(status = 0):
	nq_bup = alerts.nq
	try:
		alerts.nq = MagicMock(return_value = status)
		yield
	finally:
		alerts.nq = nq_bup

@contextmanager
def mock_sleepingHours(state = True):
	sh_bup = alerts._sleepingHours
	try:
		alerts._sleepingHours = MagicMock(return_value = state)
		yield
	finally:
		alerts._sleepingHours = sh_bup

@contextmanager
def mock_parse():
	p_bup = alerts.parse
	r_bup = alerts.report
	try:
		alerts.parse = MagicMock(return_value = 'mock_parse')
		alerts.report = MagicMock(return_value = 'mock_report')
		yield
	finally:
		alerts.parse = p_bup
		alerts.report = r_bup

@contextmanager
def mock_open(fh = BytesIO()):
	_bup_open = alerts._open
	def _open(fn, mode):
		return fh
	try:
		alerts._open = MagicMock(side_effect = _open)
		yield
	finally:
		alerts._open = _bup_open

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
			10: False,
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

	def test_sleepTZ(t):
		try:
			alerts.SLEEP_TZ = 'America/Montevideo'
			alerts._gethour()
			h = localtime()
			t.assertEqual(h.tm_zone, '-03')
			t.assertEqual(h.tm_gmtoff, -10800)
		finally:
			alerts.SLEEP_TZ = 'UTC'
			os.environ['TZ'] = 'UTC'
			tzset()

	def test_main_errors(t):
		with mock(fileinput = ['invalid']):
			t.assertEqual(alerts.main(), 0)
			alerts.sys.stderr.write.assert_has_calls([call('ERROR:')])
		with mock(ctrl_c = True):
			t.assertEqual(alerts.main(), 1)

	def test_main(t):
		with mock():
			t.assertEqual(alerts.main(), 0)
			alerts.fileinput.input.assert_called_once_with('-')
		# ~ with mock(fileinput = ['{"state_changed": "1", "worst": "OK"}']):
			# ~ with mock_sleepingHours():
				# ~ t.assertEqual(alerts.main(), 0)

	def test_no_state_changed(t):
		with mock(fileinput = ['{"state_changed": "0", "worst": "OK"}']):
			t.assertEqual(alerts.main(), 0)

	def test_main_nq(t):
		with mock(fileinput = ['{"state_changed": "1", "worst": "CRITICAL"}']):
			with mock_sleepingHours(False):
				with mock_nq():
					with mock_parse():
						t.assertEqual(alerts.main(), 0)
						# ~ alerts.nq.assert_called_once_with('mock_parse')
						alerts.nq.assert_has_calls([
							call('mock_report'),
							call('mock_parse'),
						])

	def test_main_nq_error(t):
		with mock(fileinput = ['{"state_changed": "1", "worst": "CRITICAL"}']):
			with mock_sleepingHours(False):
				with mock_nq(status = 99):
					with mock_parse():
						t.assertEqual(alerts.main(), 99)

	def test_msgContent_no_data(t):
		c = StringIO()
		m = EmailMessage()
		alerts._msgContent(c, {}, m)
		body = """NO_GROUP :: NO_PLUGIN :: NO_CATEGORY
NO_HOST :: NO_TITLE :: ERROR

None
state changed: False

"""
		t.assertEqual(c.getvalue(), body)

	def test_msgContent(t):
		c = StringIO()
		m = EmailMessage()
		m['Date'] = 'Thu, 23 Dec 2021 11:47:23 -0300'
		s = {
			'worst': 'TESTING',
			'group': 'test',
			'host': 'thost',
			'plugin': 'tplugin',
			'category': 'category',
			'title': 'munin_plugin_t',
		}
		alerts._msgContent(c, s, m)
		body = """test :: tplugin :: category
thost :: munin_plugin_t :: TESTING

Thu, 23 Dec 2021 11:47:23 -0300
state changed: False

"""
		t.assertEqual(c.getvalue(), body)

	def test_msgContent_error(t):
		c = StringIO()
		m = EmailMessage()
		m['Date'] = 'Thu, 23 Dec 2021 11:47:23 -0300'
		s = {
			'group': 'test',
			'host': 'thost',
			'plugin': 'tplugin',
			'category': 'category',
			'title': 'munin_plugin_t',
			'ok': [{
				'label': 'testing',
				'value': '0.99',
			}],
			'foks': [{
				'label': 'testing',
				'value': '0.99',
			}],
			'warning': [{
				'label': 'testing',
				'value': '0.99',
			}],
			'critical': [{
				'label': 'testing',
				'value': '0.99',
			}],
			'unknown': [{
				'label': 'testing',
				'value': 'U',
			}],
		}
		alerts._msgContent(c, s, m)
		body = """test :: tplugin :: category
thost :: munin_plugin_t :: ERROR

Thu, 23 Dec 2021 11:47:23 -0300
state changed: False

OK
  testing: 0.99
RECOVER
  testing: 0.99
WARNING
  testing: 0.99
CRITICAL
  testing: 0.99
UNKNOWN
  testing
"""
		t.assertEqual(c.getvalue(), body)

	def test_msgContent_OK(t):
		c = StringIO()
		m = EmailMessage()
		m['Date'] = 'Thu, 23 Dec 2021 11:47:23 -0300'
		s = {
			'group': 'test',
			'host': 'thost',
			'plugin': 'tplugin',
			'category': 'category',
			'title': 'munin_plugin_t',
			'worst': 'OK',
			'ok': [{
				'label': 'testing',
				'value': '0.99',
			}],
		}
		alerts._msgContent(c, s, m)
		body = """test :: tplugin :: category
thost :: munin_plugin_t :: OK

Thu, 23 Dec 2021 11:47:23 -0300
state changed: False

OK
  testing: 0.99
"""
		t.assertEqual(c.getvalue(), body)

	def test_msgContent_RECOVER(t):
		c = StringIO()
		m = EmailMessage()
		m['Date'] = 'Thu, 23 Dec 2021 11:47:23 -0300'
		s = {
			'group': 'test',
			'host': 'thost',
			'plugin': 'tplugin',
			'category': 'category',
			'title': 'munin_plugin_t',
			'worst': 'OK',
			'foks': [{
				'label': 'testing',
				'value': '0.99',
			}],
		}
		alerts._msgContent(c, s, m)
		body = """test :: tplugin :: category
thost :: munin_plugin_t :: OK

Thu, 23 Dec 2021 11:47:23 -0300
state changed: False

RECOVER
  testing: 0.99
"""
		t.assertEqual(c.getvalue(), body)

	def test_msgContent_WARNING(t):
		c = StringIO()
		m = EmailMessage()
		m['Date'] = 'Thu, 23 Dec 2021 11:47:23 -0300'
		s = {
			'group': 'test',
			'host': 'thost',
			'plugin': 'tplugin',
			'category': 'category',
			'title': 'munin_plugin_t',
			'worst': 'WARNING',
			'warning': [{
				'label': 'testing',
				'value': '0.99',
			}],
		}
		alerts._msgContent(c, s, m)
		body = """test :: tplugin :: category
thost :: munin_plugin_t :: WARNING

Thu, 23 Dec 2021 11:47:23 -0300
state changed: False

WARNING
  testing: 0.99
"""
		t.assertEqual(c.getvalue(), body)

	def test_msgContent_CRITICAL(t):
		c = StringIO()
		m = EmailMessage()
		m['Date'] = 'Thu, 23 Dec 2021 11:47:23 -0300'
		s = {
			'group': 'test',
			'host': 'thost',
			'plugin': 'tplugin',
			'category': 'category',
			'title': 'munin_plugin_t',
			'worst': 'CRITICAL',
			'critical': [{
				'label': 'testing',
				'value': '0.99',
			}],
		}
		alerts._msgContent(c, s, m)
		body = """test :: tplugin :: category
thost :: munin_plugin_t :: CRITICAL

Thu, 23 Dec 2021 11:47:23 -0300
state changed: False

CRITICAL
  testing: 0.99
"""
		t.assertEqual(c.getvalue(), body)

	def test_msgContent_UNKNOWN(t):
		c = StringIO()
		m = EmailMessage()
		m['Date'] = 'Thu, 23 Dec 2021 11:47:23 -0300'
		s = {
			'group': 'test',
			'host': 'thost',
			'plugin': 'tplugin',
			'category': 'category',
			'title': 'munin_plugin_t',
			'worst': 'UNKNOWN',
			'unknown': [{
				'label': 'testing',
				'value': 'U',
			}],
		}
		alerts._msgContent(c, s, m)
		body = """test :: tplugin :: category
thost :: munin_plugin_t :: UNKNOWN

Thu, 23 Dec 2021 11:47:23 -0300
state changed: False

UNKNOWN
  testing
"""
		t.assertEqual(c.getvalue(), body)

	def test_parse(t):
		s = {
			'group': 'test',
			'host': 'thost',
			'plugin': 'tplugin',
			'category': 'category',
			'title': 'munin_plugin_t',
			'worst': 'OK',
			'ok': [{
				'label': 'testing',
				'value': '0.99',
			}],
		}
		m = alerts.parse(s)
		t.assertEqual(m['From'], 'thost <munin-alert@thost>')
		t.assertEqual(m['Subject'], 'OK: munin_plugin_t')

	def test_nq(t):
		with mock_open():
			t.assertEqual(alerts.nq(EmailMessage()), 0)
			alerts._open.assert_called_once()

	def test_nq_error(t):
		t.assertEqual(alerts.nq(EmailMessage()), 9)

if __name__ == '__main__':
	unittest.main()
