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
	chatbot.uwscli_command['testing'] = chatbot.UwscliCmd(
		enable = True,
	)
	return cb

def mock_teardown(cb):
	chatbot.getstatusoutput = cb._bup_getstatusoutput
	chatbot.uwscli_host = cb._bup_uwscli_host
	chatbot.user.clear()
	chatbot.uwscli_command.clear()
	cb._destroy()

#
# config
#

class TestConfig(unittest.TestCase):

	def test_defaults(t):
		t.assertTrue(chatbot.debug)
		t.assertEqual(chatbot.libexec,     Path('/opt/uws/chatbot/libexec'))
		t.assertEqual(chatbot.webapp_port, 2741)

#
# uwscli
#

class TestUwscli(unittest.TestCase):

	def setUp(t):
		t.cb = mock_setup()

	def tearDown(t):
		mock_teardown(t.cb)
		t.cb = None

	def test_defaults(t):
		t.assertEqual(chatbot.uwscli_cmd,    'uwscli.sh')
		t.assertEqual(chatbot.uwscli_host,   'localhost')
		t.assertEqual(chatbot.uwscli_bindir, Path('/srv/home/uwscli/bin'))

	def test_uwscli(t):
		st, out = chatbot.uwscli('UTEST', 'testing')
		t.assertEqual(out, 'mock getstatusoutput')
		t.assertEqual(st, 0)
		t.cb.getstatusoutput.assert_called_once_with('/opt/uws/chatbot/libexec/uwscli.sh localhost testing /srv/home/uwscli/bin/testing')

	def test_uwscli_shell_quote(t):
		st, out = chatbot.uwscli('UTEST', 'testing <@UCHATBOT>')
		t.assertEqual(out, 'mock getstatusoutput')
		t.assertEqual(st, 0)
		t.cb.getstatusoutput.assert_called_once_with("/opt/uws/chatbot/libexec/uwscli.sh localhost testing /srv/home/uwscli/bin/testing '<@UCHATBOT>'")

	def test_uwscli_user_invalid(t):
		st, out = chatbot.uwscli('UINVALID', 'testing')
		t.assertEqual(out, 'unauthorized: UINVALID')
		t.assertEqual(st, -1)

	def test_uwscli_command(t):
		cl = [k for k, c in chatbot.uwscli_command.items() if c.enable]
		t.assertListEqual(cl, [
			'testing',
		])

	def test_uwscli_command_invalid(t):
		with t.assertRaises(chatbot.UwscliCmdError) as cm:
			chatbot.uwscli('UTEST', 'testing-invalid')
		err = cm.exception
		t.assertEqual(err.status, 1)

	def test_uwscli_command_disabled(t):
		chatbot.uwscli_command['testing'].enable = False
		with t.assertRaises(chatbot.UwscliCmdError) as cm:
			chatbot.uwscli('UTEST', 'testing')
		err = cm.exception
		t.assertEqual(err.status, 2)

	def test_uwscli_command_args(t):
		chatbot.uwscli_command['testing'].args = ['--args-test']
		st, out = chatbot.uwscli('UTEST', 'testing')
		t.assertEqual(out, 'mock getstatusoutput')
		t.assertEqual(st, 0)
		t.cb.getstatusoutput.assert_called_once_with('/opt/uws/chatbot/libexec/uwscli.sh localhost testing /srv/home/uwscli/bin/testing --args-test')

if __name__ == '__main__':
	unittest.main()
