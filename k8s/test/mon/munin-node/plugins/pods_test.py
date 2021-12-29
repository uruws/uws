#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import pods

class Test(unittest.TestCase):

	def test_globals(t):
		t.assertEqual(pods.MONLIB, '/srv/munin/plugins')

	def test_imports(t):
		t.assertEqual(pods.pods_info.__name__, 'pods_info')
		t.assertEqual(pods.pods_condition.__name__, 'pods_condition')
		t.assertEqual(pods.pods_container.__name__, 'pods_container')

	def test_mods(t):
		t.assertListEqual(sorted(pods._mods.keys()),
			['pods_condition', 'pods_container', 'pods_info'])

if __name__ == '__main__':
	unittest.main()
