#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys
import unittest

from os         import environ
from os         import getcwd
from os         import linesep
from pathlib    import Path
from shutil     import rmtree
from subprocess import CalledProcessError

import uwscli_t
import uwscli
import uwscli_conf
import uwscli_auth
import uwscli_version

from uwscli_user import AppUser

_PATH = '/srv/home/uwscli/bin:/usr/local/bin:/usr/bin:/bin'

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	# internal utils

	def test_globals(t):
		t.assertEqual(uwscli.bindir, '/srv/home/uwscli/bin')
		t.assertEqual(uwscli.cmddir, '/srv/uws/deploy/cli')
		t.assertEqual(uwscli.docker_storage, '/srv/docker')
		t.assertEqual(uwscli.docker_storage_min, 10)
		t.assertIsInstance(uwscli.app, dict)
		t.assertIsInstance(uwscli.cluster, dict)
		t.assertIsInstance(uwscli._user, uwscli_auth.User)
		t.assertEqual(uwscli._user.name, 'uws')
		t.assertDictEqual(uwscli._env, {'PATH': _PATH})
		t.assertEqual(uwscli.system_ttl, 600)

	def test_environ(t):
		for k, v in uwscli._env.items():
			t.assertEqual(environ[k], v, msg = f"environ['{k}']")

	def test_local_conf(t):
		t.assertFalse('local_conf' in uwscli.app.keys())
		t.assertFalse('local_conf' in uwscli.cluster.keys())
		try:
			uwscli._local_conf('./testdata/etc')
			t.assertFalse(uwscli.app['local_conf'].app)
			t.assertDictEqual(uwscli.cluster['local_conf'],
				{'region': 'testing'})
		finally:
			del uwscli.app['local_conf']
			del uwscli.cluster['local_conf']
			sys.path.remove('./testdata/etc')

	def test_vendor_libs(t):
		t.assertListEqual(uwscli._libs, [
			'semver-2.13.0',
		])

	def test_version(t):
		t.assertEqual(uwscli.version(), f"uwscli version {uwscli_version.VERSION}")

	def test_chdir(t):
		cwd = '/home/uws'
		with uwscli.chdir('/tmp'):
			t.assertEqual(getcwd(), '/tmp')
		t.assertEqual(getcwd(), cwd)
		# Path object
		with uwscli.chdir(Path('/tmp')):
			t.assertEqual(getcwd(), '/tmp')

	def test_chdir_error(t):
		with t.assertRaises(SystemExit):
			with uwscli.chdir('/invalid'):
				pass
		with uwscli_t.mock_chdir(fail = True):
			with t.assertRaises(SystemExit) as e:
				with uwscli.chdir('/testing'):
					pass
			err = e.exception
			t.assertEqual(err.args[0], 2)

	def test_mkdir(t):
		try:
			uwscli.mkdir('/tmp/testing_mkdir')
			uwscli.mkdir('/tmp/testing_mkdir') # exists ok
			uwscli.mkdir('/tmp/testing_mkdir/d0/d1/d2') # parents
			uwscli.mkdir(Path('/tmp/testing_mkdir')) # Path object
		finally:
			rmtree('/tmp/testing_mkdir')

	def test_mkdir_errors(t):
		try:
			uwscli.mkdir('/tmp/testing_mkdir')
			with t.assertRaises(FileExistsError):
				uwscli.mkdir('/tmp/testing_mkdir', exist_ok = False)
		finally:
			rmtree('/tmp/testing_mkdir')

	def test_lockf(t):
		p = Path('/tmp/.testing.lock')
		t.assertFalse(p.exists())
		with uwscli.lockf('/tmp/testing') as l:
			t.assertEqual(l.name, '/tmp/.testing.lock')
			t.assertTrue(p.exists())
		t.assertFalse(p.exists())
		# Path object
		with uwscli.lockf(Path('/tmp/testing')) as l:
			t.assertEqual(l.name, '/tmp/.testing.lock')

	def test_lockf_errors(t):
		p = Path('/tmp/.testing.lock')
		# unlock file not found
		with t.assertRaises(FileNotFoundError):
			with uwscli.lockf('/tmp/testing'):
				with uwscli.lockf('/tmp/testing2'):
					p.unlink()
		# lock exists
		with t.assertRaises(FileExistsError):
			with uwscli.lockf('/tmp/testing'):
				with uwscli.lockf('/tmp/testing'):
					pass

	def test__setenv(t):
		env = uwscli._setenv({'TESTING': 'test'})
		t.assertEqual(env.get('TESTING'), 'test')

	def test_system(t):
		e = {'TESTING': '3'}
		t.assertEqual(uwscli.system('exit 0'), 0)
		t.assertEqual(uwscli.system('exit "${TESTING}"', env = e), 3)

	def test_gso(t):
		rc, out = uwscli.gso('echo "${PATH}"')
		t.assertEqual(rc, 0)
		t.assertEqual(out, _PATH)
		rc, out = uwscli.gso('test -n "${TESTING}"')
		t.assertEqual(rc, 1)
		t.assertEqual(out, '')

	def test_check_output(t):
		e = {'TESTING': 'test'}
		t.assertEqual(uwscli.check_output('echo "${TESTING}"', env = e).strip(), 'test')
		with t.assertRaises(CalledProcessError):
			uwscli.check_output('exit 128')

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

	def test_app_groups(t):
		t.assertListEqual(uwscli.app_groups(), ['app', 'testing'])

	def test_app_autobuild(t):
		t.assertEqual(uwscli.autobuild_list(), [])
		uwscli.app['testing'].autobuild = True
		t.assertEqual(uwscli.autobuild_list(), ['testing'])

	def test_app_autobuild_description(t):
		t.assertEqual(uwscli.autobuild_description().strip(), 'available apps:')
		uwscli.app['testing'].autobuild = True
		t.assertEqual(uwscli.autobuild_description().replace('\n', '_N_'),
			'available apps:_N_  testing - Testing_N_')

	def test_app_autobuild_deploy(t):
		t.assertListEqual(uwscli.app['testing'].autobuild_deploy, [])
		t.assertListEqual(uwscli.autobuild_deploy('testing'), [])
		uwscli.app['testing'].autobuild_deploy = ['test-1', 'test-2']
		t.assertListEqual(uwscli.app['testing'].autobuild_deploy,
			['test-1', 'test-2'])
		t.assertListEqual(uwscli.autobuild_deploy('testing'),
			['test-1', 'test-2'])

	def test_build_list(t):
		t.assertEqual(uwscli.build_list(), ['testing'])

	def test_build_desc(t):
		t.assertEqual(uwscli.build_description(), 'available apps:\n  testing - Testing\n')

	def test_build_repo(t):
		uwscli.app['testing'].build.repo = 'testing.git'
		uwscli.app['testing'].build.src = 'app/src'
		t.assertEqual(uwscli.build_repo(), [{
			'app': 'testing',
			'uri': 'testing.git',
			'workdir': '/srv/deploy/Testing/app/src',
		}])

	def test_deploy_list(t):
		t.assertEqual(uwscli.deploy_list(), ['testing'])

	def test_deploy_desc(t):
		t.assertEqual(uwscli.deploy_description(), 'available apps:\n  testing - Testing\n')

	def test_ctl(t):
		with uwscli_t.mock_system():
			t.assertEqual(uwscli.ctl('testing'), 0)
			uwscli.system.assert_called_once_with('/usr/bin/sudo -H -n -u uws -- /srv/uws/deploy/cli/app-ctl.sh uws testing',
				timeout = uwscli.system_ttl)

	def test_nq(t):
		with uwscli_t.mock_system():
			t.assertEqual(uwscli.nq('testing', 'args_t'), 0)
			uwscli.system.assert_called_once_with('/usr/bin/sudo -H -n -u uws -- /srv/uws/deploy/cli/uwsnq.sh uws /srv/uws/deploy/cli/testing args_t',
				timeout = 600)

	def test_run(t):
		with uwscli_t.mock_system():
			t.assertEqual(uwscli.run('testing', 'args_t'), 0)
			uwscli.system.assert_called_once_with('/usr/bin/sudo -H -n -u uws -- /srv/uws/deploy/cli/testing args_t',
				timeout = uwscli.system_ttl)

	def test_clean_build(t):
		with uwscli_t.mock_system():
			t.assertEqual(uwscli.clean_build('testing'), 0)
			uwscli.system.assert_called_once_with('/usr/bin/sudo -H -n -u uws -- /srv/uws/deploy/cli/uwsnq.sh uws /srv/uws/deploy/cli/app-clean-build.sh testing',
				timeout = 600)

	# aws utils

	def test_list_images(t):
		with uwscli_t.mock_check_output():
			t.assertEqual(uwscli.list_images('testing', region = 't-1'), ['mock_output'])
			uwscli.check_output.assert_called_once_with("aws ecr list-images --output text --repository-name uws --region t-1 | grep -F 'test' | awk '{ print $3 }' | sed 's/^test-//' | sort -V")

	def test_list_images_error(t):
		with uwscli_t.mock_check_output(fail = True):
			t.assertEqual(uwscli.list_images('testing'), [])
		t.assertEqual(uwscli_t.err().strip(), '[ERROR] testing list images: mock_output')
		with uwscli_t.mock_check_output():
			uwscli.app['testerror'] = uwscli_conf.App(False)
			t.assertEqual(uwscli.list_images('testerror'), [])

	# git utils

	def test_git_clone(t):
		with uwscli_t.mock_system():
			t.assertEqual(uwscli.git_clone('testing.git'), 0)
			uwscli.system.assert_called_once_with('git clone testing.git')

	def test_git_fetch(t):
		with uwscli_t.mock_system():
			t.assertEqual(uwscli.git_fetch(), 0)
			uwscli.system.assert_called_once_with('git fetch --prune --prune-tags --tags')
		with uwscli_t.mock_system():
			t.assertEqual(uwscli.git_fetch(workdir = 'src/test'), 0)
			uwscli.system.assert_called_once_with('git -C src/test fetch --prune --prune-tags --tags')

	def test_git_checkout(t):
		with uwscli_t.mock_system():
			t.assertEqual(uwscli.git_checkout('0.999'), 0)
			uwscli.system.assert_called_once_with('git checkout 0.999')
		with uwscli_t.mock_system():
			t.assertEqual(uwscli.git_checkout('0.999', workdir = 'src/test'), 0)
			uwscli.system.assert_called_once_with('git -C src/test checkout 0.999')

	def test_git_deploy(t):
		with uwscli_t.mock_uwscli_deploy():
			t.assertEqual(uwscli.git_deploy('testing.git', '0.999'), 0)
			uwscli.uwscli_deploy.run.assert_called_once_with('testing.git', '0.999')

	def test_git_describe(t):
		with uwscli_t.mock_check_output():
			t.assertEqual(uwscli.git_describe(), 'mock_output')
			uwscli.check_output.assert_called_once_with('git describe --always')
		with uwscli_t.mock_check_output():
			t.assertEqual(uwscli.git_describe(workdir = 'src/test'), 'mock_output')
			uwscli.check_output.assert_called_once_with('git -C src/test describe --always')

	def test_git_tag_list(t):
		with uwscli_t.mock_check_output():
			t.assertListEqual(uwscli.git_tag_list(), ['mock_output'])
			uwscli.check_output.assert_called_once_with('git tag --list')
		with uwscli_t.mock_check_output(output = linesep.join(['t0', 't1', 't2', 't3'])):
			t.assertListEqual(uwscli.git_tag_list(), ['t0', 't1', 't2', 't3'])
		with uwscli_t.mock_check_output():
			t.assertListEqual(uwscli.git_tag_list(workdir = 'src/test'), ['mock_output'])
			uwscli.check_output.assert_called_once_with('git -C src/test tag --list')

	# app users

	def test_user_get(t):
		with uwscli_t.mock_users():
			u = uwscli.user_get('tuser')
			t.assertIsInstance(u, AppUser)
			t.assertEqual(u.uid, 5000)
			t.assertEqual(u.name, 'tuser')

	def test_user_get_not_found(t):
		t.assertIsNone(uwscli.user_get('testing'))

if __name__ == '__main__':
	unittest.main()
