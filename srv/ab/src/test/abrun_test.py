#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import abrun

class TestABRun(unittest.TestCase):

	def test_run(t):
		t.assertEqual(abrun._run('/usr/bin/false').returncode, 1)

if __name__ == '__main__':
	unittest.main()
