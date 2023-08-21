#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import os

import unittest
import uwscli_t

import slack_bolt

os.environ['UWS_SLACK_CHANNEL_ID'] = 'CTEST'

import botija

class TestBotija(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()
		slack_bolt.mock()

	def test_config(t):
		t.assertEqual(botija.channel_id, 'CTEST')

	def test_msg(t):
		botija.msg('testing')
		slack_bolt.FakeApp.client.chat_postMessage.assert_called_once_with(
			channel = 'CTEST', text = 'testing',
		)

	def test_msg_error(t):
		slack_bolt.mock(fail = True)
		botija.msg('testing')

if __name__ == '__main__':
	unittest.main()
