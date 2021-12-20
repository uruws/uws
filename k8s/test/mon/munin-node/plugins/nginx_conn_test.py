#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t

import nginx_conn

_bup_print = nginx_conn._print
_bup_sts = nginx_conn.sts

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		nginx_conn._print = MagicMock()
		nginx_conn.sts = _bup_sts.copy()

	def tearDown(t):
		mon_t.tearDown()
		nginx_conn._print = _bup_print

	def test_globals(t):
		t.assertDictEqual(nginx_conn.sts, {
			'accepted': 'U',
			'active': 'U',
			'handled': 'U',
			'reading': 'U',
			'waiting': 'U',
			'writing': 'U',
		})

	def test_print(t):
		_bup_print('test', 'ing')

	def test_parse(t):
		t.assertFalse(nginx_conn.parse('testing', None, None))
		t.assertFalse(nginx_conn.parse('nginx_ingress_controller_nginx_process_connections',
			{}, 0.999))

	def test_parse_data(t):
		states = [
			'active',
			'reading',
			'writing',
			'waiting',
			'accepted',
			'handled',
		]
		for s in states:
			t.assertTrue(nginx_conn.parse('nginx_ingress_controller_nginx_process_connections',
				{'state': s}, 0.999))

	def test_config(t):
		nginx_conn.config({})
		config = [
			call('multigraph nginx_connections_state'),
			call('graph_title connections state'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category nginx_conn'),
			call('graph_vlabel number'),
			call('graph_scale yes'),
			call('active.label active'),
			call('active.colour COLOUR0'),
			call('active.min 0'),
			call('reading.label reading'),
			call('reading.colour COLOUR1'),
			call('reading.min 0'),
			call('waiting.label waiting'),
			call('waiting.colour COLOUR2'),
			call('waiting.min 0'),
			call('writing.label writing'),
			call('writing.colour COLOUR3'),
			call('writing.min 0'),
			call('multigraph nginx_connections'),
			call('graph_title connections total'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category nginx_conn'),
			call('graph_vlabel number'),
			call('graph_scale yes'),
			call('accepted.label accepted'),
			call('accepted.colour COLOUR0'),
			call('accepted.min 0'),
			call('handled.label handled'),
			call('handled.colour COLOUR1'),
			call('handled.min 0'),
			call('multigraph nginx_connections.counter'),
			call('graph_title connections'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category nginx_conn'),
			call('graph_vlabel number per second'),
			call('graph_scale no'),
			call('accepted.label accepted'),
			call('accepted.colour COLOUR0'),
			call('accepted.type DERIVE'),
			call('accepted.min 0'),
			call('accepted.cdef accepted,1000,/'),
			call('handled.label handled'),
			call('handled.colour COLOUR1'),
			call('handled.type DERIVE'),
			call('handled.min 0'),
			call('handled.cdef handled,1000,/'),
		]
		nginx_conn._print.assert_has_calls(config)
		t.assertEqual(nginx_conn._print.call_count, len(config))

if __name__ == '__main__':
	unittest.main()
