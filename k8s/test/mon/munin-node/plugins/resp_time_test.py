#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t
import mon

import resp_time

_bup_print = resp_time._print

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		resp_time._print = MagicMock()

	def tearDown(t):
		mon_t.tearDown()
		resp_time._print = _bup_print

	def test_print(t):
		_bup_print('testing')

	def test_config(t):
		sts = {
			'/testing': {
				'GET': {
					'200': None,
				},
			},
		}
		resp_time.config(mon.cluster(), 'thost.uws', 'thost_uws', sts)
		config = [
			# time index
			call('multigraph web_response_time_thost_uws'),
			call('graph_title thost.uws response time'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category web_time'),
			call('graph_vlabel total seconds'),
			call('graph_scale yes'),
			call('graph_total', 'k8stest', 'total'),
			call('resp__testing_GET_200.label 200 GET /testing'),
			call('resp__testing_GET_200.colour COLOUR0'),
			call('resp__testing_GET_200.draw AREASTACK'),
			call('resp__testing_GET_200.min 0'),
			# time total
			call('multigraph web_response_time_thost_uws.total'),
			call('graph_title thost.uws response time'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category web_time'),
			call('graph_vlabel total seconds'),
			call('graph_scale yes'),
			call('graph_total', 'k8stest', 'total'),
			call('resp__testing_GET_200.label 200 GET /testing'),
			call('resp__testing_GET_200.colour COLOUR0'),
			call('resp__testing_GET_200.draw AREASTACK'),
			call('resp__testing_GET_200.min 0'),
			# time count
			call('multigraph web_response_time_thost_uws.count'),
			call('graph_title thost.uws response time count'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category web_time'),
			call('graph_vlabel time per second'),
			call('graph_scale no'),
			call('graph_total', 'k8stest', 'total'),
			call('resp__testing_GET_200.label 200 GET /testing'),
			call('resp__testing_GET_200.colour COLOUR0'),
			call('resp__testing_GET_200.draw AREASTACK'),
			call('resp__testing_GET_200.type DERIVE'),
			call('resp__testing_GET_200.min 0'),
			call('resp__testing_GET_200.cdef resp__testing_GET_200,1000,/'),
			# time avg
			call('multigraph web_response_time_thost_uws.avg'),
			call('graph_title thost.uws response time average'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category web_time'),
			call('graph_vlabel seconds per response'),
			call('graph_scale no'),
			call('resp__testing_GET_200.label 200 GET /testing'),
			call('resp__testing_GET_200.colour COLOUR0'),
			call('resp__testing_GET_200.min 0'),
		]
		resp_time._print.assert_has_calls(config)
		t.assertEqual(resp_time._print.call_count, len(config))

	def test_report(t):
		sts = {
			'/testing': {
				'GET': {
					'200': {
						'count': 0,
					},
				},
			},
		}
		resp_time.report('thost_uws', sts)

	def test_report_data(t):
		sts = {
			'/testing': {
				'GET': {
					'200': {
						'count': 9,
						'time': 99.0,
					},
				},
			},
		}
		resp_time.report('thost_uws', sts)
		report = [
			# time index
			call('multigraph web_response_time_thost_uws'),
			call('resp__testing_GET_200.value 99.0'),
			# time total
			call('multigraph web_response_time_thost_uws.total'),
			call('resp__testing_GET_200.value 99.0'),
			# time count
			call('multigraph web_response_time_thost_uws.count'),
			call('resp__testing_GET_200.value 99000'),
			# time avg
			call('multigraph web_response_time_thost_uws.avg'),
			call('resp__testing_GET_200.value 11.0'),
		]
		resp_time._print.assert_has_calls(report)
		t.assertEqual(resp_time._print.call_count, len(report))

if __name__ == '__main__':
	unittest.main()
