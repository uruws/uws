#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock

import mon_t

import nginx_cfg

_bup_print = nginx_cfg._print

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		nginx_cfg._print = MagicMock()

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

if __name__ == '__main__':
	unittest.main()
