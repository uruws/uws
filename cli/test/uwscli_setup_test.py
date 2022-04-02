#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from unittest.mock import call

import unittest
import uwscli_t

import uwscli
import uwscli_setup # type: ignore

_env = {'PATH': '/bin:/usr/bin:/sbin:/usr/sbin'}

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_main(t):
		calls = [
			call('/srv/home/uwscli/sbin/uwscli_setup.sh', env = _env),
			call('/srv/home/uwscli/sbin/uwscli_admin.sh', env = _env),
			call('/srv/home/uwscli/sbin/uwscli_operator.sh', env = _env),
			call('/srv/home/uwscli/sbin/uwscli_app.sh app testing', env = _env),
		]
		with uwscli_t.mock_system():
			t.assertEqual(uwscli_setup.main(), 0)
			uwscli.system.assert_has_calls(calls)
			t.assertEqual(uwscli.system.call_count, len(calls))

if __name__ == '__main__':
	unittest.main()
