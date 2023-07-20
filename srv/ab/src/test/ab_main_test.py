#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib    import contextmanager
from unittest.mock import MagicMock

import unittest

import bottle # type: ignore

import wapp_t

import ab_main
import ab_test

@contextmanager
def mock_bottle():
	bup = ab_main.app
	try:
		ab_main.app = MagicMock()
		with wapp_t.mock() as m:
			yield m
	finally:
		ab_main.app = bup

class TestMain(unittest.TestCase):

	def test_wsgi_application(t):
		app = ab_main.wsgi_application()
		t.assertIs(app, ab_main.app)

	def test_main(t):
		with mock_bottle() as m:
			ab_main.main()
			ab_main.app.run.assert_called_once_with(
				host = '0.0.0.0', port = 2741, reloader = False, debug = False,
			)

class TestViews(unittest.TestCase):

	# /healthz

	def test_healthz(t):
		with wapp_t.mock() as m:
			t.assertEqual(ab_main.healthz(), 'ok')
			t.assertEqual(m.response.content_type, 'text/plain')

	def test_healthz_error(t):
		with ab_test.mock_run(status = 99):
			with t.assertRaises(RuntimeError) as err:
				ab_main.healthz()
			t.assertEqual(str(err.exception), 'ab exit status: 99')

	# /run/

	def test_run(t):
		with wapp_t.mock() as m:
			ab_main.run()
			m.template.assert_called_once_with('ab/run.html')

	# /

	def test_home(t):
		with wapp_t.mock() as m:
			ab_main.home()
			m.template.assert_called_once_with('ab/home.html')

if __name__ == '__main__':
	unittest.main()
