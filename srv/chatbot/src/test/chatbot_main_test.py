#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib    import contextmanager
from unittest.mock import MagicMock

import unittest
import chatbot_slack_test

import bottle
import chatbot_main

@contextmanager
def mock_start():
	bup = chatbot_main.start
	try:
		chatbot_main.start = MagicMock()
		yield
	finally:
		chatbot_main.start = bup

class Test(unittest.TestCase):

	def setUp(t):
		t.app = chatbot_slack_test.mock_app_setup()

	def tearDown(t):
		chatbot_slack_test.mock_app_teardown(t.app)
		t.app = None

	def test_start(t):
		t.app.client_response = {'mock': 'chatbot_main.start'}
		chatbot_main.start()
		t.app.smh.connect.assert_called_once_with()
		t.app.client.chat_postMessage.assert_called_once_with(channel = 'CTESTING', text = 'connected')

	def test_getapp(t):
		with mock_start():
			app = chatbot_main.getapp()
			t.assertIs(app, bottle.app)

if __name__ == '__main__':
	unittest.main()
