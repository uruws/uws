#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from unittest.mock import MagicMock

import unittest

import chatbot_slack

class MockSlack(object):

	def __init__(s):
		s.event = {
			'user': 'UTEST',
		}
		s.body = {
			'event': s.event,
		}
		s.say = MagicMock()

	def _destroy(s):
		s.event.clear()
		s.event = None
		s.say = None

class MockApp(object):

	def __init__(a):
		a._bup_app        = chatbot_slack.app
		a._bup_smh        = chatbot_slack.smh
		a.smh             = MagicMock()
		a.smh.client      = MagicMock()
		a._bup_channel_id = chatbot_slack.channel_id
		a.client          = MagicMock()

	def _destroy(a):
		a._bup_app = None
		a._bup_smh = None

def mock_app_setup() -> MockApp:
	chatbot_slack.app = MockApp()
	chatbot_slack.smh = chatbot_slack.app.smh
	chatbot_slack.channel_id = 'CTESTING'
	return chatbot_slack.app

def mock_app_teardown(app: MockApp):
	chatbot_slack.app = app._bup_app
	chatbot_slack.smh = app._bup_smh
	chatbot_slack.channel_id = app._bup_channel_id
	app._destroy()

class TestEvents(unittest.TestCase):

	def setUp(t):
		t.slack = MockSlack()

	def tearDown(t):
		t.slack._destroy()
		t.slack = None

	def test_event_app_mention(t):
		chatbot_slack.event_app_mention(t.slack.event, t.slack.say)
		t.slack.say.assert_called_once_with('Hello <@UTEST>!!')

	def test_event_app_home_opened(t):
		chatbot_slack.event_app_home_opened(t.slack.body)

	def test_event_message(t):
		chatbot_slack.event_message(t.slack.body)

class TestSocketMode(unittest.TestCase):

	def setUp(t):
		t.app = mock_app_setup()

	def tearDown(t):
		mock_app_teardown(t.app)
		t.app = None

	def test_connect(t):
		chatbot_slack.connect()
		t.app.smh.connect.assert_called_once_with()

	def test_is_healthy(t):
		t.assertTrue(chatbot_slack.is_healthy())

	def test_is_healthy_no_client(t):
		t.app.smh.client = None
		t.assertFalse(chatbot_slack.is_healthy())

	def test_is_healthy_not_connected(t):
		t.app.smh.client.is_connected = MagicMock(return_value = False)
		t.assertFalse(chatbot_slack.is_healthy())

class TestUtils(unittest.TestCase):

	def setUp(t):
		t.app = mock_app_setup()

	def tearDown(t):
		mock_app_teardown(t.app)
		t.app = None

	def test_channel_id(t):
		t.assertEqual(t.app._bup_channel_id, 'C02U5ADHPCJ')
		t.assertEqual(chatbot_slack.channel_id, 'CTESTING')

	def test_msg(t):
		chatbot_slack.msg('testing')
		t.app.client.chat_postMessage.assert_called_once_with(channel = 'CTESTING', text = 'testing')

if __name__ == '__main__':
	unittest.main()
