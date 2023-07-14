#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import logging
import unittest

from contextlib    import contextmanager
from unittest.mock import MagicMock

import wapp

@contextmanager
def mock_start(debug = False):
	m = MagicMock()
	bup_debug   = wapp.debug
	bup_logging = wapp.logging
	try:
		wapp.debug   = debug
		wapp.logging = m.logging
		yield m
	finally:
		wapp.debug   = bup_debug
		wapp.logging = bup_logging

class TestWapp(unittest.TestCase):

	#
	# globals
	#

	def test_defaults(t):
		t.assertFalse(wapp.debug)
		t.assertEqual(wapp.port, 2741)

	#
	# logging
	#

	def test_getLogger(t):
		l = wapp.getLogger('testing')
		t.assertIsInstance(l, logging.Logger)

	#
	# main
	#

	def test_start(t):
		with mock_start() as m:
			wapp.start()
			m.logging.basicConfig.assert_not_called()

	def test_start_debug(t):
		with mock_start(debug = True) as m:
			wapp.start()
			m.logging.basicConfig.assert_called_once_with(
				format = wapp.logfmt_debug,
				level  = m.logging.DEBUG,
			)

	def test_run(t):
		m = MagicMock()
		wapp.run(m)
		m.run.assert_called_once_with(
			host     = '0.0.0.0',
			port     = 2741,
			reloader = False,
			debug    = False,
		)

if __name__ == '__main__':
	unittest.main()
