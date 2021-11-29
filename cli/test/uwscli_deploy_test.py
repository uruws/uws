#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib import contextmanager
from configparser import SectionProxy
from pathlib import Path

import unittest
from unittest.mock import MagicMock, call

import uwscli_t
import uwscli_deploy

import uwscli

@contextmanager
def mock(config = 'uwsci.conf', _deploy = True, _deploy_status = 0):
	if _deploy:
		_deploy_bup = uwscli_deploy._deploy
	try:
		uwscli_deploy._cfgfn = f"testdata/{config}"
		if _deploy:
			uwscli_deploy._deploy = MagicMock(return_value = _deploy_status)
		yield
	finally:
		uwscli_deploy._cfgfn = '.uwsci.conf'
		uwscli_deploy._cfgFiles = []
		if _deploy:
			uwscli_deploy._deploy = _deploy_bup

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_globals(t):
		t.assertEqual(uwscli_deploy._cfgfn, '.uwsci.conf')
		t.assertListEqual(uwscli_deploy._cfgFiles, [])
		t.assertDictEqual(uwscli_deploy._ciScripts, {
			0: 'build.sh',
			1: 'check.sh',
			2: 'install.sh',
			3: 'deploy.sh',
			4: 'clean.sh',
		})
		t.assertEqual(uwscli_deploy._scriptTtl, 3600)

	def test_newConfig(t):
		t.assertListEqual(uwscli_deploy._cfgFiles, [])
		c = uwscli_deploy._newConfig()
		t.assertListEqual(uwscli_deploy._cfgFiles, [])
		t.assertIsInstance(c, SectionProxy)
		t.assertIsNone(c.get('testing'))
		t.assertEqual(c.get('testing', 'test'), 'test')
		t.assertEqual(c.get('version', 'UNSET'), '0')
		t.assertEqual(c['ci_dir'], '/home/uws/.ci')

	def test_cfgFiles(t):
		try:
			uwscli_deploy._cfgfn = 'testdata/uwsci.conf'
			c = uwscli_deploy._newConfig()
			t.assertListEqual(uwscli_deploy._cfgFiles, ['testdata/uwsci.conf'])
			t.assertTrue(c.get('testing'))
		finally:
			uwscli_deploy._cfgfn = '.uwsci.conf'
			uwscli_deploy._cfgFiles = []

	def test_read_config_error(t):
		with uwscli_t.mock_system():
			with uwscli_t.mock_check_output():
				with mock(config = 'uwsci_error.conf'):
					with t.assertRaisesRegex(AssertionError, r'^invalid ci_dir: /tmp$'):
						uwscli_deploy.run('testing', '0.999')
				with mock(config = 'uwsci_relpath_error.conf'):
					with t.assertRaisesRegex(AssertionError, r'^invalid ci_dir: /tmp$'):
						uwscli_deploy.run('testing', '0.999')

	def test__deploy(t):
		t.assertEqual(uwscli_deploy._deploy('testing.git', '0.999', '.ci', 3), 0)
		with uwscli_t.mock_system():
			with uwscli_t.mock_check_output():
				t.assertEqual(uwscli_deploy._deploy('testing.git', '0.999', 'testdata/ci', 3), 0)
				uwscli.system.assert_called_once_with('testdata/ci/deploy.sh',
					env = {
						'UWSCLI_REPO': 'testing.git',
						'UWSCLI_REPO_NAME': 'testing.git',
						'UWSCLI_REPO_TAG': '0.999',
					}, timeout = 3)

	def test__deploy_error(t):
		with uwscli_t.mock_system(fail_cmd = 'testdata/ci/deploy.sh'):
				with uwscli_t.mock_check_output():
					t.assertEqual(uwscli_deploy._deploy('testing.git', '0.999',
						'testdata/ci', 3), 99)

	def test__rollback(t):
		with uwscli_t.mock_system():
			uwscli_deploy._rollback('t.git', '0.999', '.ci', 3)
			uwscli.system.assert_called_once_with('git checkout 0.999')

	def test__rollback_cur_tag(t):
		with uwscli_t.mock_check_output():
			with uwscli_t.mock_system():
				with mock(_deploy_status = 99):
					t.assertEqual(uwscli_deploy.run('testing.git', '0.999', cur = '0.333'), 99)
				calls = [
					call('git checkout 0.333'),
				]
				uwscli.system.assert_has_calls(calls)

	def test_run(t):
		with uwscli_t.mock_system():
			with uwscli_t.mock_check_output():
				with mock():
					t.assertEqual(uwscli_deploy.run('testing.git', '0.999'), 0)
					t.assertListEqual(uwscli_deploy._cfgFiles, ['testdata/uwsci.conf'])
					uwscli_deploy._deploy.assert_called_once_with('testing.git', '0.999', '/home/uws/.ci', 3600)
					calls = [
						call('git fetch --prune --prune-tags --tags'),
						call('git checkout 0.999'),
					]
					uwscli.system.assert_has_calls(calls)

	def test_run_no_fetch(t):
		with uwscli_t.mock_system():
			with uwscli_t.mock_check_output():
				with mock():
					t.assertEqual(uwscli_deploy.run('testing.git', '0.999', fetch = False), 0)
					t.assertListEqual(uwscli_deploy._cfgFiles, ['testdata/uwsci.conf'])
					calls = [
						call('git checkout 0.999'),
					]
					uwscli.system.assert_has_calls(calls)

	def test_run_errors(t):
		with mock(_deploy_status = 99):
			with uwscli_t.mock_system():
				with uwscli_t.mock_check_output():
					t.assertEqual(uwscli_deploy.run('testing.git', '0.999'), 99)
		with uwscli_t.mock_check_output():
			with mock(config = 'uwsci_scripts.conf', _deploy = False):
				with uwscli_t.mock_system(status = 99):
					t.assertEqual(uwscli_deploy.run('testing.git', '0.999'), 99)
				with uwscli_t.mock_system(fail_cmd = 'git checkout'):
					t.assertEqual(uwscli_deploy.run('testing.git', '0.999'), 99)

if __name__ == '__main__':
	unittest.main()
