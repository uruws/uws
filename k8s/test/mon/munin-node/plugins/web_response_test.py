#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t

import web_response

web_response.resp_total._print = MagicMock()
web_response.resp_time._print = MagicMock()
web_response.resp_size._print = MagicMock()

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()

	def tearDown(t):
		mon_t.tearDown()
		web_response.sts = None
		web_response.sts = dict()

	def test_globals(t):
		t.assertDictEqual(web_response.sts, {})

	def test_imports(t):
		t.assertEqual(web_response.resp_total.__name__, 'resp_total')
		t.assertEqual(web_response.resp_time.__name__, 'resp_time')
		t.assertEqual(web_response.resp_size.__name__, 'resp_size')

	def test_parse(t):
		t.assertFalse(web_response.parse('testing', None, None))

	def test_parse_time(t):
		t.assertTrue(web_response.parse(web_response.TIME, {}, 99.0))
		t.assertDictEqual(web_response.sts, {
			'default': {
				'default': {
					'default': {
						'unknown': {
							'count': 0,
							'size': 0,
							'time': 99.0,
						},
					},
				},
			},
		})

	def test_parse_count(t):
		t.assertTrue(web_response.parse(web_response.COUNT, {}, 99.0))
		t.assertDictEqual(web_response.sts, {
			'default': {
				'default': {
					'default': {
						'unknown': {
							'count': 99.0,
							'size': 0,
							'time': 0,
						},
					},
				},
			},
		})

	def test_parse_size(t):
		t.assertTrue(web_response.parse(web_response.SIZE, {}, 99.0))
		t.assertDictEqual(web_response.sts, {
			'default': {
				'default': {
					'default': {
						'unknown': {
							'count': 0,
							'size': 99.0,
							'time': 0,
						},
					},
				},
			},
		})

	def test_config(t):
		sts = {'thost.uws': {}}
		web_response.config(sts)
		web_response.resp_total._print.assert_called()
		web_response.resp_time._print.assert_called()
		web_response.resp_size._print.assert_called()

	def test_report(t):
		sts = {'thost.uws': {}}
		web_response.report(sts)
		web_response.resp_total._print.assert_called()
		web_response.resp_time._print.assert_called()
		web_response.resp_size._print.assert_called()

if __name__ == '__main__':
	unittest.main()
