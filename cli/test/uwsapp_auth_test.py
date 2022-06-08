#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib import contextmanager

from unittest.mock import call

import unittest
import uwscli_t

import uwscli
import uwsapp_auth # type: ignore

@contextmanager
def mock():
	with uwscli_t.mock_users():
		with uwscli_t.mock_system():
			yield

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_main(t):
		calls = [
			call('/usr/bin/install -v -d -m 0750 -u uws -g uws /run/uwscli/auth/f78d7d8e-b8cb-5613-95d2-eb1d440a6b0e'),
		]
		with mock():
			t.assertEqual(uwsapp_auth.main(), 0)
			uwscli.system.assert_has_calls(calls)
			t.assertEqual(uwscli.system.call_count, len(calls))

if __name__ == '__main__':
	unittest.main()
