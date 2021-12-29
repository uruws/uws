#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t
import mon

import req_total

_bup_print = req_total._print

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		req_total._print = MagicMock()

	def tearDown(t):
		mon_t.tearDown()
		req_total._print = _bup_print

	def test_print(t):
		_bup_print('testing')

	def test_config(t):
		sts = {
			'/testing': {
				'GET': {
					'200': {}
				},
			},
		}
		req_total.config(mon.cluster(), 'thost.uws', 'thost_uws', sts)
		config = [
			# total index
			call('multigraph web_request_thost_uws'),
			call('graph_title thost.uws request'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category web'),
			call('graph_vlabel total number'),
			call('graph_scale yes'),
			call('graph_total', 'k8stest', 'total'),
			call('req__testing_GET_200.label 200 GET /testing'),
			call('req__testing_GET_200.colour COLOUR0'),
			call('req__testing_GET_200.draw AREASTACK'),
			call('req__testing_GET_200.min 0'),
			# total
			call('multigraph web_request_thost_uws.total'),
			call('graph_title thost.uws request'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category web'),
			call('graph_vlabel total number'),
			call('graph_scale yes'),
			call('graph_total', 'k8stest', 'total'),
			call('req__testing_GET_200.label 200 GET /testing'),
			call('req__testing_GET_200.colour COLOUR0'),
			call('req__testing_GET_200.draw AREASTACK'),
			call('req__testing_GET_200.min 0'),
			# total count
			call('multigraph web_request_thost_uws.count'),
			call('graph_title thost.uws request count'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category web'),
			call('graph_vlabel number per second'),
			call('graph_scale no'),
			call('graph_total', 'k8stest', 'total'),
			call('req__testing_GET_200.label 200 GET /testing'),
			call('req__testing_GET_200.colour COLOUR0'),
			call('req__testing_GET_200.draw AREASTACK'),
			call('req__testing_GET_200.type DERIVE'),
			call('req__testing_GET_200.min 0'),
			call('req__testing_GET_200.cdef req__testing_GET_200,1000,/'),
			# total count per minute
			call('multigraph web_request_thost_uws.count_per_minute'),
			call('graph_title thost.uws request count'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category web'),
			call('graph_vlabel number per minute'),
			call('graph_scale no'),
			call('graph_total', 'k8stest', 'total'),
			call('graph_period minute'),
			call('req__testing_GET_200.label 200 GET /testing'),
			call('req__testing_GET_200.colour COLOUR0'),
			call('req__testing_GET_200.draw AREASTACK'),
			call('req__testing_GET_200.type DERIVE'),
			call('req__testing_GET_200.min 0'),
			call('req__testing_GET_200.cdef req__testing_GET_200,1000,/'),
		]
		req_total._print.assert_has_calls(config)
		t.assertEqual(req_total._print.call_count, len(config))

	def test_report(t):
		sts = {
			'/testing': {
				'GET': {
					'200': {'count': 99.0},
				},
			},
		}
		req_total.report('thost_uws', sts)
		report = [
			# total index
			call('multigraph web_request_thost_uws'),
			call('req__testing_GET_200.value 99.0'),
			# total
			call('multigraph web_request_thost_uws.total'),
			call('req__testing_GET_200.value 99.0'),
			# total count
			call('multigraph web_request_thost_uws.count'),
			call('req__testing_GET_200.value 99000'),
			# total count per minute
			call('multigraph web_request_thost_uws.count_per_minute'),
			call('req__testing_GET_200.value 99000'),
		]
		req_total._print.assert_has_calls(report)
		t.assertEqual(req_total._print.call_count, len(report))

if __name__ == '__main__':
	unittest.main()
