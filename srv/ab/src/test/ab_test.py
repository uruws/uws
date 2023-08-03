#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

from pathlib import Path

import wapp_t

import ab

#-------------------------------------------------------------------------------
# config

class TestConfig(unittest.TestCase):

	def test_defaults(t):
		t.assertEqual(ab.cmdpath, '/opt/uws/ab/abrun.py')

#-------------------------------------------------------------------------------
# command

default_cmd      = '/opt/uws/ab/abrun.py -s7 -c1 -n1'
default_cmd_list = default_cmd.split(' ')

full_cmd_list = [
	'/opt/uws/ab/abrun.py', '-t99', '-s99', '-c99', '-n99', '-ppost.t', '-Tc/t',
]

nqdir = '/opt/uws/ab/test/data/nq'

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
		cmd += ' -Htesting https://test.domain/path'
		c = ab.command_parse('testing', cmd)
		t.assertListEqual(c.args(), l)

	def test_command_form(t):
		f = ab.CommandForm()
		t.assertDictEqual(dict(f.items()), {
			'concurrency': '1',
			'requests':    '1',
			'timelimit':   '0',
			'timeout':     '7',
		})

	def test_parse(t):
		with wapp_t.mock(nqdir = nqdir) as m:
			c = ab.Command()
			c._id = '189b8021ea5.24'
			c._parse()
			t.assertEqual(c.command(),
				'exec /usr/bin/nq -q /opt/uws/ab/abrun.py -n1 -c1 -s7 https://sarmiento.uws.talkingpts.org/iqvm39mcpbkFJzucEAFETVpbhoqAvpqt-healthz.txt')
			t.assertEqual(c.start_time(), 'Wed Aug  2 20:48:14 2023')
			t.assertEqual(c.end_time(),   'Wed Aug  2 20:48:15 2023')
			t.assertEqual(c.concurrency,  1)
			t.assertEqual(c.requests,     1)
			t.assertEqual(c.took(),       1.035)
			t.assertEqual(c.failed(),     0)
			t.assertEqual(c.rps(),        0.97)
			t.assertEqual(c.tpr(),        1034.975)

if __name__ == '__main__':
	unittest.main()
