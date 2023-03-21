#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib import contextmanager

import unittest
from unittest.mock import MagicMock, call

import mon_t

import deploy_condition

_bup_print = deploy_condition._print

condition_test = {
	'condition': {'ns': {'name': {'Available': 0, 'Testing': 1}}},
	'condition_index': {'Available': 0, 'Testing': 1},
}

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		deploy_condition._print = MagicMock()

	def tearDown(t):
		mon_t.tearDown()
		deploy_condition._print = _bup_print

	def test_parse(t):
		info = {
			'status': {
				'conditions': [
					{'status': 'True', 'type': 'Testing'},
				],
			},
		}
		sts = {}
		deploy_condition.parse(sts, 'ns', 'name', info)
		t.assertDictEqual(sts, condition_test.copy())

	def test_print(t):
		_bup_print('testing', '...')

	def test_config(t):
		deploy_condition.config(condition_test.copy())
		config = [
			call('multigraph deploy_condition'),
			call('graph_title k8stest deployments condition'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category deploy'),
			call('graph_vlabel number'),
			call('graph_printf %3.0lf'),
			call('graph_scale yes'),
			call('c_Available.label', 'Available'),
			call('c_Available.colour COLOUR0'),
			call('c_Available.min 0'),
			call('c_Testing.label', 'Testing'),
			call('c_Testing.colour COLOUR1'),
			call('c_Testing.min 0'),
			call('multigraph deploy_condition.ns_name'),
			call('graph_title k8stest ns/name condition'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category deploy'),
			call('graph_vlabel number of deployments'),
			call('graph_printf %3.0lf'),
			call('graph_scale yes'),
			call('c_Available.label', 'Available'),
			call('c_Available.colour COLOUR0'),
			call('c_Available.min 0'),
			call('c_Available.critical 0:'),
			call('c_Testing.label', 'Testing'),
			call('c_Testing.colour COLOUR1'),
			call('c_Testing.min 0'),
		]
		t.assertEqual(deploy_condition._print.call_count, len(config))
		deploy_condition._print.assert_has_calls(config)

	def test_report(t):
		deploy_condition.report(condition_test.copy())
		report = [
			call('multigraph deploy_condition'),
			call('c_Available.value', 0),
			call('c_Testing.value', 1),
			call('multigraph deploy_condition.ns_name'),
			call('c_Available.value', 0),
			call('c_Testing.value', 1),
		]
		t.assertEqual(deploy_condition._print.call_count, len(report))
		deploy_condition._print.assert_has_calls(report)

if __name__ == '__main__':
	unittest.main()
