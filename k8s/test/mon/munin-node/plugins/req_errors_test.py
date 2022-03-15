#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t
import mon

import req_errors

_bup_print = req_errors._print

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		req_errors._print = MagicMock()

	def tearDown(t):
		mon_t.tearDown()
		req_errors._print = _bup_print

	def test_print(t):
		_bup_print('testing')

	def test_config(t):
		sts = {
			'/testing': {
				'200': None,
			},
		}
		req_errors.config(mon.cluster(), 'thost.uws', 'thost_uws', sts)
		config = [
			# per second
			call('multigraph web_request_thost_uws.errors'),
			call('graph_title thost.uws request errors'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category web'),
			call('graph_vlabel number per second'),
			call('graph_scale no'),
			call('graph_total', 'k8stest', 'total'),
			call('req__testing_200.label 200 /testing'),
			call('req__testing_200.colour COLOUR0'),
			call('req__testing_200.draw AREASTACK'),
			call('req__testing_200.type DERIVE'),
			call('req__testing_200.min 0'),
			call('req__testing_200.cdef req__testing_200,1000,/'),
			# per minute
			call('multigraph web_request_thost_uws.errors_per_minute'),
			call('graph_title thost.uws request errors'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category web'),
			call('graph_vlabel number per minute'),
			call('graph_scale no'),
			call('graph_total', 'k8stest', 'total'),
			call('graph_period minute'),
			call('req__testing_200.label 200 /testing'),
			call('req__testing_200.colour COLOUR0'),
			call('req__testing_200.draw AREASTACK'),
			call('req__testing_200.type DERIVE'),
			call('req__testing_200.min 0'),
			call('req__testing_200.cdef req__testing_200,1000,/'),
			# per minute avg
			call('multigraph web_request_thost_uws.errors_per_minute_avg'),
			call('graph_title thost.uws request errors average'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category web'),
			call('graph_vlabel number per minute'),
			call('graph_scale no'),
			call('graph_period minute'),
			call('req_avg.label average'),
			call('req_avg.colour COLOUR0'),
			call('req_avg.draw AREASTACK'),
			call('req_avg.type DERIVE'),
			call('req_avg.min 0'),
			call('req_avg.cdef req_avg,1000,/'),
			call('req_avg.warning 1'),
			call('req_avg.critical 2'),
		]
		req_errors._print.assert_has_calls(config)
		t.assertEqual(req_errors._print.call_count, len(config))

	def test_report(t):
		sts = {
			'/testing': {
				'200': 99.0,
			},
		}
		sts_total = {
			'/testing': {
				'GET': {
					'200': {'count': 99.0},
				},
			},
		}
		req_errors.report('thost_uws', sts, sts_total)
		report = [
			# per second
			call('multigraph web_request_thost_uws.errors'),
			call('req__testing_200.value', 99000),
			# per minute
			call('multigraph web_request_thost_uws.errors_per_minute'),
			call('req__testing_200.value', 99000),
			# per minute avg
			call('multigraph web_request_thost_uws.errors_per_minute_avg'),
			call('req_avg.value', 1000),
		]
		req_errors._print.assert_has_calls(report)
		t.assertEqual(req_errors._print.call_count, len(report))

if __name__ == '__main__':
	unittest.main()
