#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t

import web_latency

_bup_print = web_latency._print

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		web_latency._print = MagicMock()

	def tearDown(t):
		mon_t.tearDown()
		web_latency._print = _bup_print
		web_latency.sts = None
		web_latency.sts = dict()

	def test_globals(t):
		t.assertDictEqual(web_latency.sts, {})

	def test_print(t):
		_bup_print('testing')

	def test_parse(t):
		t.assertFalse(web_latency.parse('testing', None, None))
		t.assertDictEqual(web_latency.sts, {})

	def test_parse_count(t):
		t.assertTrue(web_latency.parse(web_latency.COUNT, None, None))
		t.assertDictEqual(web_latency.sts, {})

	def test_parse_sum(t):
		t.assertTrue(web_latency.parse(web_latency.SUM, {}, 99.0))
		t.assertDictEqual(web_latency.sts, {
			'default': {'default': {'default': {'sum': 99.0}}},
		})

	def test_config(t):
		sts = {
			'ns': {
				'ingress': {
					'service': None,
				},
			},
		}
		web_latency.config(sts)
		config = [
			# sum
			call('multigraph web_latency_ns_ingress'),
			call('graph_title ns/ingress service latency total'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category web_latency'),
			call('graph_vlabel seconds'),
			call('graph_scale no'),
			call('graph_total total'),
			call('service.label service'),
			call('service.colour COLOUR0'),
			call('service.draw AREASTACK'),
			call('service.min 0'),
			# sum derive
			call('multigraph web_latency_ns_ingress.count'),
			call('graph_title ns/ingress service latency'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category web_latency'),
			call('graph_vlabel latency per second'),
			call('graph_scale no'),
			call('graph_total total'),
			call('service.label service seconds'),
			call('service.colour COLOUR0'),
			call('service.draw AREASTACK'),
			call('service.type DERIVE'),
			call('service.min 0'),
			call('service.cdef service,1000,/'),
		]
		web_latency._print.assert_has_calls(config)
		t.assertEqual(web_latency._print.call_count, len(config))

	def test_report(t):
		sts = {
			'ns': {
				'ingress': {
					'service': {
						'sum': 99.0,
					},
				},
			},
		}
		web_latency.report(sts)
		report = [
			# sum
			call('multigraph web_latency_ns_ingress'),
			call('service.value 99.0'),
			# sum derive
			call('multigraph web_latency_ns_ingress.count'),
			call('service.value 99000'),
		]
		web_latency._print.assert_has_calls(report)
		t.assertEqual(web_latency._print.call_count, len(report))

if __name__ == '__main__':
	unittest.main()
