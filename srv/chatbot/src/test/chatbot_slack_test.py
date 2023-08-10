#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from unittest.mock import MagicMock
from unittest.mock import call

import unittest

import chatbot_test
import chatbot_msg_test

import chatbot
import chatbot_slack

#-------------------------------------------------------------------------------
# mock

class MockSlack(object):

	def __init__(s):
		s.thread_ts = '1674248319.693579'
		s.event = {
			'text':      'testing',
			'thread_ts': s.thread_ts,
			'user':      'UTEST',
		}
		s.body = {
			'event': s.event,
		}
		s.say = MagicMock()

	def _destroy(s):
		s.event.clear()
		s.event = None
		s.body.clear()
		s.body = None
		s.say = None

	def mock_app_mention(s):
		s.event['thread_ts'] = None
		s.event['ts'] = s.thread_ts
		s.event['text'] = '<@UBOT> testing'

class MockApp(object):

	def __init__(a):
		a._bup_app                = chatbot_slack.app
		a._bup_smh                = chatbot_slack.smh
		a.smh                     = MagicMock()
		a.smh.client              = MagicMock()
		a._bup_channel_id         = chatbot_slack.channel_id
		a.client_response         = {'mock': 'client_response'}
		a.client                  = MagicMock()
		a.client.chat_postMessage = MagicMock(side_effect = a.mock_client_response)
		a.client.files_upload     = MagicMock(side_effect = a.mock_client_response)

	def _destroy(a):
		a._bup_app = None
		a._bup_smh = None

	def mock_client_response(a, *args, **kwargs):
		return a.client_response

def mock_app_setup():
	chatbot_slack.app = MockApp()
	chatbot_slack.smh = chatbot_slack.app.smh
	chatbot_slack.channel_id = 'CTESTING'
	return chatbot_slack.app

def mock_app_teardown(app):
	chatbot_slack.app = app._bup_app
	chatbot_slack.smh = app._bup_smh
	chatbot_slack.channel_id = app._bup_channel_id
	app._destroy()

#-------------------------------------------------------------------------------
# utils

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

#-------------------------------------------------------------------------------
# events

class TestEvents(unittest.TestCase):

	def setUp(t):
		t.app = mock_app_setup()
		t.slack = MockSlack()
		t.cb = chatbot_test.mock_setup()

	def tearDown(t):
		t.slack._destroy()
		t.slack = None
		chatbot_test.mock_teardown(t.cb)
		t.cb = None
		mock_app_teardown(t.app)
		t.app = None

	def test_event_app_home_opened(t):
		chatbot_slack.event_app_home_opened(t.slack.body)

	def test_event_app_mention(t):
		t.slack.mock_app_mention()
		chatbot_slack.event_app_mention(t.slack.event, t.slack.say)
		t.slack.say.assert_called_once_with(
			'<@UTEST>: testing\n```mock getstatusoutput```', thread_ts = t.slack.thread_ts,
		)

	def test_event_app_mention_uwscli_failed(t):
		t.slack.mock_app_mention()
		t.cb.getstatusoutput.return_value = (99, 'mock error')
		chatbot_slack.event_app_mention(t.slack.event, t.slack.say)
		t.slack.say.assert_called_once_with(
			'<@UTEST>: [ERROR] testing\n```mock error```', thread_ts = t.slack.thread_ts,
		)

	def test_event_app_mention_empty(t):
		t.slack.mock_app_mention()
		t.slack.event['text'] = '<@UBOT>'
		chatbot_slack.event_app_mention(t.slack.event, t.slack.say)
		t.slack.say.assert_called_once_with(
			'<@UTEST>: what do you mean?', thread_ts = t.slack.thread_ts,
		)

	def test_event_message(t):
		chatbot_slack.event_message(t.slack.body, t.slack.say)
		t.slack.say.assert_called_once_with(
			'testing\n```mock getstatusoutput```', thread_ts = t.slack.thread_ts,
		)

	def test_event_message_ignore(t):
		t.slack.event['thread_ts'] = None
		chatbot_slack.event_message(t.slack.body, t.slack.say)
		t.slack.say.assert_not_called()

	def test_event_message_uwscli_failed(t):
		t.cb.getstatusoutput.return_value = (99, 'mock error')
		chatbot_slack.event_message(t.slack.body, t.slack.say)
		t.slack.say.assert_called_once_with(
			'[ERROR] testing\n```mock error```', thread_ts = t.slack.thread_ts,
		)

	def test_event_message_uwscli_ignore(t):
		def _fail(*args, **kwargs):
			raise chatbot.UwscliCmdError(99, 'mock uwscli ignore')
		t.cb.getstatusoutput.side_effect = _fail
		chatbot_slack.event_message(t.slack.body, t.slack.say)
		t.slack.say.assert_not_called()

	def test_message_invalid_command(t):
		def _fail(*args, **kwargs):
			raise chatbot.UwscliCmdError(99, 'mock uwscli ignore')
		t.cb.getstatusoutput.side_effect = _fail
		typ = chatbot_slack._message(t.slack.event, t.slack.say)
		t.assertEqual(typ, 'error')
		t.slack.say.assert_not_called()

	def test_message_invalid_command_mention(t):
		def _fail(*args, **kwargs):
			raise chatbot.UwscliCmdError(99, 'mock uwscli ignore')
		t.cb.getstatusoutput.side_effect = _fail
		t.slack.event['text'] = '<@UBOT> testing'
		typ = chatbot_slack._message(t.slack.event, t.slack.say, mention = True)
		t.assertEqual(typ, 'error')
		t.slack.say.assert_called_once_with(
			'<@UTEST>: invalid command: testing', thread_ts = t.slack.thread_ts,
		)

	def test_message_attach(t):
		with chatbot_msg_test.mock(max_bytes = 5):
			t.cb.getstatusoutput.return_value = (0, 'attach1\nattach2\nattach3\n')
			typ = chatbot_slack._message(t.slack.event, t.slack.say)
			t.assertEqual(typ, 'attach')
			t.slack.say.assert_not_called()
			t.app.client.files_upload.assert_called_once_with(
				channels='CTESTING',
				thread_ts='1674248319.693579',
				content='attach1\nattach2\nattach3',
				initial_comment='testing',
				filetype='text/plain',
				title='output.txt',
				filename='output.txt',
			)

#-------------------------------------------------------------------------------
# socket mode handler

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

if __name__ == '__main__':
	unittest.main()
