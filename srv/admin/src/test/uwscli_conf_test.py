#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import admin_t
import admin_test_conf

import uwscli_conf # type: ignore

class TestUwscliConf(unittest.TestCase):

	def test_app_nogroup(t):
		t.assertListEqual(uwscli_conf.App(False).groups, ['nogroup'])

if __name__ == '__main__':
	unittest.main()
