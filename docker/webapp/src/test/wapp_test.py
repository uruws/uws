#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import logging
import unittest

from unittest.mock import call

import wapp_t
import wapp

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
		with wapp_t.mock_start() as m:
			wapp.start(m.app)
			m.logging.basicConfig.assert_not_called()
			m.app.get.assert_called()

	def test_start_debug(t):
		with wapp_t.mock_start(debug = True) as m:
			wapp.start(m.app)
			m.logging.basicConfig.assert_called_once_with(
				format = wapp.logfmt_debug,
				level  = m.logging.DEBUG,
			)

	def test_run(t):
		with wapp_t.mock() as m:
			wapp.run(m.app)
			m.app.run.assert_called_once_with(
				host     = '0.0.0.0',
				port     = 2741,
				reloader = False,
				debug    = False,
			)

if __name__ == '__main__':
	unittest.main()
