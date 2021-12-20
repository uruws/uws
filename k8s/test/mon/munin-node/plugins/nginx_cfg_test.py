#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t

import nginx_cfg

_bup_print = nginx_cfg._print
_bup_sts = nginx_cfg.sts

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		nginx_cfg._print = MagicMock()
		nginx_cfg.sts = _bup_sts.copy()

	def tearDown(t):
		mon_t.tearDown()
		nginx_cfg._print = _bup_print

	def test_globals(t):
		t.assertDictEqual(nginx_cfg.sts, {
			'config_hash': 'U',
			'config_last_reload_successful': 'U',
			'config_last_reload_successful_timestamp_seconds': 'U',
		})

	def test_print(t):
		_bup_print('test', 'ing')

	def test_parse(t):
		t.assertFalse(nginx_cfg.parse('testing', None, None))
		t.assertFalse(nginx_cfg.parse('nginx_ingress_controller_config_invalid', None, None))
		t.assertTrue(nginx_cfg.parse('nginx_ingress_controller_config_hash', None, 0.999))
		t.assertDictEqual(nginx_cfg.sts, {
			'config_hash': 0.999,
			'config_last_reload_successful': 'U',
			'config_last_reload_successful_timestamp_seconds': 'U',
		})

	def test_config(t):
		nginx_cfg.config({})
		config = [
			call('multigraph nginx_cfg_hash'),
			call('graph_title Running config hash'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category nginx_cfg'),
			call('graph_vlabel number'),
			call('graph_scale yes'),
			call('hash.label hash'),
			call('hash.colour COLOUR0'),
			call('hash.min 0'),
			call('multigraph nginx_cfg_reload'),
			call('graph_title Config reload status'),
			call('graph_args --base 1000 -l 0 -u 1'),
			call('graph_category nginx_cfg'),
			call('graph_vlabel successful reload'),
			call('graph_scale yes'),
			call('reload.label reload'),
			call('reload.colour COLOUR0'),
			call('reload.draw AREA'),
			call('reload.min 0'),
			call('reload.max 1'),
			call('multigraph nginx_cfg_uptime'),
			call('graph_title Config uptime since last reload'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category nginx_cfg'),
			call('graph_vlabel hours'),
			call('graph_scale no'),
			call('uptime.label uptime'),
			call('uptime.colour COLOUR0'),
			call('uptime.draw AREA'),
			call('uptime.min 0'),
		]
		nginx_cfg._print.assert_has_calls(config)
		t.assertEqual(nginx_cfg._print.call_count, len(config))

if __name__ == '__main__':
	unittest.main()
