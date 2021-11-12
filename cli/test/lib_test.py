#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import uwscli_t
import uwscli

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_globals(t):
		t.assertEqual(uwscli.bindir, '/srv/home/uwscli/bin')
		t.assertEqual(uwscli.cmddir, '/srv/uws/deploy/cli')
		t.assertEqual(uwscli.docker_storage, '/srv/docker/lib')
		t.assertEqual(uwscli.docker_storage_min, 10*1024*1024)
		t.assertIsInstance(uwscli.app, dict)
		t.assertIsInstance(uwscli.cluster, dict)
		t.assertEqual(uwscli._user, 'uws')

	def test_system(t):
		t.assertEqual(uwscli.system('exit 0'), 0)
		t.assertEqual(uwscli.system('exit 2'), 2)

	def test_log(t):
		uwscli.log('test', 'ing', sep = '')
		t.assertEqual(uwscli_t.out().strip(), 'testing')
		uwscli.log('testing2')
		t.assertEqual(uwscli_t.out().strip(), 'testing2')

	def test_log_disable(t):
		with uwscli_t.log_disable():
			uwscli.log('testing3')
		t.assertEqual(uwscli_t.out().strip(), '')

	def test_error(t):
		uwscli.error('test', 'ing')
		t.assertEqual(uwscli_t.err().strip(), 'test ing')
		with uwscli_t.log_disable():
			# errors should print anyway
			uwscli.error('testing2')
		t.assertEqual(uwscli_t.err().strip(), 'testing2')

	def test_app_list(t):
		t.assertEqual(uwscli.app_list(), ['testing', 'testing1'])

	def test_app_desc(t):
		t.assertEqual(uwscli.app_description(), 'available apps:\n  testing  - Testing\n  testing1 - Testing1\n')

if __name__ == '__main__':
	unittest.main()
