#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t

import nginx_proc

_bup_print = nginx_proc._print
_bup_sts = nginx_proc.sts

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		nginx_proc._print = MagicMock()
		nginx_proc.sts = _bup_sts.copy()

	def tearDown(t):
		mon_t.tearDown()
		nginx_proc._print = _bup_print

	def test_globals(t):
		t.assertDictEqual(nginx_proc.sts, {
			'byte': {
				'read': 'U',
				'write': 'U',
			},
			'cpu': {
				'controller': 'U',
				'total': 'U',
			},
			'mem': {
				'resident': 'U',
				'virtual': 'U',
			},
			'requests': 'U',
			'uptime': 'U',
		})

	def test_print(t):
		_bup_print('test', 'ing')

	def test_parse(t):
		t.assertFalse(nginx_proc.parse('testing', None, None))

	def test_parse_cpu(t):
		t.assertTrue(nginx_proc.parse(nginx_proc.CPU_CONTROLLER, None, 0.999))
		t.assertEqual(nginx_proc.sts['cpu']['controller'], 0.999)
		t.assertTrue(nginx_proc.parse(nginx_proc.CPU_TOTAL, None, 0.999))
		t.assertEqual(nginx_proc.sts['cpu']['total'], 0.999)

if __name__ == '__main__':
	unittest.main()
