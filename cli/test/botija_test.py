#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
import uwscli_t

import botija

class TestBotija(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_config(t):
		t.assertEqual(botija.channel_id, '')

if __name__ == '__main__':
	unittest.main()
