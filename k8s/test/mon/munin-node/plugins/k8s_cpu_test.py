#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t

import k8s_cpu

_bup_print = k8s_cpu._print
_bup_sts = k8s_cpu.sts

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		k8s_cpu._print = MagicMock()
		k8s_cpu.sts = _bup_sts.copy()

	def tearDown(t):
		mon_t.tearDown()
		k8s_cpu._print = _bup_print

	def test_globals(t):
		t.assertDictEqual(k8s_cpu.sts, dict(
			go_version        = 'go_version',
			goroutines        = 'U',
			threads           = 'U',
			cpu_seconds_total = 'U',
			uptime_hours      = 'U',
		))

	def test_print(t):
		_bup_print('testing', '...')

	def test_parse(t):
		t.assertFalse(k8s_cpu.parse('testing', None, None))

if __name__ == '__main__':
	unittest.main()
