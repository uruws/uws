#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import nginx_cfg

class Test(unittest.TestCase):

	def test_globals(t):
		t.assertDictEqual(nginx_cfg.sts, {
			'config_hash': 'U',
			'config_last_reload_successful': 'U',
			'config_last_reload_successful_timestamp_seconds': 'U',
		})

if __name__ == '__main__':
	unittest.main()
