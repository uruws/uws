#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

from pathlib import Path

import ab

#
# config
#

class TestConfig(unittest.TestCase):

	def test_defaults(t):
		t.assertEqual(ab.cmdpath, Path('/usr/bin/ab'))

#
# command
#

class TestCommand(unittest.TestCase):

	def test_args(t):
		t.assertListEqual(ab.Command().args(),
			['/usr/bin/ab', '-n1', '-c1', '-s7', '-HUser-Agent:uwsab'])

	def test_args_init(t):
		t.assertListEqual(ab.Command('https://test.domain/uri').args(),
			['/usr/bin/ab', '-n1', '-c1', '-s7', '-HUser-Agent:uwsab',
				'https://test.domain/uri'])

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
			'-HUser-Agent:uwsab',
		])

if __name__ == '__main__':
	unittest.main()
