#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib import contextmanager
from io import StringIO
from time import time

import unittest
from unittest.mock import MagicMock, call

import mon_t
import mon

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()

	def tearDown(t):
		mon_t.tearDown()

	def test_system(t):
		t.assertEqual(mon.system('/bin/true'), 0)
		t.assertEqual(mon.system('/bin/false'), 1)

	# logger

	def test_debug(t):
		t.assertFalse(mon.debug())
		try:
			mon._debug = True
			t.assertTrue(mon.debug())
		finally:
			mon._debug = False
		t.assertFalse(mon.debug())

	def test_print(t):
		mon_t._bup_print('testing')

	def test_log(t):
		mon.log('test', 'ing')
		mon._print.assert_called_once_with('test', 'ing')

	def test_dbg(t):
		mon.dbg('testing')
		mon._print.assert_not_called()
		try:
			mon._debug = True
			mon.dbg('test', 'ing')
			calls = [
				call('DEBUG: ', end = ''),
				call('test', 'ing'),
			]
			mon._print.assert_has_calls(calls)
		finally:
			mon._debug = False

	# utils

	def test_cleanfn(t):
		t.assertEqual(mon.cleanfn('testing'), 'testing')
		t.assertEqual(mon.cleanfn('test.ing'), 'test_ing')
		t.assertEqual(mon.cleanfn('_test.ing'), '_test_ing')
		t.assertEqual(mon.cleanfn('_test.in g'), '_test_in_g')
		t.assertEqual(mon.cleanfn('_te/st.in g'), '_te_st_in_g')

	def test_derive(t):
		t.assertEqual(mon.derive('U'), 'U')
		t.assertEqual(mon.derive('testing'), 'testing')
		t.assertEqual(mon.derive('9'), '9')
		t.assertEqual(mon.derive(0.0009), 1)
		t.assertEqual(mon.derive(0.009), 9)
		t.assertEqual(mon.derive(0.001), 1)
		t.assertEqual(mon.derive(1), 1000)
		t.assertEqual(mon.derive(1.3), 1300)
		t.assertEqual(mon.derive(1.7), 1700)
		t.assertEqual(mon.derive(1.9991), 2000)

	def test_cluster(t):
		t.assertEqual(mon.cluster(), 'k8stest')
		try:
			mon._cluster = None
			t.assertIsNone(mon.cluster())
		finally:
			mon._cluster = 'k8stest'
		t.assertEqual(mon.cluster(), 'k8stest')

	def test_color(t):
		t.assertEqual(mon.color(0), 1)
		t.assertEqual(mon.color(28), 0)

	def test_generateName(t):
		t.assertIsNone(mon.generateName({}))
		_pod = {
			'metadata': {
				'generateName': 'testing',
			},
		}
		t.assertEqual(mon.generateName(_pod), 'testing')
		_pod = {
			'metadata': {
				'generateName': 'testing-',
			},
		}
		t.assertEqual(mon.generateName(_pod), 'testing')
		_pod = {
			'metadata': {
				'generateName': 'testing-abc123-',
				'labels': {
					'pod-template-hash': 'abc123',
				},
			},
		}
		t.assertEqual(mon.generateName(_pod), 'testing')

	def test_containerImage(t):
		t.assertEqual(mon.containerImage('testing'), 'testing')
		t.assertEqual(mon.containerImage('testing/image'), 'image')
		t.assertEqual(mon.containerImage('test/ing/img'), 'img')

	def test_cachefn(t):
		t.assertEqual(mon._cachefn('/tmp/testing.x'),
			'/tmp/mon._tmp_testing_x.cache')

	def test_openfn(t):
		with t.assertRaises(FileNotFoundError):
			with mon._openfn('/tmp/testing.fn', 'r'):
				pass

	def test_jsonDump(t):
		with StringIO() as fh:
			mon._jsonDump({'testing': 1}, fh)
			t.assertEqual(fh.getvalue(), '{"testing": 1}')

	def test_jsonLoad(t):
		with StringIO() as fh:
			t.assertEqual(fh.write('{"testing": 1}'), 14)
			t.assertEqual(fh.seek(0, 0), 0)
			obj = mon._jsonLoad(fh)
			t.assertEqual(fh.getvalue(), '{"testing": 1}')

	def test_cacheSet(t):
		with StringIO() as fh:
			with mon_t.mock_openfn(fh = fh):
				mon.cacheSet({}, 'testing')

	def test_cacheSet_error(t):
		with mon_t.mock_openfn(fail = FileNotFoundError('mock_error')):
			mon.cacheSet({}, 'testing')
		mon._print.assert_called_once()

	def test_cacheGet(t):
		with StringIO() as fh:
			tt = time() + 1
			fh.write('{"__cache_expire": %s, "testing": 1}' % tt)
			fh.seek(0, 0)
			with mon_t.mock_openfn(fh = fh):
				t.assertEqual(mon.cacheGet('testing'), {
					'__cache_expire': tt,
					'testing': 1,
				})

	def test_cacheGet_error(t):
		t.assertIsNone(mon_t._bup_cacheGet('testing'))
		mon._print.assert_called_once()

	def test_cacheGet_expired(t):
		with StringIO() as fh:
			t.assertEqual(fh.write('{"__cache_expire": 1}'), 21)
			fh.seek(0, 0)
			with mon_t.mock_openfn(fh = fh):
				t.assertIsNone(mon.cacheGet('testing'))

if __name__ == '__main__':
	unittest.main()
