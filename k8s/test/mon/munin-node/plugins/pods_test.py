#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import pods

class Test(unittest.TestCase):

	def test_globals(t):
		t.assertEqual(pods.MONLIB, '/srv/munin/plugins')

if __name__ == '__main__':
	unittest.main()
