#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import mon_t
import mon_kube

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

if __name__ == '__main__':
	unittest.main()
