#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib import contextmanager

from unittest.mock import call
from unittest.mock import MagicMock

import unittest
import uwscli_t

import uwscli
import uwscli_user
import uwsapp_auth # type: ignore

@contextmanager
def mock():
	jsd_bup = uwsapp_auth._json_dump
	try:
		with uwscli_t.mock_users():
			uwscli_user.user['tuser'].username = 'tuser@devel.uwscli.local'
			with uwscli_t.mock_system():
				uwsapp_auth._json_dump = MagicMock(return_value = None)
				yield
	finally:
		uwsapp_auth._json_dump = jsd_bup

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_main(t):
		calls = [
			call('/usr/bin/install -v -d -m 0750 -o uws -g uws /run/uwscli/auth/f78d7d8e-b8cb-5613-95d2-eb1d440a6b0e'),
			call('/usr/bin/install -v -m 0640 -o uws -g uws /run/uwscli/auth/f78d7d8e-b8cb-5613-95d2-eb1d440a6b0e/meta.json.new /run/uwscli/auth/f78d7d8e-b8cb-5613-95d2-eb1d440a6b0e/meta.json'),
			call('/usr/bin/install -v -m 0640 -o uws -g uws /run/uwscli/auth/f78d7d8e-b8cb-5613-95d2-eb1d440a6b0e/apps.json.new /run/uwscli/auth/f78d7d8e-b8cb-5613-95d2-eb1d440a6b0e/apps.json'),
		]
		with mock():
			t.assertEqual(uwsapp_auth.main(), 0)
			uwscli.system.assert_has_calls(calls)
			t.assertEqual(uwscli.system.call_count, len(calls))

	def test_user_remove(t):
		calls = [
			call('/usr/bin/rm -rf /run/uwscli/auth/f78d7d8e-b8cb-5613-95d2-eb1d440a6b0e'),
		]
		with mock():
			uwscli_user.user['tuser'].remove = True
			t.assertEqual(uwsapp_auth.main(), 0)
			uwscli.system.assert_has_calls(calls)
			t.assertEqual(uwscli.system.call_count, len(calls))

if __name__ == '__main__':
	unittest.main()
