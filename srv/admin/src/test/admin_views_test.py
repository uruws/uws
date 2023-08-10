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

	#---------------------------------------------------------------------------
	# /

	def test_home(t):
		with wapp_t.mock() as m:
			admin_views.home()
			m.template.assert_called_once_with('admin/home.html')

if __name__ == '__main__':
	unittest.main()
