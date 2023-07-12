#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib    import contextmanager
from unittest.mock import MagicMock

import unittest

import bottle # type: ignore
import ab_main
import ab_test

@contextmanager
def mock_bottle():
	bup = ab_main.app
	bup_resp = ab_main.response
	try:
		ab_main.app = MagicMock()
		ab_main.response = MagicMock()
		yield
	finally:
		ab_main.app = bup
		ab_main.response = bup_resp

class TestMain(unittest.TestCase):

	def test_wsgi_application(t):
		app = ab_main.wsgi_application()
		t.assertIs(app, ab_main.app)

	def test_main(t):
		with mock_bottle():
			ab_main.main()
			ab_main.app.run.assert_called_once_with(
				host = '0.0.0.0', port = 2741, reloader = True, debug = True,
			)

class TestViews(unittest.TestCase):

	def test_healthz(t):
		t.assertEqual(ab_main.healthz(), 'ok')
		t.assertEqual(ab_main.response.content_type, 'text/plain')

	def test_healthz_error(t):
		with ab_test.mock_run(status = 99):
			with t.assertRaises(RuntimeError) as err:
				ab_main.healthz()
			t.assertEqual(str(err.exception), 'ab exit status: 99')

if __name__ == '__main__':
	unittest.main()
