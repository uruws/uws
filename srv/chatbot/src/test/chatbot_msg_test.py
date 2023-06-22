#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import chatbot_msg

class TestChatbotMsg(unittest.TestCase):

	def test_defaults(t):
		t.assertEqual(chatbot_msg.max_bytes, 3500)

if __name__ == '__main__':
	unittest.main()
