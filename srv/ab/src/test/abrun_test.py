#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

from contextlib    import contextmanager
from unittest.mock import MagicMock
from unittest.mock import call

import abrun

@contextmanager
def mock(status = 0):
	bup_run   = abrun._run
	bup_outfh = abrun._outfh
	try:
		m = MagicMock()
		abrun._run = m.run
		m.run.return_value = m.proc
		m.proc.returncode = status
		abrun._outfh = m.outfh
		yield m
	finally:
		abrun._run   = bup_run
		abrun._outfh = bup_outfh

class TestABRun(unittest.TestCase):

	def test_settings(t):
		t.assertEqual(abrun.cmdpath,    '/usr/bin/ab')
		t.assertEqual(abrun.user_agent, '-HUser-Agent:uwsab')

	def test_run(t):
		t.assertEqual(abrun._run('/usr/bin/false').returncode, 1)

	def test_main(t):
		with mock() as m:
			t.assertEqual(abrun.main(), 0)

	def test_main_error(t):
		with mock(status = 99) as m:
			t.assertEqual(abrun.main(), 99)

if __name__ == '__main__':
	unittest.main()
