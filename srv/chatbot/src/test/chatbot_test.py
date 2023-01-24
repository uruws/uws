#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from unittest.mock import MagicMock

import unittest

from pathlib import Path

import chatbot

#
# mock
#

class MockChatbot(object):

	def __init__(b):
		b._destroy_done = False
		b._bup_getstatusoutput = chatbot.getstatusoutput
		b.getstatusoutput = MagicMock(return_value = (0, 'mock getstatusoutput'))
		b._bup_uwscli_host = chatbot.uwscli_host

	def _destroy(b):
		if not b._destroy_done:
			b._destroy_done = True
			b._bup_getstatusoutput = None
			b.getstatusoutput = None

def mock_setup():
	cb = MockChatbot()
	chatbot.getstatusoutput = cb.getstatusoutput
	chatbot.uwscli_host = 'localhost'
	chatbot.user['UTEST'] = chatbot.User(
		name = 'testing',
	)
	return cb

def mock_teardown(cb):
	chatbot.getstatusoutput = cb._bup_getstatusoutput
	chatbot.uwscli_host = cb._bup_uwscli_host
	del chatbot.user['UTEST']
	cb._destroy()

#
# config
#

class TestConfig(unittest.TestCase):

	def test_defaults(t):
		t.assertEqual(chatbot.libexec,     Path('/opt/uws/chatbot/libexec'))
		t.assertEqual(chatbot.uwscli_cmd,  'uwscli.sh')
		t.assertEqual(chatbot.uwscli_host, 'chatbotdev.uws.talkingpts.org')

#
# utils
#

class TestUtils(unittest.TestCase):

	def setUp(t):
		t.cb = mock_setup()

	def tearDown(t):
		mock_teardown(t.cb)
		t.cb = None

	def test_uwscli(t):
		st, out = chatbot.uwscli('UTEST', 'testing')
		t.assertEqual(out, 'mock getstatusoutput')
		t.assertEqual(st, 0)
		t.cb.getstatusoutput.assert_called_once_with('/opt/uws/chatbot/libexec/uwscli.sh localhost testing testing')

	def test_uwscli_shell_quote(t):
		st, out = chatbot.uwscli('UTEST', '<@UCHATBOT> testing')
		t.assertEqual(out, 'mock getstatusoutput')
		t.assertEqual(st, 0)
		t.cb.getstatusoutput.assert_called_once_with("/opt/uws/chatbot/libexec/uwscli.sh localhost testing '<@UCHATBOT>' testing")

	def test_uwscli_invalid_user(t):
		st, out = chatbot.uwscli('UINVALID', 'testing')
		t.assertEqual(out, 'unauthorized')
		t.assertEqual(st, -1)

if __name__ == '__main__':
	unittest.main()
