#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t

import web_ssl

_bup_print = web_ssl._print
_bup_time = web_ssl.time

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		web_ssl._print = MagicMock()
		web_ssl.time = MagicMock(return_value = 1640207589)

	def tearDown(t):
		mon_t.tearDown()
		web_ssl._print = _bup_print
		web_ssl.sts = None
		web_ssl.sts = dict()
		web_ssl.time = _bup_time

	def test_globals(t):
		t.assertDictEqual(web_ssl.sts, {})

	def test_print(t):
		_bup_print('testing')

	def test_parse(t):
		t.assertFalse(web_ssl.parse('testing', None, None))
		t.assertDictEqual(web_ssl.sts, {})

	def test_parse_sum(t):
		t.assertTrue(web_ssl.parse(web_ssl.SUM, {}, 99.0))
		t.assertDictEqual(web_ssl.sts, {
			'default': {'default': 99.0},
		})

	def test_config(t):
		sts = {'default': {'default': 1642799589}}
		web_ssl.config(sts)
		config = [
			call('multigraph web_ssl_default_default'),
			call('graph_title default ssl cert expire'),
			call('graph_args --base 1000'),
			call('graph_category web_ssl'),
			call('graph_vlabel days'),
			call('graph_scale no'),
			call('ssl.label expire'),
			call('ssl.colour COLOUR0'),
			call('ssl.draw AREA'),
			call('ssl.info', 'Fri Jan 21 21:13:09 2022 +0000'),
			call('ssl.warning 20:'),
			call('ssl.critical 15:'),
		]
		web_ssl._print.assert_has_calls(config)
		t.assertEqual(web_ssl._print.call_count, len(config))

	def test_report(t):
		sts = {'default': {'default': 1642799589}}
		web_ssl.report(sts)
		report = [
			call('multigraph web_ssl_default_default'),
			call('ssl.value', 30.0),
		]
		web_ssl._print.assert_has_calls(report)
		t.assertEqual(web_ssl._print.call_count, len(report))

if __name__ == '__main__':
	unittest.main()
