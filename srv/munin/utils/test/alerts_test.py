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
import alerts_conf as conf

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
		# ~ if isinstance(status, list):
			# ~ def _nq_status(m, prefix = ''):
				# ~ return status.pop(0)
			# ~ alerts.nq = MagicMock(side_effect = _nq_status)
		# ~ else:
			# ~ alerts.nq = MagicMock(return_value = status)
		alerts.nq = MagicMock(return_value = status)
		yield
	finally:
		alerts.nq = nq_bup

@contextmanager
def mock_sleepingHours(state = True):
	sh_bup = conf.sleepingHours
	try:
		conf.sleepingHours = MagicMock(return_value = state)
		yield
	finally:
		conf.sleepingHours = sh_bup

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
def mock_open():
	_bup_open = alerts._open
	def _open(fn, mode):
		return BytesIO()
	try:
		alerts._open = MagicMock(side_effect = _open)
		yield
	finally:
		alerts._open = _bup_open

@contextmanager
def mock_timestamp():
	bup = alerts._timestamp
	try:
		alerts._timestamp = MagicMock(return_value = 123456)
		yield
	finally:
		alerts._timestamp = bup

@contextmanager
def mock_statuspage(mock_sp = True):
	bup = alerts.conf.sp.copy()
	bup_domain = alerts.conf.DOMAIN
	if mock_sp:
		bup_sp = alerts._sp
	try:
		alerts.conf.sp.clear()
		alerts.conf.sp.update({
			'_': {
				'sp_domain': 'sp.comp',
				'sp_mailcc': ['mailcc1@sp.comp', 'mailcc2@sp.comp'],
			},
			'thost': {
				'tgrp': {
					'tctg::tpl': {},
					'tctg::taddr': {
						'component_description': 'testing group -> desc',
						'component': 'testing',
					},
				},
			},
		})
		alerts.conf.DOMAIN = 'uws.test'
		if mock_sp:
			alerts._sp = MagicMock(return_value = None)
		with mock_nq():
			yield
	finally:
		alerts.conf.sp.clear()
		alerts.conf.sp.update(bup.copy())
		alerts.conf.DOMAIN = bup_domain
		if mock_sp:
			alerts._sp = bup_sp

class Test(unittest.TestCase):

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
						alerts.nq.assert_called_once_with('mock_parse')
						# ~ alerts.nq.assert_has_calls([
							# ~ call('mock_report', prefix = 'report'),
							# ~ call('mock_parse'),
						# ~ ])

	def test_main_nq_report_error(t):
		with mock(fileinput = ['{"state_changed": "1", "worst": "CRITICAL"}']):
			with mock_sleepingHours(False):
				with mock_nq(status = 99):
					with mock_parse():
						t.assertEqual(alerts.main(), 99)

	def test_main_nq_parse_error(t):
		with mock(fileinput = ['{"state_changed": "1", "worst": "CRITICAL"}']):
			with mock_sleepingHours(False):
				# ~ with mock_nq(status = [0, 99]):
				with mock_nq(status = 99):
					with mock_parse():
						t.assertEqual(alerts.main(), 99)

	def test_msgContent_no_data(t):
		c = StringIO()
		m = EmailMessage()
		alerts._msgContent(c, {}, m)
		body = """NO_GROUP :: NO_CATEGORY :: NO_PLUGIN
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
		body = """test :: category :: tplugin
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
		body = """test :: category :: tplugin
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
		body = """test :: category :: tplugin
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
		body = """test :: category :: tplugin
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
		body = """test :: category :: tplugin
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
		body = """test :: category :: tplugin
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
		body = """test :: category :: tplugin
thost :: munin_plugin_t :: UNKNOWN

Thu, 23 Dec 2021 11:47:23 -0300
state changed: False

UNKNOWN
  testing
