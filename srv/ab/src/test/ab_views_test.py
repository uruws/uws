#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib    import contextmanager
from unittest.mock import MagicMock

import unittest

import wapp_t

import ab_views

@contextmanager
def mock_check(rc = 22):
	bup_check = ab_views._check
	try:
		ab_views._check = MagicMock(return_value = rc)
		yield
	finally:
		ab_views._check = bup_check

class TestViews(unittest.TestCase):

	# /healthz

	def test_healthz(t):
		with wapp_t.mock() as m:
			t.assertEqual(ab_views.healthz(), 'ok')
			t.assertEqual(m.response.content_type, 'text/plain')

	def test_healthz_error(t):
		with mock_check(rc = 99):
			with t.assertRaises(RuntimeError) as err:
				ab_views.healthz()
			t.assertEqual(str(err.exception), 'ab exit status: 99')

	# /run/

	def test_run(t):
		with wapp_t.mock() as m:
			ab_views.run()
			m.template.assert_called_once_with('ab/run.html')

	# /

	def test_home(t):
		with wapp_t.mock() as m:
			ab_views.home()
			m.template.assert_called_once_with('ab/home.html')

if __name__ == '__main__':
	unittest.main()
