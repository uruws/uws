#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import logging
import unittest

from contextlib    import contextmanager
from unittest.mock import MagicMock

import wapp

@contextmanager
def mock_start():
	m = MagicMock()
	bup_logging = wapp.logging
	try:
		wapp.logging = m.logging
		yield m
	finally:
		wapp.logging = bup_logging

class TestWapp(unittest.TestCase):

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
			wapp.start('testing')
			m.logging.basicConfig.assert_not_called()

	def test_start_debug(t):
		with mock_start() as m:
			wapp.start('testing', debug = True)
			m.logging.basicConfig.assert_called_once_with(
				format = wapp.logfmt_debug,
				level  = m.logging.DEBUG,
			)

if __name__ == '__main__':
	unittest.main()
