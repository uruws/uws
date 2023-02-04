#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from unittest.mock import MagicMock

import unittest

from pathlib import Path

import ab

class TestConfig(unittest.TestCase):

	def test_defaults(t):
		t.assertTrue(ab.debug)
		t.assertEqual(ab.webapp_port, 2741)
		t.assertEqual(ab.cmdpath,     Path('/usr/bin/ab'))

if __name__ == '__main__':
	unittest.main()
