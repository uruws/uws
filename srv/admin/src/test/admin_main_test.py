#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib    import contextmanager
from unittest.mock import MagicMock

import unittest

import wapp_t

import admin_main

@contextmanager
def mock_bottle():
	bup = admin_main.app
	try:
		admin_main.app = MagicMock()
		with wapp_t.mock() as m:
			yield m
	finally:
		admin_main.app = bup

class TestMain(unittest.TestCase):

	def test_wsgi_application(t):
		app = admin_main.wsgi_application()
		t.assertIs(app, admin_main.app)

	def test_main(t):
		with mock_bottle() as m:
			admin_main.main()
			admin_main.app.run.assert_called_once_with(
				host = '0.0.0.0', port = 2741, reloader = False, debug = False,
			)

if __name__ == '__main__':
	unittest.main()
