#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t

import web_sent

_bup_print = web_sent._print

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		web_sent._print = MagicMock()

	def tearDown(t):
		mon_t.tearDown()
		web_sent._print = _bup_print
		web_sent.sts = None
		web_sent.sts = dict()

	def test_globals(t):
		t.assertDictEqual(web_sent.sts, {})

	def test_print(t):
		_bup_print('testing')

	def test_parse(t):
		t.assertFalse(web_sent.parse('testing', None, None))
		t.assertDictEqual(web_sent.sts, {})

	def test_parse_sum(t):
		t.assertTrue(web_sent.parse(web_sent.SUM, {}, 99.0))
		t.assertDictEqual(web_sent.sts, {
			'default': {'default': {'default': {'default': {'count': 'U', 'sum': 99.0}}}},
		})

	def test_parse_count(t):
		t.assertTrue(web_sent.parse(web_sent.COUNT, {}, 99.0))
		t.assertDictEqual(web_sent.sts, {
			'default': {'default': {'default': {'default': {'count': 99.0, 'sum': 'U'}}}},
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
		web_sent.config(sts)
		config = [
			# total
			call('multigraph web_sent_ns_ingress_service'),
			call('graph_title ns/ingress service client requests total'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category web_sent'),
			call('graph_vlabel number'),
			call('graph_scale yes'),
			call('graph_total total'),
			call('status_200.label 200'),
			call('status_200.colour COLOUR0'),
			call('status_200.draw AREASTACK'),
			call('status_200.min 0'),
			# count
			call('multigraph web_sent_ns_ingress_service.count'),
			call('graph_title ns/ingress service client requests'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category web_sent'),
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
		web_sent._print.assert_has_calls(config)
		t.assertEqual(web_sent._print.call_count, len(config))

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
		web_sent.report(sts)
		report = [
			# total
			call('multigraph web_sent_ns_ingress_service'),
			call('status_200.value 99.0'),
			# count
			call('multigraph web_sent_ns_ingress_service.count'),
			call('status_200.value 99000'),
		]
		web_sent._print.assert_has_calls(report)
		t.assertEqual(web_sent._print.call_count, len(report))

if __name__ == '__main__':
	unittest.main()
