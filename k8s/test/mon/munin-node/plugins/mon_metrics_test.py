#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib import contextmanager
import json
import re

import unittest
from unittest.mock import MagicMock

import mon_t
import mon_metrics

import mon

def _mock_response(r, status):
	resp = MagicMock()
	resp.read = MagicMock(return_value = r)
	resp.status = status
	return resp

@contextmanager
def mock(resp = {}, resp_status = 200, resp_fail = False, metrics = (None, None, None)):
	_bup_urlopen = mon_metrics.urlopen
	_bup_exit = mon_metrics._exit
	_bup_metrics_parse = mon_metrics._metrics_parse
	def _exit(status):
		raise SystemExit(status)
	def _resp_fail():
		raise Exception('mock_error')
	try:
		if resp_fail:
			mon_metrics.urlopen = MagicMock(side_effect = _resp_fail)
		else:
			r = json.dumps(resp).encode()
			mon_metrics.urlopen = MagicMock(return_value = _mock_response(r, resp_status))
		mon_metrics._exit = MagicMock(side_effect = _exit)
		mon_metrics._metrics_parse = MagicMock(return_value = metrics)
		yield
	finally:
		mon_metrics.urlopen = _bup_urlopen
		mon_metrics._exit = _bup_exit
		mon_metrics._metrics_parse = _bup_metrics_parse

def _mock_metric(d: list):
	body = '\n'.join(d).encode()
	r = MagicMock()
	r.read = MagicMock(return_value = body)
	return r

@contextmanager
def mock_metrics(d = (None, None, None)):
	_bup = mon_metrics._metrics_get
	def __get(url):
		yield d
	try:
		mon_metrics._metrics_get = MagicMock(side_effect = __get)
		yield
	finally:
		mon_metrics._metrics_get = _bup

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()

	def tearDown(t):
		mon_t.tearDown()

	def test_regexs(t):
		t.assertIsInstance(mon_metrics.parse_re, re.Pattern)
		t.assertIsInstance(mon_metrics.line1_re, re.Pattern)
		t.assertIsInstance(mon_metrics.line2_re, re.Pattern)
		t.assertIsInstance(mon_metrics.line3_re, re.Pattern)
		t.assertIsInstance(mon_metrics.line4_re, re.Pattern)

	def test_metrics_parse(t):
		# ignore lines
		r = _mock_metric(['# testing', '\n'])
		for __, __, __ in mon_metrics._metrics_parse(r):
			pass # pragma no cover
		# miss lines
		r = _mock_metric(['{}'])
		for __, __, __ in mon_metrics._metrics_parse(r):
			pass # pragma no cover
		# parse
		r = _mock_metric(['testing 99.0'])
		for name, meta, value in mon_metrics._metrics_parse(r):
			t.assertEqual(name, 'testing')
			t.assertIsNone(meta)
			t.assertEqual(value, 99.0)

	def test_metrics_parse_meta(t):
		# parse metadata
		r = _mock_metric(['testing{k0="v0",k1="v1"} 0.99'])
		for name, meta, value in mon_metrics._metrics_parse(r):
			t.assertEqual(name, 'testing')
			t.assertDictEqual(meta, {'k0': 'v0', 'k1': 'v1'})
			t.assertEqual(value, 0.99)

	def test_metrics_parse_meta_error(t):
		r = _mock_metric(['testing{k0=v0} 0.99'])
		for __, __, __ in mon_metrics._metrics_parse(r):
			pass
		mon._print.assert_called_once()

	def test_metrics_parse_value_error(t):
		r = _mock_metric(['testing 0,99'])
		for name, meta, value in mon_metrics._metrics_parse(r):
			t.assertEqual(name, 'testing')
			t.assertIsNone(meta)
			t.assertEqual(value, 'U')

	def test_exit(t):
		with t.assertRaises(SystemExit) as e:
			mon_metrics._exit(0)
		err = e.exception
		t.assertEqual(err.args[0], 0)
		with t.assertRaises(SystemExit) as e:
			mon_metrics._exit(2)
		err = e.exception
		t.assertEqual(err.args[0], 2)

	def test_metrics_get(t):
		with mock():
			mon_metrics._metrics_get('testing')
			mon_metrics._metrics_parse.assert_called_once()

	def test_metrics_get_errors(t):
		# urlopen
		with mock(resp_fail = True):
			with t.assertRaises(SystemExit) as e:
				mon_metrics._metrics_get('testing')
			err = e.exception
			t.assertEqual(err.args[0], 9)
		# resp
		with mock(resp_status = 900):
			with t.assertRaises(SystemExit) as e:
				mon_metrics._metrics_get('testing')
			err = e.exception
			t.assertEqual(err.args[0], 8)

	def test_metrics_data(t):
		with mock_metrics():
			t.assertEqual(mon_metrics._metrics('testing', {}), {})
		# with mods
		with mock_metrics():
			tm = MagicMock()
			tm.sts = MagicMock()
			tm.sts.copy = MagicMock(return_value = 'mock_status')
			tm.parse = MagicMock(return_value = 'mock_parse')
			mods = {'testing': tm}
			t.assertEqual(mon_metrics._metrics('testing', mods), {'testing': 'mock_status'})
			mon_metrics._metrics_get.assert_called_once_with('testing')
			tm.parse.assert_called_once_with(None, None, None)
			tm.sts.copy.assert_called_once()

	def test_config(t):
		with mock_metrics():
			tm = MagicMock()
			tm.config = MagicMock()
			t.assertEqual(mon_metrics._config('testing', {'testing': tm}), 0)
			tm.config.assert_called_once()

	def test_report(t):
		with mock_metrics():
			tm = MagicMock()
			tm.report = MagicMock()
			t.assertEqual(mon_metrics._report('testing', {'testing': tm}), 0)
			tm.report.assert_called_once()

if __name__ == '__main__':
	unittest.main()
