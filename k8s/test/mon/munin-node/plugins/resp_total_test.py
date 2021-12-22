#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t
import mon

import resp_total

_bup_print = resp_total._print

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		resp_total._print = MagicMock()

	def tearDown(t):
		mon_t.tearDown()
		resp_total._print = _bup_print

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
		resp_total.config(mon.cluster(), 'thost.uws', 'thost_uws', sts)
		config = [
			# total index
			call('multigraph web_response_thost_uws'),
			call('graph_title thost.uws response'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category web_resp'),
			call('graph_vlabel total number'),
			call('graph_scale yes'),
			call('graph_total', 'k8stest', 'total'),
			call('resp__testing_GET_200.label 200 GET /testing'),
			call('resp__testing_GET_200.colour COLOUR0'),
			call('resp__testing_GET_200.draw AREASTACK'),
			call('resp__testing_GET_200.min 0'),
			# total
			call('multigraph web_response_thost_uws.total'),
			call('graph_title thost.uws response'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category web_resp'),
			call('graph_vlabel total number'),
			call('graph_scale yes'),
			call('graph_total', 'k8stest', 'total'),
			call('resp__testing_GET_200.label 200 GET /testing'),
			call('resp__testing_GET_200.colour COLOUR0'),
			call('resp__testing_GET_200.draw AREASTACK'),
			call('resp__testing_GET_200.min 0'),
			# total count
			call('multigraph web_response_thost_uws.count'),
			call('graph_title thost.uws response count'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category web_resp'),
			call('graph_vlabel number per second'),
			call('graph_scale no'),
			call('graph_total', 'k8stest', 'total'),
			call('resp__testing_GET_200.label 200 GET /testing'),
			call('resp__testing_GET_200.colour COLOUR0'),
			call('resp__testing_GET_200.draw AREASTACK'),
			call('resp__testing_GET_200.type DERIVE'),
			call('resp__testing_GET_200.min 0'),
			call('resp__testing_GET_200.cdef resp__testing_GET_200,1000,/'),
		]
		resp_total._print.assert_has_calls(config)
		t.assertEqual(resp_total._print.call_count, len(config))

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
		resp_total.report('thost_uws', sts)

	def test_report_data(t):
		sts = {
			'/testing': {
				'GET': {
					'200': {
						'count': 9,
						'size': 99.0,
					},
				},
			},
		}
		resp_total.report('thost_uws', sts)
		report = [
			# total index
			call('multigraph web_response_thost_uws'),
			call('resp__testing_GET_200.value 9'),
			# total
			call('multigraph web_response_thost_uws.total'),
			call('resp__testing_GET_200.value 9'),
			# total count
			call('multigraph web_response_thost_uws.count'),
			call('resp__testing_GET_200.value 9000'),
		]
		resp_total._print.assert_has_calls(report)
		t.assertEqual(resp_total._print.call_count, len(report))

if __name__ == '__main__':
	unittest.main()
