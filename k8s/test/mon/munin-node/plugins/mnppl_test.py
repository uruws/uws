#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import mnppl

class Test(unittest.TestCase):

	def test_globals(t):
		t.assertEqual(mnppl.plugins_bindir, '/usr/local/bin')
		t.assertEqual(mnppl.plugins_suffix, '.mnppl')

	def test_listPlugins(t):
		t.assertListEqual(mnppl._listPlugins('./k8s/test/mon/munin-node/plugins/mnppl'), [
			't0.mnppl',
			't1.mnppl',
			't2.mnppl',
			't3.mnppl',
			't4.mnppl',
		])

	def test_main(t):
		t.assertEqual(mnppl.main([]), 0)

if __name__ == '__main__':
	unittest.main()
