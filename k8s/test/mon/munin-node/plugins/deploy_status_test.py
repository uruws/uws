#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib import contextmanager

import unittest
from unittest.mock import MagicMock, call

import mon_t

import deploy_status

_bup_print = deploy_status._print

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		deploy_status._print = MagicMock()

	def tearDown(t):
		mon_t.tearDown()
		deploy_status._print = _bup_print

	def test_print(t):
		_bup_print('testing')

	def test_parse(t):
		t.assertDictEqual(deploy_status.parse({}), {
			'available_replicas': 'U',
			'ready_replicas': 'U',
			'replicas': 'U',
			'spec_replicas': 'U',
			'updated_replicas': 'U',
		})

	def test_config(t):
		sts = {
			'ns': {
				'testing': {
					'available_replicas': 'U',
					'ready_replicas': 'U',
					'replicas': 'U',
					'spec_replicas': 'U',
					'updated_replicas': 'U',
				},
			},
		}
		deploy_status.config(sts)
		config = [
			call('multigraph deploy_replicas'),
			call('graph_title k8stest deployments replicas'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category deploy'),
			call('graph_vlabel number'),
			call('graph_printf %3.0lf'),
			call('graph_scale yes'),
			call('f_ns_testing.label ns/testing'),
			call('f_ns_testing.colour COLOUR0'),
			call('f_ns_testing.min 0'),
			call('multigraph deploy_replicas.all'),
			call('graph_title k8stest all deployments'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category deploy'),
			call('graph_vlabel number of replicas'),
			call('graph_printf %3.0lf'),
			call('graph_scale yes'),
			call('f_ns_testing.label ns/testing'),
			call('f_ns_testing.colour COLOUR0'),
			call('f_ns_testing.min 0'),
			call('multigraph deploy_replicas.ns_testing'),
			call('graph_title k8stest ns/testing deployment'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category deploy'),
			call('graph_vlabel number of replicas'),
			call('graph_printf %3.0lf'),
			call('graph_scale yes'),
			call('available_replicas.label', 'available'),
			call('available_replicas.colour COLOUR0'),
			call('available_replicas.min 0'),
			call('ready_replicas.label', 'ready'),
			call('ready_replicas.colour COLOUR1'),
			call('ready_replicas.min 0'),
			call('replicas.label', 'running'),
			call('replicas.colour COLOUR2'),
			call('replicas.min 0'),
			call('spec_replicas.label', 'spec'),
			call('spec_replicas.colour COLOUR3'),
			call('spec_replicas.min 0'),
			call('updated_replicas.label', 'updated'),
			call('updated_replicas.colour COLOUR4'),
			call('updated_replicas.min 0'),
		]
		deploy_status._print.assert_has_calls(config)
		t.assertEqual(deploy_status._print.call_count, len(config))

if __name__ == '__main__':
	unittest.main()
