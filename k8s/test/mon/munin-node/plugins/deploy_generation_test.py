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
		_bup_print('testing')

if __name__ == '__main__':
	unittest.main()
