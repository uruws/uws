#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t
import mon

import req_by_path

_bup_print = req_by_path._print

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		req_by_path._print = MagicMock()

	def tearDown(t):
		mon_t.tearDown()
		req_by_path._print = _bup_print

	def test_print(t):
		_bup_print('testing')

	def test_config(t):
		sts = {
			'/testing': None,
		}
		req_by_path.config(mon.cluster(), 'thost.uws', 'thost_uws', sts)
		config = [
			# per second
			call('multigraph web_request_thost_uws.by_path'),
			call('graph_title thost.uws request by path'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category web'),
			call('graph_vlabel number per second'),
			call('graph_scale no'),
			call('graph_total', 'k8stest', 'total'),
			call('req__testing.label /testing'),
			call('req__testing.colour COLOUR0'),
			call('req__testing.draw AREASTACK'),
			call('req__testing.type DERIVE'),
			call('req__testing.min 0'),
			call('req__testing.cdef req__testing,1000,/'),
			# per minute
			call('multigraph web_request_thost_uws.by_path_per_minute'),
			call('graph_title thost.uws request by path'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category web'),
			call('graph_vlabel number per minute'),
			call('graph_scale no'),
			call('graph_total', 'k8stest', 'total'),
			call('graph_period minute'),
			call('req__testing.label /testing'),
			call('req__testing.colour COLOUR0'),
			call('req__testing.draw AREASTACK'),
			call('req__testing.type DERIVE'),
			call('req__testing.min 0'),
			call('req__testing.cdef req__testing,1000,/'),
		]
		req_by_path._print.assert_has_calls(config)
		t.assertEqual(req_by_path._print.call_count, len(config))

	def test_report(t):
		sts = {
			'/testing': 99.0,
		}
		req_by_path.report('thost_uws', sts)
		report = [
			# per second
			call('multigraph web_request_thost_uws.by_path'),
			call('req__testing.value', 99000),
			# per minute
			call('multigraph web_request_thost_uws.by_path_per_minute'),
			call('req__testing.value', 99000),
		]
		req_by_path._print.assert_has_calls(report)
		t.assertEqual(req_by_path._print.call_count, len(report))

if __name__ == '__main__':
	unittest.main()
