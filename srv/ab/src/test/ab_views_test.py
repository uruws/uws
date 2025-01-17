#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib    import contextmanager
from unittest.mock import MagicMock

import unittest

import wapp_t
import wapp

import ab
import ab_views

nqdir = '/opt/uws/ab/test/data/nq'

@contextmanager
def mock_check(rc = 22):
	bup_check = ab_views._check
	try:
		ab_views._check = MagicMock(return_value = rc)
		yield
	finally:
		ab_views._check = bup_check

@contextmanager
def mock_command_parse(nqdir = wapp.nqdir.strip(), cleanup = True):
	bup_command_parse = ab.command_parse
	try:
		with wapp_t.mock(nqdir = nqdir, cleanup = cleanup) as m:
			ab.command_parse = m.command_parse
			ab.command_parse.return_value = m.command_parse_job
			yield m
	finally:
		ab.command_parse = bup_command_parse

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
			m.template.assert_called_once()

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
			m.template.assert_called_once_with('ab/nq.html', abench_nqjobs = [])

	def test_nq_list(t):
		with wapp_t.mock(nqdir = nqdir, cleanup = False) as m:
			ab_views.nq()
			m.template.assert_called_once()

	def test_nq_job(t):
		with wapp_t.mock(nqdir = nqdir, cleanup = False) as m:
			ab_views.nq_job('18989e6df22.19391')
			m.template.assert_called_once_with(
				'ab/nq_job.html',
				job_id = '18989e6df22.19391',
				job_output = 'exec nq /usr/bin/true\n\n\n[exited with status 0.]\n',
			)

	def test_nq_job_not_found(t):
		with wapp_t.mock() as m:
			ab_views.nq_job('123456')
			m.error.assert_called_once_with(
				404,
				'ab/error.html',
				app='ab',
				error="[Errno 2] No such file or directory: '/tmp/wappnq/ab/run/,123456'",
			)

	#---------------------------------------------------------------------------
	# /nq.delete/

	def test_nq_delete(t):
		with mock_command_parse() as m:
			ab_views.nq_delete('abc123.456')
			m.template.assert_called_once_with('ab/job_delete.html', job = m.command_parse_job)

	def test_nq_delete_post(t):
		with wapp_t.mock() as m:
			ab_views.nq_delete_post(nq = m.nq)
			m.redirect.assert_called_once_with('/nq/')

	def test_nq_delete_post_error(t):
		with wapp_t.mock() as m:
			m.request.POST.get.return_value = '123456'
			ab_views.nq_delete_post()
			m.error.assert_called_once_with(
				404,
				'ab/error.html',
				app='ab',
				error="[Errno 2] No such file or directory: '/tmp/wappnq/ab/run/,123456'",
			)

	#---------------------------------------------------------------------------
	# /nq.exec/

	def test_nq_exec(t):
		with mock_command_parse(nqdir = nqdir, cleanup = False) as m:
			ab_views.nq_exec('18989e6df22.19391')
			m.template.assert_called_once_with('ab/job_exec.html', job = m.command_parse_job)

	def test_nq_exec_post(t):
		with wapp_t.mock(nqdir = nqdir, cleanup = False) as m:
			m.request.POST.get.return_value = '18989e6df22.19391'
			ab_views.nq_exec_post()
			m.redirect.assert_called_once_with('/nq/')

	def test_nq_exec_post_error(t):
		with wapp_t.mock() as m:
			m.request.POST.get.return_value = 'abc123'
			m.nq.exec.return_value = m.nq_job
			m.nq_job.rc.return_value = 999
			ab_views.nq_exec_post(nq = m.nq)
			m.error.assert_called_once_with(
				500,
				'ab/error.html',
				app='ab',
				error='command failed: 999',
			)

	def test_nq_exec_job_not_found(t):
		with wapp_t.mock() as m:
			m.request.POST.get.return_value = 'nq_exec.123'
			ab_views.nq_exec_post()
			m.error.assert_called_once_with(
				404,
				'ab/error.html',
				app='ab',
				error='/tmp/wappnq/ab/run/,nq_exec.123: file not found',
			)

	#---------------------------------------------------------------------------
	# /

	def test_home(t):
		with wapp_t.mock() as m:
			ab_views.home()
			m.template.assert_called_once()

	def test_home_jobs(t):
		with wapp_t.mock(nqdir = nqdir, cleanup = False) as m:
			ab_views.home()
			m.template.assert_called_once()

if __name__ == '__main__':
	unittest.main()
