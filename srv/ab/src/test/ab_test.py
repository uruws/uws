#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

from pathlib import Path

import ab

#-------------------------------------------------------------------------------
# config

class TestConfig(unittest.TestCase):

	def test_defaults(t):
		t.assertEqual(ab.cmdpath,    Path('/usr/bin/ab'))
		t.assertEqual(ab.user_agent, '-HUser-Agent:uwsab')

#-------------------------------------------------------------------------------
# command

default_cmd      = '/usr/bin/ab -n1 -c1 -s7'
default_cmd_list = default_cmd.split(' ')
default_cmd_list.append('-HUser-Agent:uwsab')

full_cmd_list = [
	'/usr/bin/ab', '-n99', '-c99', '-t99', '-s99', '-ppost.t', '-Tc/t',
	'-HUser-Agent:uwsab',
]

class TestCommand(unittest.TestCase):

	def test_str(t):
		t.assertEqual(str(ab.Command()), default_cmd)

	def test_str_id(t):
		c = ab.Command()
		c._id = 'testing'
		t.assertEqual(c.id(), 'testing')
		t.assertEqual(str(c), 'testing: %s' % default_cmd)

	def test_args(t):
		t.assertListEqual(ab.Command().args(), default_cmd_list)

	def test_args_init(t):
		l = default_cmd_list.copy()
		l.append('https://test.domain/path')
		t.assertListEqual(ab.Command('https://test.domain/path').args(), l)

	def test_args_settings(t):
		c = ab.Command()
		c.requests     = 99
		c.concurrency  = 99
		c.timelimit    = 99
		c.timeout      = 99
		c.postfile     = 'post.t'
		c.content_type = 'c/t'
		t.assertListEqual(c.args(), full_cmd_list)

	def test_command_parse(t):
		c = ab.command_parse('testing', default_cmd.strip())
		t.assertIsInstance(c, ab.Command)
		t.assertListEqual(c.args(), default_cmd_list)

	def test_command_parse_user_agent(t):
		c = ab.command_parse('testing', ' '.join(default_cmd_list))
		t.assertListEqual(c.args(), default_cmd_list)

	def test_command_parse_options(t):
		cmd = ' '.join(full_cmd_list)
		c = ab.command_parse('testing', cmd)
		t.assertListEqual(c.args(), full_cmd_list)

	def test_command_parse_args(t):
		l = default_cmd_list.copy()
		l.append('https://test.domain/path')
		cmd = default_cmd.strip()
		cmd += ' https://test.domain/path'
		c = ab.command_parse('testing', cmd)
		t.assertListEqual(c.args(), l)

if __name__ == '__main__':
	unittest.main()
