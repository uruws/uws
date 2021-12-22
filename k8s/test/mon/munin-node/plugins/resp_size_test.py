#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t
import mon

import resp_size

_bup_print = resp_size._print

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		resp_size._print = MagicMock()

	def tearDown(t):
		mon_t.tearDown()
		resp_size._print = _bup_print

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
		resp_size.config(mon.cluster(), 'thost.uws', 'thost_uws', sts)
		config = [
			# size index
			call('multigraph web_response_size_thost_uws'),
			call('graph_title thost.uws response size'),
			call('graph_args --base 1024 -l 0'),
			call('graph_category web_size'),
			call('graph_vlabel total bytes'),
			call('graph_scale yes'),
			call('graph_total', 'k8stest', 'total'),
			call('resp__testing_GET_200.label 200 GET /testing'),
			call('resp__testing_GET_200.colour COLOUR0'),
			call('resp__testing_GET_200.draw AREASTACK'),
			call('resp__testing_GET_200.min 0'),
			# size total
			call('multigraph web_response_size_thost_uws.total'),
			call('graph_title thost.uws response size'),
			call('graph_args --base 1024 -l 0'),
			call('graph_category web_size'),
			call('graph_vlabel total bytes'),
			call('graph_scale yes'),
			call('graph_total', 'k8stest', 'total'),
			call('resp__testing_GET_200.label 200 GET /testing'),
			call('resp__testing_GET_200.colour COLOUR0'),
			call('resp__testing_GET_200.draw AREASTACK'),
			call('resp__testing_GET_200.min 0'),
			# size count
			call('multigraph web_response_size_thost_uws.count'),
			call('graph_title thost.uws response size count'),
			call('graph_args --base 1024 -l 0'),
			call('graph_category web_size'),
			call('graph_vlabel bytes per second'),
			call('graph_scale yes'),
			call('graph_total', 'k8stest', 'total'),
			call('resp__testing_GET_200.label 200 GET /testing'),
			call('resp__testing_GET_200.colour COLOUR0'),
			call('resp__testing_GET_200.draw AREASTACK'),
			call('resp__testing_GET_200.type DERIVE'),
			call('resp__testing_GET_200.min 0'),
			call('resp__testing_GET_200.cdef resp__testing_GET_200,1000,/'),
			# size avg
			call('multigraph web_response_size_thost_uws.avg'),
			call('graph_title thost.uws response size average'),
			call('graph_args --base 1024 -l 0'),
			call('graph_category web_size'),
			call('graph_vlabel bytes per response'),
			call('graph_scale yes'),
			call('resp__testing_GET_200.label 200 GET /testing'),
			call('resp__testing_GET_200.colour COLOUR0'),
			call('resp__testing_GET_200.min 0'),

		]
		resp_size._print.assert_has_calls(config)
		t.assertEqual(resp_size._print.call_count, len(config))

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
		resp_size.report('thost_uws', sts)

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
		resp_size.report('thost_uws', sts)
		report = [
			# size index
			call('multigraph web_response_size_thost_uws'),
			call('resp__testing_GET_200.value 99.0'),
			# size total
			call('multigraph web_response_size_thost_uws.total'),
			call('resp__testing_GET_200.value 99.0'),
			# size count
			call('multigraph web_response_size_thost_uws.count'),
			call('resp__testing_GET_200.value 99000'),
			# size avg
			call('multigraph web_response_size_thost_uws.avg'),
			call('resp__testing_GET_200.value 11.0'),
		]
		resp_size._print.assert_has_calls(report)
		t.assertEqual(resp_size._print.call_count, len(report))

if __name__ == '__main__':
	unittest.main()
