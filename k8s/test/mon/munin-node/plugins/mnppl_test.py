#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import mnppl

class Test(unittest.TestCase):

	def test_main(t):
		t.assertEqual(mnppl.main([]), 0)

if __name__ == '__main__':
	unittest.main()
