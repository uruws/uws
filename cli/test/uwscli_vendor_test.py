#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import uwscli_vendor

class Test(unittest.TestCase):

	def test_exports(t):
		t.assertListEqual(uwscli_vendor.__all__, ['semver'])
		from uwscli_vendor import semver

if __name__ == '__main__':
	unittest.main()
