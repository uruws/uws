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

	#
	# globals
	#

	def test_all_export(t):
		t.assertListEqual(wapp.__all__, [
			'Bottle',
			'Logger',
			'request',
			'response',
			'template',
		])

	def test_defaults(t):
		t.assertFalse(wapp.debug)
		t.assertEqual(wapp.port,  2741)

	#
	# logging
	#

	def test_getLogger(t):
		l = wapp.getLogger('testing')
		t.assertIsInstance(l, logging.Logger)

	#
	# main
	#

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

	#
	# nq
	#

	def test_nq_job(t):
		j = wapp._nqrun('/usr/bin/nq /usr/bin/true')
		t.assertIsInstance(j, wapp.NQJob)
		t.assertEqual(j.rc(), 0)
		t.assertTrue(j.id().startswith(','))
		t.assertEqual(j.error(), '')

	def test_nq(t):
		q = wapp.NQ('testing')
		t.assertEqual(q.name, 'testing')
		t.assertEqual(q.app,  'devel')
		t.assertTrue(q.dir.exists())
		q.delete()
		t.assertFalse(q.dir.exists())
		t.assertTrue(q.cleanup)

	def test_nq_defaults(t):
		t.assertEqual(wapp.fqcmd, '/usr/bin/fq')
		t.assertEqual(wapp.nqcmd, '/usr/bin/nq')
		t.assertTrue(wapp.nqdir.startswith('/tmp/wappnq.'))

	def test_nq_env(t):
		q = wapp.NQ('testing')
		t.assertListEqual(sorted(q.env().keys()), [
			'HOME',
			'NQDIR',
			'PATH',
			'USER',
		])

	def test_nq_args(t):
		q = wapp.NQ('testing')
		t.assertEqual(q.args(), ' -c -q ')
		q.cleanup = True
		q.quiet   = False
		t.assertEqual(q.args(), ' -c ')
		q.cleanup = False
		q.quiet   = True
		t.assertEqual(q.args(), ' -q ')
		q.cleanup = False
		q.quiet   = False
		t.assertEqual(q.args(), ' ')

	def test_nq_run(t):
		q = wapp.NQ('testing')
		with wapp_t.mock() as m:
			q.run(['/usr/bin/true'])
			m.nqrun.assert_called_once_with('/usr/bin/nq -c -q /usr/bin/true', env = {
				'USER':  'uws',
				'HOME':  '/home/uws',
				'PATH':  '/usr/bin',
				'NQDIR': Path(wapp.nqdir, 'devel/testing').as_posix(),
			})

if __name__ == '__main__':
	unittest.main()
