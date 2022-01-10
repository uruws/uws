#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib import contextmanager

import unittest
from unittest.mock import MagicMock, call

import mon_t

import deploy_generation

_bup_print = deploy_generation._print

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		deploy_generation._print = MagicMock()

	def tearDown(t):
		mon_t.tearDown()
		deploy_generation._print = _bup_print

	def test_parse(t):
		t.assertDictEqual(deploy_generation.parse({}, {}), {
			'generation': 'U',
			'observed_generation': 'U',
		})

	def test_print(t):
		_bup_print('test', 'ing')

	def test_config(t):
		deploy_generation.config({
			'test_ns': {
				'test_name': {},
			},
		})
		config = [
			call('multigraph deploy_generation'),
			call('graph_title k8stest deployments generation'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category deploy'),
			call('graph_vlabel number'),
			call('graph_printf %3.0lf'),
			call('graph_scale yes'),
			call('f_test_ns_test_name_cur.label test_ns/test_name cur'),
			call('f_test_ns_test_name_cur.colour COLOUR0'),
			call('f_test_ns_test_name_cur.min 0'),
			call('f_test_ns_test_name_obs.label test_ns/test_name obs'),
			call('f_test_ns_test_name_obs.colour COLOUR0'),
			call('f_test_ns_test_name_obs.min 0')
		]
		t.assertEqual(deploy_generation._print.call_count, len(config))
		deploy_generation._print.assert_has_calls(config)

	def test_report(t):
		deploy_generation.report({
			'test_ns': {
				'test_name': {},
			},
		})
		report = [
			call('multigraph deploy_generation'),
			call('f_test_ns_test_name_cur.value', 'U'),
			call('f_test_ns_test_name_obs.value', 'U'),
		]
		t.assertEqual(deploy_generation._print.call_count, len(report))
		deploy_generation._print.assert_has_calls(report)

if __name__ == '__main__':
	unittest.main()
