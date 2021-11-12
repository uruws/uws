#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import uwscli_t
import uwscli
import uwscli_conf

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
		t.assertTrue(uwscli._log)

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
		t.assertEqual(uwscli.app_list(), ['testing'])

	def test_app_desc(t):
		try:
			uwscli.app['testing1'] = uwscli_conf.App(True,
				cluster = 'ktest1',
				desc = 'Testing1',
				pod = 'test1',
				build = uwscli_conf.AppBuild('/srv/deploy/Testing1', 'build.sh'),
				deploy = uwscli_conf.AppDeploy('test1'),
			)
			t.assertEqual(uwscli.app_description(), 'available apps:\n  testing  - Testing\n  testing1 - Testing1\n')
		finally:
			del uwscli.app['testing1']

	def test_build_list(t):
		t.assertEqual(uwscli.build_list(), ['testing'])

	def test_build_desc(t):
		t.assertEqual(uwscli.build_description(), 'available apps:\n  testing - Testing\n')

	def test_deploy_list(t):
		t.assertEqual(uwscli.deploy_list(), ['testing'])

	def test_deploy_desc(t):
		t.assertEqual(uwscli.deploy_description(), 'available apps:\n  testing - Testing\n')

if __name__ == '__main__':
	unittest.main()
