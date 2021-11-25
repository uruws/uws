#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

from os import environ

import uwscli_t
import uwscli
import uwscli_conf

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_globals(t):
		t.assertEqual(uwscli.bindir, '/srv/home/uwscli/bin')
		t.assertEqual(uwscli.cmddir, '/srv/uws/deploy/cli')
		t.assertEqual(uwscli.docker_storage, '/srv/docker')
		t.assertEqual(uwscli.docker_storage_min, 10)
		t.assertIsInstance(uwscli.app, dict)
		t.assertIsInstance(uwscli.cluster, dict)
		t.assertEqual(uwscli._user, 'uws')
		t.assertTrue(uwscli._log)
		t.assertDictEqual(uwscli._env,
			{'PATH': '/srv/home/uwscli/bin:/usr/local/bin:/usr/bin:/bin'})
		t.assertEqual(uwscli._cmdTtl, 180)

	def test_environ(t):
		for k, v in uwscli._env.items():
			t.assertEqual(environ[k], v, msg = f"environ['{k}']")

	def test_system(t):
		t.assertEqual(uwscli.system('exit 0'), 0)
		t.assertEqual(uwscli.system('exit 2'), 2)
		t.assertEqual(uwscli.system('test -n "${TESTING}"',
			env = {'TESTING': 'test'}), 0)

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

	def test_ctl(t):
		with uwscli_t.mock_system():
			t.assertEqual(uwscli.ctl('testing'), 0)
			uwscli.system.assert_called_once_with('/usr/bin/sudo -H -n -u uws -- /srv/uws/deploy/cli/app-ctl.sh uws testing')

	def test_nq(t):
		with uwscli_t.mock_system():
			t.assertEqual(uwscli.nq('testing', 'args_t'), 0)
			uwscli.system.assert_called_once_with('/usr/bin/sudo -H -n -u uws -- /srv/uws/deploy/cli/uwsnq.sh uws /srv/uws/deploy/cli/testing args_t')

	def test_run(t):
		with uwscli_t.mock_system():
			t.assertEqual(uwscli.run('testing', 'args_t'), 0)
			uwscli.system.assert_called_once_with('/usr/bin/sudo -H -n -u uws -- /srv/uws/deploy/cli/testing args_t')

	def test_clean_build(t):
		with uwscli_t.mock_system():
			t.assertEqual(uwscli.clean_build('testing', '0.999'), 0)
			uwscli.system.assert_called_once_with('/usr/bin/sudo -H -n -u uws -- /srv/uws/deploy/cli/uwsnq.sh uws /srv/uws/deploy/cli/app-clean-build.sh testing 0.999')

	def test_list_images(t):
		with uwscli_t.mock_check_output():
			t.assertEqual(uwscli.list_images('testing', region = 't-1'), ['mock_output'])
			uwscli.check_output.assert_called_once_with("aws ecr list-images --output text --repository-name uws --region t-1 | grep -F 'test' | awk '{ print $3 }' | sed 's/^test-//' | sort -n")

	def test_list_images_error(t):
		with uwscli_t.mock_check_output(fail = True):
			t.assertEqual(uwscli.list_images('testing'), [])
		t.assertEqual(uwscli_t.err().strip(), '[ERROR] testing list images: mock_output')

if __name__ == '__main__':
	unittest.main()
