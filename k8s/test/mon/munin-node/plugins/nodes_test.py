#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock

import nodes

_kube_bup = nodes._kube

class Test(unittest.TestCase):

	def setUp(t):
		nodes._kube = MagicMock(return_value = 0)

	def tearDown(t):
		nodes._kube = None
		nodes._kube = _kube_bup

	def test_globals(t):
		t.assertEqual(nodes.MONLIB, '/srv/munin/plugins')

	def test_imports(t):
		t.assertEqual(nodes.nodes_info.__name__, 'nodes_info')

	def test_main_error(t):
		nodes._kube.return_value = 99
		t.assertEqual(nodes.main(), 99)
		nodes._kube.assert_called_once_with('nodes', 'info')

	def test_main_info(t):
		t.assertEqual(nodes.main(), 0)
		nodes._kube.assert_called_once_with('nodes', 'info')

if __name__ == '__main__':
	unittest.main()
