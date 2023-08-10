#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import logging
import unittest

from unittest.mock import call

from pathlib import Path

import wapp_t
import wapp

class TestWapp(unittest.TestCase):

	#---------------------------------------------------------------------------
	# globals

	def test_all_export(t):
		t.assertListEqual(wapp.__all__, [
			'Bottle',
			'Logger',
			'redirect',
			'request',
			'response',
			'template',
		])

	def test_defaults(t):
		t.assertFalse(wapp.debug)
		t.assertEqual(wapp.name,     'devel')
		t.assertEqual(wapp.port,     2741)
		t.assertEqual(wapp.base_url, '/')

	#---------------------------------------------------------------------------
	# logging

	def test_getLogger(t):
		l = wapp.getLogger('testing')
		t.assertIsInstance(l, logging.Logger)

	#---------------------------------------------------------------------------
	# utils

	def test_url(t):
		t.assertEqual(wapp.url('/'), '/')
		t.assertEqual(wapp.url('/testing'), '/testing')
		t.assertEqual(wapp.url('testing/'), 'testing/')
		t.assertEqual(wapp.url('testing'),  'testing')

	def test_url_config(t):
		with wapp_t.mock(base_url = '/b'):
			t.assertEqual(wapp.url('/'),        '/b/')
			t.assertEqual(wapp.url('/testing'), '/b/testing')
			t.assertEqual(wapp.url('testing/'), '/btesting/')
			t.assertEqual(wapp.url('testing'),  '/btesting')

	def test_error(t):
		with wapp_t.mock(mock_error = False) as m:
			wapp.error(500, 'test.tpl', key1 = 'val1', key2 = 'val2')
			t.assertEqual(m.response.status, 500)
			m.template.assert_called_once_with('test.tpl', key1 = 'val1', key2 = 'val2')

	#---------------------------------------------------------------------------
	# main

	def test_start(t):
		with wapp_t.mock_start() as m:
			wapp.start(m.app)
			m.logging.basicConfig.assert_not_called()
			m.app.get.assert_called()

	def test_start_debug(t):
		with wapp_t.mock_start(debug = True) as m:
			wapp.start(m.app)
			m.logging.basicConfig.assert_called_once_with(
				format = wapp.logfmt_debug,
				level  = m.logging.DEBUG,
			)

	def test_run(t):
		with wapp_t.mock() as m:
			wapp.run(m.app)
			m.app.run.assert_called_once_with(
				host     = '0.0.0.0',
				port     = 2741,
				reloader = False,
				debug    = False,
			)

	#---------------------------------------------------------------------------
	# nq

	def test_nq_job_info(t):
		with wapp_t.mock(nqdir = '/opt/uws/lib/test') as m:
			j = wapp.NQJobInfo('==> ,18989e70a11.19428 exec nq /usr/bin/false')
			t.assertEqual(str(j), '==> ,18989e70a11.19428 exec nq /usr/bin/false')
			t.assertEqual(j.id(), '18989e70a11.19428')

	def test_nq_job(t):
		j = wapp._nqrun('/usr/bin/nq /usr/bin/true')
		t.assertIsInstance(j, wapp.NQJob)
		t.assertEqual(j.rc(), 0)
		t.assertTrue(j.id().startswith(','))
		t.assertEqual(j.error(), '')

	def test_nq_job_id(t):
		j = wapp._nqrun('/usr/bin/nq /usr/bin/true')
		j._id = 'testing'
		t.assertEqual(j.id(), 'testing')

	def test_nq(t):
		q = wapp.NQ('testing', app = 'nq')
		t.assertEqual(q.name, 'testing')
		t.assertEqual(q.app,  'nq')
		dh = Path(q.dir)
		t.assertTrue(dh.exists())
		q.delete()
		t.assertFalse(dh.exists())
		t.assertTrue(q.cleanup)
		Path(wapp.nqdir, 'nq').rmdir()
		Path(wapp.nqdir).rmdir()
		t.assertFalse(Path(wapp.nqdir).exists())

	def test_nq_defaults(t):
		t.assertEqual(wapp.fqcmd, '/usr/bin/fq')
		t.assertEqual(wapp.nqcmd, '/usr/bin/nq')
		t.assertTrue(wapp.nqdir.startswith('/tmp/'))

	def test_nq_env(t):
		with wapp_t.mock():
			q = wapp.NQ('testing', app = 'nq_env')
			t.assertListEqual(sorted(q.env().keys()), [
				'HOME',
				'NQDIR',
				'PATH',
				'USER',
			])

	def test_nq_args(t):
		with wapp_t.mock():
			q = wapp.NQ('testing', app = 'nq_args')
			t.assertEqual(q.args(), ' -c ')
			q.cleanup = True
			q.quiet   = False
			t.assertEqual(q.args(), ' -c ')
			q.cleanup = False
			q.quiet   = True
			t.assertEqual(q.args(), ' -q ')
			q.cleanup = False
			q.quiet   = False
			t.assertEqual(q.args(), ' ')

	def test_nqrun(t):
		with wapp_t.mock(nqdir = '/tmp/wappnq') as m:
			q = wapp.NQ('testing', app = 'nqrun')
			q.run(['/usr/bin/true'])
			m.nqrun.assert_called_once_with('/usr/bin/nq -c /usr/bin/true', env = {
				'USER':  'uws',
				'HOME':  '/home/uws',
				'PATH':  '/usr/bin',
				'NQDIR': Path(wapp.nqdir, 'nqrun/testing').as_posix(),
			})

	def test_nqrun_error(t):
		with wapp_t.mock() as m:
			q = wapp.NQ('testing', app = 'nqrun_error')
			m.nqrun.side_effect = wapp_t.mock_nqrun_error
			q.run(['/usr/bin/true'])
			m.nqrun.assert_called_once()

	def test_nqrun_fail(t):
		with wapp_t.mock() as m:
			q = wapp.NQ('testing', app = 'nqrun_fail')
			m.nqrun.side_effect = wapp_t.mock_nqrun_fail
			with t.assertRaises(wapp_t.MockNQRunFail):
				q.run(['/usr/bin/true'])
			m.nqrun.assert_called_once()

	def test_nq_list(t):
		with wapp_t.mock(nqdir = '/opt/uws/lib/test/data/nq') as m:
			q = wapp.NQ('testing')
			t.assertEqual(q.dir, '/opt/uws/lib/test/data/nq/devel/testing')
			l = q.list()
			t.assertEqual(len(l), 3)
			t.assertIsInstance(l[0], wapp.NQJobInfo)
			ids = [j.id() for j in l]
			t.assertListEqual(ids, [
				'18989e6df22.19391',
				'18989e70a11.19428',
				'18989e71777.19432',
			])

	def test_nq_read(t):
		with wapp_t.mock(nqdir = '/opt/uws/lib/test/data/nq') as m:
			q = wapp.NQ('testing')
			text = q.read('18989e6df22.19391')
			t.assertListEqual(text.splitlines(), [
				'exec nq /usr/bin/true',
				'',
				'',
				'[exited with status 0.]',
			])

	def test_nq_rm(t):
		fn = Path('/tmp/wappnq.test_nq_rm/devel/testing/,abc123.delete')
		t.assertFalse(fn.exists())
		with wapp_t.mock(nqdir = '/tmp/wappnq.test_nq_rm') as m:
			q = wapp.NQ('testing')
			dn = Path(q.dir)
			dn.mkdir(parents = True)
			fn.touch()
			t.assertTrue(fn.exists())
			q.rm('abc123.delete')
		t.assertFalse(fn.exists())

	def test_nq_exec(t):
		nqdir = '/tmp/wappnq.test_nq_exec'
		with wapp_t.mock(nqdir = nqdir, mock_run = False) as m:
			q = wapp.NQ('testing')
			q.cleanup = False
			q.quiet = False
			job = q.run(['/bin/true'])
			t.assertEqual(job.error(), '')
			t.assertEqual(job.rc(), 0)
			job2 = q.exec(job.id()[1:])
			t.assertEqual(job2.error(), '')
			t.assertEqual(job2.rc(), 0)

	def test_nq_exec_job_not_found(t):
		nqdir = '/tmp/wappnq.test_nq_exec_job_not_found'
		with wapp_t.mock(nqdir = nqdir) as m:
			with t.assertRaises(FileNotFoundError) as err:
				q = wapp.NQ('testing')
				q.exec('abc123')
			t.assertEqual(str(err.exception),
				'/tmp/wappnq.test_nq_exec_job_not_found/devel/testing/,abc123: file not found')

if __name__ == '__main__':
	unittest.main()
