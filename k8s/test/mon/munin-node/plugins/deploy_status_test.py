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

if __name__ == '__main__':
	unittest.main()
