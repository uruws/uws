#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

from contextlib    import contextmanager
from unittest.mock import MagicMock

import chatbot_msg

@contextmanager
def mock(max_bytes = 100):
	bup_max_bytes = chatbot_msg.max_bytes
	try:
		chatbot_msg.max_bytes = max_bytes
		yield
	finally:
		chatbot_msg.max_bytes = bup_max_bytes

class TestChatbotMsg(unittest.TestCase):

	def test_defaults(t):
		t.assertEqual(chatbot_msg.max_bytes, 3500)

	def test_msgadd(t):
		l = []
		chatbot_msg._msgadd(l, ['output'], 'testing', 1, 1)
		t.assertListEqual(l, ['testing\n```output```'])

	def test_msgadd_empty(t):
		l = []
		chatbot_msg._msgadd(l, [], 'testing', 1, 1)
		t.assertListEqual(l, ['testing\n```[empty]```'])

	def test_msgadd_lines(t):
		l = []
		chatbot_msg._msgadd(l, ['out1', 'out2'], 'testing', 1, 2)
		t.assertListEqual(l, ['testing [1/2]\n```out1\nout2```'])

	def test_parse(t):
		l = chatbot_msg.parse('testing', 'output')
		t.assertListEqual(l, ['testing\n```output```'])

	def test_parse_empty(t):
		l = chatbot_msg.parse('testing', '')
		t.assertListEqual(l, ['testing\n```[empty]```'])

	def test_parse_multi_lines(t):
		with mock(max_bytes = 5):
			l = chatbot_msg.parse('testing', 'out1\nout2\nout3\n')
			t.assertListEqual(l, [
				'testing [1/3]\n```out1```',
				'testing [2/3]\n```out2```',
				'testing [3/3]\n```out3```',
			])

if __name__ == '__main__':
	unittest.main()
