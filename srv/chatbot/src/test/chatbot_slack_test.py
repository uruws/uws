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
		s.say = MagicMock()

	def _destroy(s):
		s.event.clear()
		s.event = None
		s.say = None

class Test(unittest.TestCase):

	def setUp(t):
		t.slack = MockSlack()

	def tearDown(t):
		t.slack._destroy()
		t.slack = None

	def test_event_app_mention(t):
		chatbot_slack.event_app_mention(t.slack.event, t.slack.say)
		t.slack.say.assert_called_once_with('Hello <@UTEST>!!')

if __name__ == '__main__':
	unittest.main()
