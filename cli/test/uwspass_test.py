#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys
import unittest

import uwscli_t

from contextlib    import contextmanager
from random        import random
from unittest.mock import MagicMock

sys.path.insert(0, '/srv/uws/deploy/cli')
import uwspass

@contextmanager
def mock(pwfail = False):
	bup_getpass = uwspass.getpass
	bup_save = uwspass._save
	def _getpass(*args, **kwargs):
		if pwfail:
			return str(random())
		return 'testing'
	try:
		uwspass.getpass = MagicMock(side_effect = _getpass)
		uwspass._save = MagicMock()
		with uwscli_t.mock_users():
			yield
	finally:
		uwspass.getpass = bup_getpass
		uwspass._save = bup_save

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_args_error(t):
		t.assertEqual(uwspass.main(['--user', 'invalid']), 8)

	def test_main(t):
		with mock():
			t.assertEqual(uwspass.main(['--user', 'tuser']), 0)

	def test_password_error(t):
		with mock(pwfail = True):
			t.assertEqual(uwspass.main(['--user', 'tuser']), 9)

if __name__ == '__main__':
	unittest.main()
