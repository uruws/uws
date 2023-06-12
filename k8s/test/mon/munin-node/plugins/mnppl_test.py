#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from   unittest.mock import MagicMock, call

import mon_t

import mnppl

_bup_print = mnppl._print

testing_plugins_bindir = './k8s/test/mon/munin-node/plugins/mnppl'

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		mnppl._print = MagicMock()

	def test_globals(t):
		t.assertEqual(mnppl.plugins_bindir, '/usr/local/bin')
		t.assertEqual(mnppl.plugins_suffix, '.mnppl')
		t.assertEqual(mnppl.pool_wait,      300)
		t.assertEqual(mnppl.time_warning,   270)
		t.assertEqual(mnppl.time_critical,  290)

	#
	# configs and reports
	#

	def test_print(t):
		_bup_print('testing', '...')

	#
	# run parallel
	#

	def test_listPlugins(t):
		t.assertListEqual(mnppl._listPlugins(testing_plugins_bindir), [
			't0.mnppl',
			't1.mnppl',
			't2.mnppl',
			't3.mnppl',
			't4.mnppl',
		])

	#
	# main
	#

	def test_main_no_plugins(t):
		t.assertEqual(mnppl.main([]), 1)

if __name__ == '__main__':
	unittest.main()
