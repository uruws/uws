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
def mock(config = 'uwsci.conf', _run = True, _run_status = 0):
	if _run:
		_run_bup = uwscli_deploy._run
	try:
		uwscli_deploy._cfgfn = f"testdata/{config}"
		if _run:
			uwscli_deploy._run = MagicMock(return_value = _run_status)
		yield
	finally:
		uwscli_deploy._cfgfn = '.uwsci.conf'
		uwscli_deploy._cfgFiles = []
		if _run:
			uwscli_deploy._run = _run_bup

class Test(unittest.TestCase):

	def setUp(t):
		uwscli_t.mock()

	def test_globals(t):
		t.assertEqual(uwscli_deploy._cfgfn, '.uwsci.conf')
		t.assertListEqual(uwscli_deploy._cfgFiles, [])

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
		with mock(config = 'uwsci_error.conf'):
			with t.assertRaisesRegex(AssertionError, r'^invalid ci_dir: /tmp$'):
				uwscli_deploy.run('testing', '0.999')
		with mock(config = 'uwsci_relpath_error.conf'):
			with t.assertRaisesRegex(AssertionError, r'^invalid ci_dir: /tmp$'):
				uwscli_deploy.run('testing', '0.999')

	def test_ciScripts(t):
		t.assertDictEqual(uwscli_deploy._ciScripts, {
			0: 'build.sh',
			1: 'check.sh',
			2: 'install.sh',
			3: 'deploy.sh',
			4: 'clean.sh',
		})

	def test__run(t):
		t.assertEqual(uwscli_deploy._run('testing.git', '0.999',
			Path('test.sh')), 0)
		with mock(config = 'uwsci_scripts.conf', _run = False):
			with uwscli_t.mock_system():
				t.assertEqual(uwscli_deploy.run('testing.git', '0.999'), 0)
				t.assertListEqual(uwscli_deploy._cfgFiles,
					['testdata/uwsci_scripts.conf'])
				uwscli.system.assert_called_once_with('/home/uws/testdata/ci/deploy.sh',
					env = {
						'UWSCLI_REPO': 'testing.git',
						'UWSCLI_REPO_NAME': 'testing.git',
						'UWSCLI_REPO_TAG': '0.999',
					})

	def test_run(t):
		_run_calls = []
		for i in sorted(uwscli_deploy._ciScripts.keys()):
			script = uwscli_deploy._ciScripts[i]
			_run_calls.append(call('testing.git', '0.999',
				Path(f"/home/uws/.ci/{script}")))
		with mock():
			t.assertEqual(uwscli_deploy.run('testing.git', '0.999'), 0)
			t.assertListEqual(uwscli_deploy._cfgFiles, ['testdata/uwsci.conf'])
			uwscli_deploy._run.assert_has_calls(_run_calls)

	def test_run_errors(t):
		with mock(_run_status = 99):
			t.assertEqual(uwscli_deploy.run('testing.git', '0.999'), 99)
		with mock(config = 'uwsci_scripts.conf', _run = False):
			with uwscli_t.mock_system(status = 99):
				t.assertEqual(uwscli_deploy.run('testing.git', '0.999'), 99)

if __name__ == '__main__':
	unittest.main()
