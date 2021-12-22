#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t

import web_request

web_request.req_total._print = MagicMock()
web_request.req_by_path._print = MagicMock()
web_request.req_errors._print = MagicMock()
web_request.req_time._print = MagicMock()
web_request.req_size._print = MagicMock()

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()

	def tearDown(t):
		mon_t.tearDown()
		web_request.sts = None
		web_request.sts = dict()

	def test_globals(t):
		t.assertDictEqual(web_request.sts, {})

	def test_imports(t):
		t.assertEqual(web_request.req_total.__name__, 'req_total')
		t.assertEqual(web_request.req_by_path.__name__, 'req_by_path')
		t.assertEqual(web_request.req_errors.__name__, 'req_errors')
		t.assertEqual(web_request.req_time.__name__, 'req_time')
		t.assertEqual(web_request.req_size.__name__, 'req_size')

	def test_parse(t):
		t.assertFalse(web_request.parse('testing', None, None))

	def test_parse_time(t):
		t.assertTrue(web_request.parse(web_request.TIME, {}, 99.0))
		t.assertDictEqual(web_request.sts, {
			'default': {
				'all': {
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
				'by_path': {},
				'errors': {},
			},
		})

	def test_parse_count(t):
		t.maxDiff = None
		meta = {
			'status': '400',
		}
		t.assertTrue(web_request.parse(web_request.COUNT, meta, 99.0))
		t.assertDictEqual(web_request.sts, {
			'default': {
				'all': {
					'default': {
						'default': {
							'400': {
								'count': 99.0,
								'size': 0,
								'time': 0,
							},
						},
					},
				},
				'by_path': {'default': 99.0},
				'errors': {'default': {'400': 99.0}},
			},
		})

	def test_parse_size(t):
		t.assertTrue(web_request.parse(web_request.SIZE, {}, 99.0))
		t.assertDictEqual(web_request.sts, {
			'default': {
				'all': {
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
				'by_path': {},
				'errors': {},
			},
		})

	def test_parse_error(t):
		meta = {
			'status': 'not_a_number',
		}
		t.assertFalse(web_request.parse(web_request.COUNT, meta, 99.0))

	def test_config(t):
		sts = {'thost.uws': {}}
		web_request.config(sts)
		web_request.req_total._print.assert_called()
		web_request.req_by_path._print.assert_called()
		web_request.req_errors._print.assert_called()
		web_request.req_time._print.assert_called()
		web_request.req_size._print.assert_called()

	def test_report(t):
		sts = {'thost.uws': {}}
		web_request.report(sts)
		web_request.req_total._print.assert_called()
		web_request.req_by_path._print.assert_called()
		web_request.req_errors._print.assert_called()
		web_request.req_time._print.assert_called()
		web_request.req_size._print.assert_called()

if __name__ == '__main__':
	unittest.main()
