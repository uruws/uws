#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
import uwscli_t

import slack_bolt

import botija

class TestBotija(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()
		slack_bolt.mock()

	def test_config(t):
		t.assertEqual(botija.channel_id, 'CTEST')

	def test_msg(t):
		t.assertTrue(botija.msg('testing'))
		slack_bolt.FakeApp.client.chat_postMessage.assert_called_once_with(
			channel = 'CTEST', text = 'testing',
		)

	def test_msg_error(t):
		slack_bolt.mock(fail = True)
		t.assertFalse(botija.msg('testing'))
		slack_bolt.FakeApp.client.chat_postMessage.assert_called_once_with(
			channel = 'CTEST', text = 'testing',
		)

	def test_main(t):
		t.assertEqual(botija.main(['testing']), 0)
		slack_bolt.FakeApp.client.chat_postMessage.assert_called_once_with(
			channel = 'CTEST', text = 'testing',
		)

	def test_main_error(t):
		slack_bolt.mock(fail = True)
		t.assertEqual(botija.main(['testing']), 0)
		slack_bolt.FakeApp.client.chat_postMessage.assert_called_once_with(
			channel = 'CTEST', text = 'testing',
		)

if __name__ == '__main__':
	unittest.main()
