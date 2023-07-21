#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import wapptpl

class TestWappTpl(unittest.TestCase):

	def test_all_export(t):
		t.assertListEqual(wapptpl.__all__, [
			'url',
		])

if __name__ == '__main__':
	unittest.main()
