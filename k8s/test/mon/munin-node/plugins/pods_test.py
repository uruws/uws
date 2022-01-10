#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock

import pods

_kube_bup = pods._kube

class Test(unittest.TestCase):

	def setUp(t):
		pods._kube = MagicMock(return_value = 0)

	def tearDown(t):
		pods._kube = None
		pods._kube = _kube_bup

	def test_globals(t):
		t.assertEqual(pods.MONLIB, '/srv/munin/plugins')

	def test_imports(t):
		t.assertEqual(pods.pods_info.__name__, 'pods_info')
		t.assertEqual(pods.pods_condition.__name__, 'pods_condition')
		t.assertEqual(pods.pods_container.__name__, 'pods_container')

	def test_mods(t):
		t.assertListEqual(sorted(pods._mods['info'].keys()),
			['pods_condition', 'pods_container', 'pods_info'])

	def test_main_error(t):
		pods._kube.return_value = 99
		t.assertEqual(pods.main(), 99)

if __name__ == '__main__':
	unittest.main()
