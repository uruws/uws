#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t

import pods_info

_bup_print = pods_info._print

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		pods_info._print = MagicMock()

	def tearDown(t):
		mon_t.tearDown()
		pods_info._print = _bup_print

	def test_print(t):
		_bup_print('testing')

	def test_parse(t):
		pods = {
			'items': [{}],
		}
		t.assertDictEqual(pods_info.parse(pods), {'total': 0})

	def test_parse_data(t):
		pods = {
			'items': [{'kind': 'Pod'}],
		}
		t.assertDictEqual(pods_info.parse(pods), {'total': 1})

	def test_config(t):
		pods_info.config({})
		config = [
			call('multigraph pod'),
			call('graph_title k8stest pods'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category pod'),
			call('graph_vlabel number'),
			call('graph_printf %3.0lf'),
			call('graph_scale yes'),
			call('total.label total'),
			call('total.colour COLOUR0'),
			call('total.draw AREA'),
			call('total.min 0'),
		]
		pods_info._print.assert_has_calls(config)
		t.assertEqual(pods_info._print.call_count, len(config))

if __name__ == '__main__':
	unittest.main()
