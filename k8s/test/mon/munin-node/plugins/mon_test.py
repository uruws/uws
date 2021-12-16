#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib import contextmanager
from io import StringIO

import unittest
from unittest.mock import MagicMock, call

import mon

_bup_print = mon._print

@contextmanager
def mock_openfn(fail = None, fh = None):
	__bup = mon._openfn
	def __open(fn, mode):
		if fail is not None:
			raise fail
		return fh
	try:
		mon._openfn = MagicMock(side_effect = __open)
		yield
	finally:
		mon._openfn = __bup

class Test(unittest.TestCase):

	def setUp(t):
		mon._print = MagicMock()
		mon._cluster = 'k8stest'

	def tearDown(t):
		mon._print = None
		mon._print = _bup_print

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
		_bup_print('testing')

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
		_pod = {
			'metadata': {},
		}
		t.assertIsNone(mon.generateName(_pod))
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
			t.assertEqual(fh.seek(0, 0), 0)
			t.assertEqual(fh.read(), '{"testing": 1}')

	def test_jsonLoad(t):
		with StringIO() as fh:
			t.assertEqual(fh.write('{"testing": 1}'), 14)
			t.assertEqual(fh.seek(0, 0), 0)
			obj = mon._jsonLoad(fh)
			t.assertEqual(fh.seek(0, 0), 0)
			t.assertEqual(fh.read(), '{"testing": 1}')

	def test_cacheSet(t):
		with mock_openfn():
			mon.cacheSet({}, 'testing')

if __name__ == '__main__':
	unittest.main()
