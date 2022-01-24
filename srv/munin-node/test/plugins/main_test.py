#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib    import contextmanager
from unittest.mock import MagicMock
from unittest.mock import call

import unittest

import mnpl_t
import main

@contextmanager
def mock_cmd(cmd = {}):
	_bup_cmd = main._cmd.copy()
	try:
		main._cmd = {'testing': True}
		main._cmd.update(cmd)
		yield
	finally:
		main._cmd = None
		main._cmd = _bup_cmd.copy()

class Test(unittest.TestCase):

	def setUp(t):
		mnpl_t.setup()

	def tearDown(t):
		mnpl_t.teardown()

	def test_main_errors(t):
		t.assertEqual(main.run(['']), main.ENOCMD)
		t.assertEqual(main.run(['invalid']), main.EWRONGCMD)

	def test_main(t):
		with mock_cmd():
			t.assertEqual(main.run(['testing']), 0)

if __name__ == '__main__':
	unittest.main()
