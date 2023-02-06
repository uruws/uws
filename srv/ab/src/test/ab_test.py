#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib    import contextmanager
from unittest.mock import MagicMock

import unittest
import subprocess

from pathlib import Path

import ab

@contextmanager
def mock_cmdpath(cmd: str):
	bup = ab.cmdpath.as_posix()
	try:
		ab.cmdpath = Path(cmd)
		yield ab.Command()
	finally:
		ab.cmdpath = Path(bup)

@contextmanager
def mock_subprocess(status: int = 0, timeout: bool = False):
	bup = ab.subprocess.run
	def _timeout(*args, **kwargs):
		raise subprocess.TimeoutExpired('mock_timeout', 99)
	try:
		if timeout:
			ab.subprocess.run = MagicMock(side_effect = _timeout)
		else:
			ab.subprocess.run = MagicMock(return_value = status)
		yield
	finally:
		ab.subprocess.run = bup

#
# config
#

class TestConfig(unittest.TestCase):

	def test_defaults(t):
		t.assertTrue(ab.debug)
		t.assertEqual(ab.webapp_port, 2741)
		t.assertEqual(ab.cmdpath,     Path('/usr/bin/ab'))

#
# command
#

class TestCommand(unittest.TestCase):

	def test_args(t):
		t.assertListEqual(ab.Command().args(), ['/usr/bin/ab', '-HUser-Agent: uwsab'])

	def test_args_init(t):
		t.assertListEqual(ab.Command('-a', '-b', 123).args(),
			['/usr/bin/ab', '-a', '-b', '123', '-HUser-Agent: uwsab'])

	def test_args_settings(t):
		c = ab.Command()
		c.requests     = 99
		c.concurrency  = 99
		c.timelimit    = 99
		c.timeout      = 99
		c.postfile     = 'post.t'
		c.content_type = 'c/t'
		t.assertListEqual(c.args(), [
			'/usr/bin/ab', '-n99', '-c99', '-t99', '-s99', '-ppost.t', '-Tc/t',
			'-HUser-Agent: uwsab',
		])

#
# api
#

class TestApi(unittest.TestCase):

	def test_run(t):
		with mock_cmdpath('/bin/true') as cmd:
			t.assertEqual(ab.run(cmd), 0)
		with mock_subprocess():
			t.assertEqual(ab.run(cmd), 0)

	def test_run_fail(t):
		with mock_cmdpath('/bin/false') as cmd:
			t.assertEqual(ab.run(cmd), 1)

	def test_run_timeout(t):
		with mock_subprocess(timeout = True):
			cmd = ab.Command('10')
			cmd.cmdpath = '/bin/sleep'
			cmd.timelimit = 1
			t.assertEqual(ab.run(cmd, timeout = 0), 9)

if __name__ == '__main__':
	unittest.main()
