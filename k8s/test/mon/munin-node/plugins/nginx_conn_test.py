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

if __name__ == '__main__':
	unittest.main()
