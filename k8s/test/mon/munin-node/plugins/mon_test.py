#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import mon

class Test(unittest.TestCase):

	def test_globals(t):
		t.assertFalse(mon.debug())
		t.assertIsNone(mon.cluster())

if __name__ == '__main__':
	unittest.main()
