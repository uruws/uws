#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib import contextmanager

import unittest
from unittest.mock import MagicMock

import deploy

@contextmanager
def mock_mods():
	_bup_generation = deploy.deploy_generation
	_bup_condition = deploy.deploy_condition
	_bup_status = deploy.deploy_status
	try:
		deploy.deploy_generation = MagicMock()
		deploy.deploy_condition = MagicMock()
		deploy.deploy_status = MagicMock()
		yield
	finally:
		deploy.deploy_generation = _bup_generation
		deploy.deploy_condition = _bup_condition
		deploy.deploy_status = _bup_status

class Test(unittest.TestCase):

	def test_imports(t):
		t.assertEqual(deploy.deploy_generation.__name__, 'deploy_generation')
		t.assertEqual(deploy.deploy_condition.__name__, 'deploy_condition')
		t.assertEqual(deploy.deploy_status.__name__, 'deploy_status')

	def test_parse(t):
		with mock_mods():
			t.assertDictEqual(deploy.parse({}), {
				'condition': {},
				'condition_index': {},
				'deploy': {},
				'status': {},
				'total': 0,
			})
			deploy.deploy_generation.parse.assert_not_called()
			deploy.deploy_condition.parse.assert_not_called()
			deploy.deploy_status.parse.assert_not_called()

	def test_parse_items(t):
		items = [
			{},
			{'kind': 'Deployment'},
			{
				'kind': 'Deployment',
				'metadata': {},
			},
		]
		with mock_mods():
			sts = deploy.parse({'items': items})
			t.assertDictEqual(sts['condition'], {None: {}})
			t.assertDictEqual(sts['condition_index'], {})
			t.assertIsInstance(sts['deploy'], dict)
			t.assertIsInstance(sts['status'], dict)
			t.assertEqual(sts['total'], 3)
			deploy.deploy_generation.parse.assert_called_once_with({}, {})
			deploy.deploy_condition.parse.assert_called_once()
			deploy.deploy_status.parse.assert_called_once_with({
				'kind': 'Deployment',
				'metadata': {},
			})

	def test_config(t):
		with mock_mods():
			deploy.config({})
			deploy.deploy_generation.config.assert_called_once_with({})
			deploy.deploy_condition.config.assert_called_once_with({})
			deploy.deploy_status.config.assert_called_once_with({})

if __name__ == '__main__':
	unittest.main()
