#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import re

import unittest
from unittest.mock import MagicMock

import mon_t
import mon_metrics

import mon

def _mock_resp(d):
	body = '\n'.join(d).encode()
	r = MagicMock()
	r.read = MagicMock(return_value = body)
	return r

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
		r = _mock_resp(['# testing', '\n'])
		for __, __, __ in mon_metrics._metrics_parse(r):
			pass # pragma no cover
		# miss lines
		r = _mock_resp(['{}'])
		for __, __, __ in mon_metrics._metrics_parse(r):
			pass # pragma no cover
		# parse
		r = _mock_resp(['testing 99.0'])
		for name, meta, value in mon_metrics._metrics_parse(r):
			t.assertEqual(name, 'testing')
			t.assertIsNone(meta)
			t.assertEqual(value, 99.0)

	def test_metrics_parse_meta(t):
		# parse metadata
		r = _mock_resp(['testing{k0="v0",k1="v1"} 0.99'])
		for name, meta, value in mon_metrics._metrics_parse(r):
			t.assertEqual(name, 'testing')
			t.assertDictEqual(meta, {'k0': 'v0', 'k1': 'v1'})
			t.assertEqual(value, 0.99)

	def test_metrics_parse_meta_error(t):
		r = _mock_resp(['testing{k0=v0} 0.99'])
		for __, __, __ in mon_metrics._metrics_parse(r):
			pass
		mon._print.assert_called_once()

	def test_metrics_parse_value_error(t):
		r = _mock_resp(['testing 0,99'])
		for name, meta, value in mon_metrics._metrics_parse(r):
			t.assertEqual(name, 'testing')
			t.assertIsNone(meta)
			t.assertEqual(value, 'U')

if __name__ == '__main__':
	unittest.main()
