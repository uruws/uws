#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib import contextmanager
import json

import unittest
from unittest.mock import MagicMock

import mon_t
import mon_kube

def _mock_response(r, status):
	resp = MagicMock()
	resp.read = MagicMock(return_value = r)
	resp.status = status
	return resp

@contextmanager
def mock(resp = {}, resp_status = 200, resp_fail = False):
	_bup_urlopen = mon_kube.urlopen
	_bup_exit = mon_kube._exit
	def _exit(status):
		raise SystemExit(status)
	def _resp_fail():
		raise Exception('mock_error')
	try:
		if resp_fail:
			mon_kube.urlopen = MagicMock(side_effect = _resp_fail)
		else:
			r = json.dumps(resp).encode()
			mon_kube.urlopen = MagicMock(return_value = _mock_response(r, resp_status))
		mon_kube._exit = MagicMock(side_effect = _exit)
		yield
	finally:
		mon_kube.urlopen = _bup_urlopen
		mon_kube._exit = _bup_exit

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()

	def tearDown(t):
		mon_t.tearDown()

	def test_globals(t):
		t.assertEqual(mon_kube._uwskube_url,
			'http://k8s.mon.svc.cluster.local:2800/kube')
		t.assertEqual(mon_kube.UWSKUBE_URL, mon_kube._uwskube_url)

	def test_exit(t):
		with t.assertRaises(SystemExit) as e:
			mon_kube._exit(0)
		err = e.exception
		t.assertEqual(err.args[0], 0)
		with t.assertRaises(SystemExit) as e:
			mon_kube._exit(2)
		err = e.exception
		t.assertEqual(err.args[0], 2)

	def test_get(t):
		with mock():
			t.assertDictEqual(mon_kube._get('testing'), {})

	def test_get_errors(t):
		with mock(resp_status = 500):
			with t.assertRaises(SystemExit) as e:
				mon_kube._get('testing')
			err = e.exception
			t.assertEqual(err.args[0], 8)
		with mock(resp_fail = True):
			with t.assertRaises(SystemExit) as e:
				mon_kube._get('testing')
			err = e.exception
			t.assertEqual(err.args[0], 9)

	def test_parse(t):
		with mock(resp = {'testing': 1}):
			t.assertDictEqual(mon_kube._parse('testing', {}), {})
			# with mods
			tm = MagicMock()
			tm.parse = MagicMock(return_value = 'test')
			mods = {'testing': tm}
			t.assertDictEqual(mon_kube._parse('testing', mods), {'testing': 'test'})
			tm.parse.assert_called_once_with({'testing': 1})

	def test_config(t):
		with mon_t.mock_openfn():
			with mock():
				t.assertEqual(mon_kube._config('testing', {}), 0)
		# with mods
		with mon_t.mock_openfn():
			with mock():
				tm = MagicMock()
				tm.config = MagicMock()
				mods = {'testing': tm}
				t.assertEqual(mon_kube._config('testing', mods), 0)
				tm.config.assert_called_once()

	def test_report(t):
		with mon_t.mock_openfn():
			with mock():
				t.assertEqual(mon_kube._report('testing', {}), 0)
		# with mods
		with mon_t.mock_openfn():
			with mock():
				tm = MagicMock()
				tm.report = MagicMock()
				mods = {'testing': tm}
				t.assertEqual(mon_kube._report('testing', mods), 0)
				tm.report.assert_called_once()

	def test_uri(t):
		t.assertEqual(mon_kube._uri('testing'), f"{mon_kube.UWSKUBE_URL}/testing")

if __name__ == '__main__':
	unittest.main()
