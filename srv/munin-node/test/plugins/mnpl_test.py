#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from pathlib import Path

import unittest

import mnpl_t
import mnpl

class Test(unittest.TestCase):

	def setUp(t):
		mnpl_t.setup()

	def tearDown(t):
		mnpl_t.teardown()

	def test_log_disabled(t):
		t.assertFalse(mnpl._log)
		mnpl.log('testing', '...')
		t.assertEqual(mnpl_t.log_string(), '')

	def test_log_enabled(t):
		mnpl._log = True
		mnpl.log('testing', '...')
		t.assertEqual(mnpl_t.log_string(), 'testing ...')

	def test_error_log(t):
		mnpl.error('testing', '...')
		t.assertEqual(mnpl_t.log_string(), '[E] testing ...')

	def test_cleanfn(t):
		t.assertEqual(mnpl.cleanfn('k8s-test'), 'k8s_test')

	def test_print(t):
		mnpl_t.bup_print('testing', '...')

	def test_clusters(t):
		t.assertEqual(mnpl._clusters_fn, Path('/uws/etc/cluster.json'))
		t.assertListEqual(mnpl.clusters(), [
			{'host': 'k8stest', 'name': 'k8stest'},
		])

	def test_getpw(t):
		t.assertEqual(mnpl._getpw(), 'pwd')
		mnpl._tls_cert = 'test-id'
		t.assertEqual(mnpl._getpw(), '')

	def test_tls_context_auth(t):
		mnpl._tls_cert = mnpl_t.bup_tls_cert
		mnpl._tls_conf = mnpl_t.bup_tls_conf
		ctx = mnpl._context(True)
		t.assertIs(mnpl._ctx_auth, ctx)

	def test_GET(t):
		t.assertIsNone(mnpl.GET('k8stest', mnpl.Config(auth = False)))

if __name__ == '__main__':
	unittest.main()