"""
		t.assertEqual(c.getvalue(), body)

	def test_nq(t):
		with mock_open():
			t.assertEqual(alerts.nq(EmailMessage()), 0)
			alerts._open.assert_called_once()

	def test_nq_filename(t):
		with mock_open():
			with mock_timestamp():
				t.assertEqual(alerts.nq(EmailMessage()), 0)
				alerts._open.assert_called_once_with('/var/opt/munin-alert/123456.eml', 'wb')

	def test_nq_filename_prefix(t):
		with mock_open():
			with mock_timestamp():
				t.assertEqual(alerts.nq(EmailMessage(), prefix = 'testing'), 0)
				alerts._open.assert_called_once_with('/var/opt/munin-alert/testing-123456.eml', 'wb')

	def test_nq_error(t):
		t.assertEqual(alerts.nq(EmailMessage()), 9)

	def test_nq_no_message(t):
		t.assertEqual(alerts.nq(None), 8)

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
		t.assertEqual(m.get_charset(), 'utf-8')
		t.assertEqual(m.get_content_type(), 'text/plain')
		t.assertEqual(m['Content-Transfer-Encoding'], '7bit')

	def test_report(t):
		stats = {
			"ok": [{
				"label": "ready",
				"value": "6.00",
				"extinfo": "",
			}],
			"foks": [{
				"label": "ready",
				"value": "6.00",
				"extinfo": "",
			}],
			"warning": [],
			"critical": [],
			"unknown": [],
			"recovered": "",
			"state_changed": "1",
			"worst": "OK",
			"category": "api",
			"title": "production api jobs :: production api parentNotifications.jobs",
			"group": "t.o",
			"host": "app.t.o",
			"plugin": "parentNotifications_jobs",
		}
		m = alerts.report(stats)
		t.assertEqual(m['From'], '"app.t.o" <munin-alert@app.t.o>')
		t.assertEqual(m['Subject'], '[OK] production api parentNotifications.jobs')
		t.assertEqual(m.get_charset(), 'utf-8')
		t.assertEqual(m.get_content_type(), 'text/plain')
		t.assertEqual(m['Content-Transfer-Encoding'], 'base64')

	def test_report_error(t):
		stats = {"testing": RuntimeError('testing')}
		m = alerts.report(stats)
		t.assertIsNone(m)

	def test_statuspage_no_report(t):
		stats = {'worst': 'TEST'}
		t.assertEqual(alerts.statuspage(stats), 1)

	def test_statuspage_no_config(t):
		stats = {'worst': 'OK'}
		t.assertEqual(alerts.statuspage(stats), 2)

	def test_statuspage_host_no_match(t):
		stats = {'host': 'thost', 'worst': 'CRITICAL'}
		t.assertEqual(alerts.statuspage(stats), 2)

	def test_statuspage_host_no_component_addr(t):
		with mock_statuspage():
			stats = {
				'host': 'thost',
				'group': 'tgrp',
				'category': 'tctg',
				'plugin': 'tpl',
				'worst': 'CRITICAL',
			}
			t.assertEqual(alerts.statuspage(stats), 2)

	def test_statuspage(t):
		with mock_statuspage():
			stats = {
				'host': 'thost',
				'group': 'tgrp',
				'category': 'tctg',
				'plugin': 'taddr',
				'worst': 'CRITICAL',
			}
			t.assertEqual(alerts.statuspage(stats), 0)
			alerts._sp.assert_called_once_with(
				'"thost :: tctg :: taddr" <munin-statuspage@uws.test>',
				'"testing group -> desc" <testing@sp.comp>', 'CRITICAL')
			alerts.nq.assert_called_once_with(None, qdir = '/var/opt/munin-alert/statuspage')

	def test_statuspage_message_up(t):
		m = alerts._sp('test@munin.check', 'test@sp.comp', 'OK')
		t.assertEqual(m['From'],    'test@munin.check')
		t.assertEqual(m['To'],      'test@sp.comp')
		t.assertEqual(m['Subject'], 'UP')
		t.assertEqual(m.get_content().strip(), '=)')

	def test_statuspage_message_down(t):
		m = alerts._sp('test@munin.check', 'test@sp.comp', 'CRITICAL')
		t.assertEqual(m['From'],    'test@munin.check')
		t.assertEqual(m['To'],      'test@sp.comp')
		t.assertEqual(m['Subject'], 'DOWN')
		t.assertEqual(m.get_content().strip(), '=(')

	def test_statuspage_message_other(t):
		m = alerts._sp('test@munin.check', 'test@sp.comp', 'TESTING')
		t.assertEqual(m['From'],    'test@munin.check')
		t.assertEqual(m['To'],      'test@sp.comp')
		t.assertEqual(m['Subject'], 'DOWN')
		t.assertEqual(m.get_content().strip(), '=(')

	def test_statuspage_message_cc(t):
		with mock_statuspage(mock_sp = False):
			m = alerts._sp('test@munin.check', 'test@sp.comp', 'OK')
			t.assertEqual(m['Cc'], 'mailcc1@sp.comp, mailcc2@sp.comp')

if __name__ == '__main__':
	unittest.main()
