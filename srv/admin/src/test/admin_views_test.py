#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib    import contextmanager
from unittest.mock import MagicMock

import unittest

import wapp_t
import wapp

import admin
import admin_views

class TestViews(unittest.TestCase):

	#---------------------------------------------------------------------------
	# /healthz

	def test_healthz(t):
		t.assertEqual(admin_views.healthz(), 'ok')

if __name__ == '__main__':
	unittest.main()
