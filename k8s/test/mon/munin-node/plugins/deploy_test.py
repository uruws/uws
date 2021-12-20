#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib import contextmanager

import unittest
from unittest.mock import MagicMock, call

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

_bup_print = deploy._print

class Test(unittest.TestCase):

	def setUp(t):
		deploy._print = MagicMock()

	def tearDown(t):
		deploy._print = _bup_print

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

	def test_print(t):
		_bup_print('testing')

	def test_config(t):
		with mock_mods():
			deploy.config({})
			deploy.deploy_generation.config.assert_called_once_with({})
			deploy.deploy_condition.config.assert_called_once_with({})
			deploy.deploy_status.config.assert_called_once_with({})
		config = [
			call('multigraph deploy'),
			call('graph_title None deployments'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category deploy'),
			call('graph_vlabel number'),
			call('graph_printf %3.0lf'),
			call('graph_scale yes'),
			call('a_total.label total'),
			call('a_total.colour COLOUR0'),
			call('a_total.draw AREA'),
			call('a_total.min 0'),
		]
		deploy._print.assert_has_calls(config)

if __name__ == '__main__':
	unittest.main()
