#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t

import web_ingress

_bup_print = web_ingress._print

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		web_ingress._print = MagicMock()

	def tearDown(t):
		mon_t.tearDown()
		web_ingress._print = _bup_print
		web_ingress.sts = None
		web_ingress.sts = dict()

	def test_globals(t):
		t.assertDictEqual(web_ingress.sts, {})

	def test_print(t):
		_bup_print('testing')

	def test_parse(t):
		t.assertFalse(web_ingress.parse('testing', None, None))
		t.assertDictEqual(web_ingress.sts, {})

	def test_parse_data(t):
		t.assertTrue(web_ingress.parse(web_ingress.REQUESTS, {}, 99.0))
		t.assertDictEqual(web_ingress.sts, {
			'default': {'default': {'default': {'unknown': 99.0}}},
		})

	def test_config(t):
		sts = {
			'ns': {
				'ingress': {
					'service': {
						'200': None,
					},
				},
			},
		}
		web_ingress.config(sts)
		config = [
			# total
			call('multigraph web_ingress_ns_ingress_service'),
			call('graph_title ns/ingress service client requests total'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category web_ingress'),
			call('graph_vlabel number'),
			call('graph_scale yes'),
			call('graph_total total'),
			call('status_200.label 200'),
			call('status_200.colour COLOUR0'),
			call('status_200.draw AREASTACK'),
			call('status_200.min 0'),
			# count
			call('multigraph web_ingress_ns_ingress_service.count'),
			call('graph_title ns/ingress service client requests'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category web_ingress'),
			call('graph_vlabel number per second'),
			call('graph_scale yes'),
			call('graph_total total'),
			call('status_200.label 200'),
			call('status_200.colour COLOUR0'),
			call('status_200.draw AREASTACK'),
			call('status_200.type DERIVE'),
			call('status_200.min 0'),
			call('status_200.cdef status_200,1000,/'),
		]
		web_ingress._print.assert_has_calls(config)
		t.assertEqual(web_ingress._print.call_count, len(config))

	def test_report(t):
		sts = {
			'ns': {
				'ingress': {
					'service': {
						'200': 99.0,
					},
				},
			},
		}
		web_ingress.report(sts)
		report = [
			# total
			call('multigraph web_ingress_ns_ingress_service'),
			call('status_200.value 99.0'),
			# count
			call('multigraph web_ingress_ns_ingress_service.count'),
			call('status_200.value 99000'),
		]
		web_ingress._print.assert_has_calls(report)
		t.assertEqual(web_ingress._print.call_count, len(report))

if __name__ == '__main__':
	unittest.main()
