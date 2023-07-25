#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib    import contextmanager
from unittest.mock import MagicMock

import unittest

import wapp_t
import wapp

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

	#---------------------------------------------------------------------------
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

	#---------------------------------------------------------------------------
	# /run/

	def test_run(t):
		with wapp_t.mock() as m:
			ab_views.run()
			m.template.assert_called_once_with('ab/run.html')

	def test_run_post(t):
		with wapp_t.mock() as m:
			ab_views.run_post()
			m.template.assert_not_called()
			m.redirect.assert_called_once_with('/nq/')

	def test_run_post_exception(t):
		with wapp_t.mock(mock_error = False) as m:
			m.nqrun.side_effect = wapp_t.mock_nqrun_fail
			ab_views.run_post()
			t.assertEqual(wapp.response.status, 500)
			m.template.assert_called_once_with('ab/error.html', app = 'ab', error = 'mock_nqrun_fail')

	def test_run_post_error(t):
		with wapp_t.mock(mock_error = False) as m:
			m.nqrun.side_effect = wapp_t.mock_nqrun_error
			ab_views.run_post()
			t.assertEqual(wapp.response.status, 500)
			m.template.assert_called_once_with('ab/error.html', app = 'ab', error = 'command failed: 999')

	#---------------------------------------------------------------------------
	# /nq/

	def test_nq(t):
		with wapp_t.mock() as m:
			ab_views.nq()
			m.template.assert_called_once_with('ab/nq.html',
				abench_nqjobs = [],
			)

	def test_nq_list(t):
		with wapp_t.mock(nqdir = '/opt/uws/lib/test/data/nq') as m:
			ab_views.nq()
			m.template.assert_called_once()

	def test_nq_job(t):
		with wapp_t.mock(nqdir = '/opt/uws/lib/test/data/nq') as m:
			ab_views.nq_job('18989e6df22.19391')
			m.template.assert_called_once_with(
				'ab/nq_job.html',
				job_id = '18989e6df22.19391',
				job_output = 'exec nq /usr/bin/true\n\n\n[exited with status 0.]\n',
			)

	#---------------------------------------------------------------------------
	# /

	def test_home(t):
		with wapp_t.mock() as m:
			ab_views.home()
			m.template.assert_called_once_with('ab/home.html')

if __name__ == '__main__':
	unittest.main()
